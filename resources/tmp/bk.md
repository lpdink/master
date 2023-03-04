# 如何快速借用开源算法repo测试自己的idea——以本次任务为例

## 定位关键点

算法repo有几个关键点，在我们拿到仓库后，应该第一时间定位。

- 训练主循环，常在main.py，train.py等文件中，可以在repo全局搜索epoch，找到以epoch为循环变量的循环，一般就是训练主循环。  
找到主循环，一般可以连带着找到模型、数据集、优化器、损失等等。

- 模型. 一般继承自torch.nn.Module，可能有多继承，全局搜索nn.Module。
- 数据集. 全局搜索data_loader。
- 损失函数设计. 全局搜索loss。

找到训练主循环后，在vscode中为服务器或本地安装python插件，就能在按住ctrl键时，从标识符调用处找到标识符定义处，这样就能找到模型、数据集、损失函数的定义。  

## step1: 调用teacher模型，完成推理，保存推理结果

要调用训练好的模型进行推理，需要以下资源：
- 模型的外存文件(.pt, .pth, .pkl)
- 模型结构(代码定义，一个nn.Module子类)
- 推理的输入数据

逻辑是：
1. 申请一个模型类的对象
2. 将外存模型文件载入；
3. 处理好推理的输入数据
4. 将输入数据喂给模型的__call__/forward/infer/predict，取得输出

对于本次任务，我们已经有了模型的外存文件，一个路径。因此需要寻找两个东西：
- 模型结构定义
- repo的数据处理方法

首先来找模型的结构定义：  
train_all是一个更外层的循环，多个模型。在trainer.py中包裹了主循环。通过闭包自省的方法捕获的模型定义。闭包与自省的知识参考流畅的python。  
从/home/zhidan/xiaozeyu/zhou_project/miro/domainbed/trainer.py:22，进入get_algorithm_class的函数定义，其通过:

```py
from .algorithms import *
globals()[algorithm_name]
```

捕获了准备使用的模型的类，因此模型定义在.algorithms中，具体由传入参数args.algorithm决定。  
本次任务中，我们使用的是ERM，故在.algorithms中寻找类ERM。

善用搜索，很容易找到ERM定义为：
```py
class ERM(Algorithm):
    """
    Empirical Risk Minimization (ERM)
    """

    def __init__(self, input_shape, num_classes, num_domains, hparams):
        super(ERM, self).__init__(input_shape, num_classes, num_domains, hparams)
        self.featurizer = networks.Featurizer(input_shape, self.hparams)
        self.classifier = nn.Linear(self.featurizer.n_outputs, num_classes)
        self.network = nn.Sequential(self.featurizer, self.classifier)
        self.optimizer = get_optimizer(
            hparams["optimizer"],
            self.network.parameters(),
            lr=self.hparams["lr"],
            weight_decay=self.hparams["weight_decay"],
        )

    def update(self, x, y, **kwargs):
        all_x = torch.cat(x)
        all_y = torch.cat(y)
        loss = F.cross_entropy(self.predict(all_x), all_y)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return {"loss": loss.item()}

    def predict(self, x):
        return self.network(x)
```

注意到：
- 类的构造函数需要input_shape, num_classes, num_domains, hparams四个参数。
- 本repo的损失函数是一个简单的交叉熵损失，并没有自行定义复杂损失。  
- update中包含了损失计算/优化器step/反向传播过程，因此我们后续的训练无需在主循环中写这些。  
- 定义了predict函数，且是十分简单的前向传播，说明模型中不存在人工特征或复杂结构。  

由于类的构造函数要求四个参数，我们寻找原repo是怎样申请模型对象的。  
这一定在训练主循环附近，回到trainer.py，注意到/home/zhidan/xiaozeyu/zhou_project/miro/domainbed/trainer.py:100 是主循环代码在获取模型对象:

```py
algorithm = algorithm_class(
        dataset.input_shape,
        dataset.num_classes,
        len(dataset) - len(test_envs),
        hparams,
    )
```

显然依赖于dataset，test_envs和hparams。  
从行为看，dataset显然是一个复杂的对象，test_envs则可能是内置对象，hparams显然指超参数，多半是字典或类似对象。  
寻找dataset的定义，通过ctrl加点击，注意到在/home/zhidan/xiaozeyu/zhou_project/miro/domainbed/trainer.py:35.


```py
dataset, in_splits, out_splits = get_dataset(test_envs, args, hparams, algorithm_class)
```

故进入get_dataset：

```py
def get_dataset(test_envs, args, hparams, algorithm_class=None):
    """Get dataset and split."""
    is_mnist = "MNIST" in args.dataset
    dataset = vars(datasets)[args.dataset](args.data_dir)
    #  if not isinstance(dataset, MultipleEnvironmentImageFolder):
    #      raise ValueError("SMALL image datasets are not implemented (corrupted), for transform.")

    in_splits = []
    out_splits = []
    for env_i, env in enumerate(dataset):
        # The split only depends on seed_hash (= trial_seed).
        # It means that the split is always identical only if use same trial_seed,
        # independent to run the code where, when, or how many times.
        # breakpoint()
        out, in_ = split_dataset(
            env,
            int(len(env) * args.holdout_fraction),
            misc.seed_hash(args.trial_seed, env_i),
        )
        if env_i in test_envs:
            in_type = "test"
            out_type = "test"
        else:
            in_type = "train"
            out_type = "valid"

        if is_mnist:
            in_type = "mnist"
            out_type = "mnist"

        set_transfroms(in_, in_type, hparams, algorithm_class)
        set_transfroms(out, out_type, hparams, algorithm_class)

        if hparams["class_balanced"]:
            in_weights = misc.make_weights_for_balanced_classes(in_)
            out_weights = misc.make_weights_for_balanced_classes(out)
        else:
            in_weights, out_weights = None, None
        in_splits.append((in_, in_weights))
        out_splits.append((out, out_weights))

    return dataset, in_splits, out_splits
```

发现较为复杂，且存在transform这类意味着数据前处理的逻辑，不便理解，且不能抛开独立使用PIL读取训练数据。故最好当成黑盒，尝试复用它。  
由于未进入训练主循环，并不会影响反向传播，故可以直接在附近插断点breakpoint()，进入pdb，尝试解析三个返回值dataset, in_splits, out_splits。  

```sh
(Pdb) dataset
<domainbed.datasets.datasets.PACS object at 0x7f23bc353f40>
(Pdb) dir(dataset)
['CHECKPOINT_FREQ', 'ENVIRONMENTS', 'INPUT_SHAPE', 'N_STEPS', 'N_WORKERS', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'datasets', 'dir', 'environments', 'input_shape', 'num_classes']
(Pdb) dataset.dir
'/home/zhidan/zhidan/PACS/'
(Pdb) dataset.datasets
[Dataset ImageFolder
    Number of datapoints: 2048
    Root location: /home/zhidan/zhidan/PACS/art_painting, Dataset ImageFolder
    Number of datapoints: 2344
    Root location: /home/zhidan/zhidan/PACS/cartoon, Dataset ImageFolder
    Number of datapoints: 1670
    Root location: /home/zhidan/zhidan/PACS/photo, Dataset ImageFolder
    Number of datapoints: 3929
    Root location: /home/zhidan/zhidan/PACS/sketch]
(Pdb) dataset.environments
['art_painting', 'cartoon', 'photo', 'sketch']
(Pdb) dataset.input_shape
(3, 224, 224)
(Pdb) dataset.num_classes
7
```
首先通过dir()函数获取dataset的已定义的函数及数据成员，__前缀的是python的魔术方法，具体参考流畅的python.  
可以看到'datasets', 'dir', 'environments', 'input_shape', 'num_classes'四个明显的自定义方法，分别调用打印。  
含义是容易理解的，
- datasets指向了torchcv提供的imageFolder，其用法可以百度到。  
- dir指向了数据路径，显然通过args传入。
- input_shape对应于数据的shape，我们在做cv任务，这显然是指一个3通道，224*224的图片。
- 我们在做分类任务，num_classes显然指类别多少。
- env指多种风格/子文件夹名。

用类似的方法解析in_splits，可以得到分析：
```sh
    # in_splits size==4,
    # dtype = (_SplitDataset, None)
    # [(<domainbed.datasets._SplitDataset object at 0x7f246b786410>, None), (<domainbed.datasets._SplitDataset object at 0x7f246b786470>, None), (<domainbed.datasets._SplitDataset object at 0x7f246b786530>, None), (<domainbed.datasets._SplitDataset object at 0x7f246b7865f0>, None)]

    # _SplitDataset
    # 存在keys range(pic_num_under_folder)
    # 数量与在目录/home/zhidan/zhidan/PACS/art_painting下求：
    # find ./   -name "*.jpg" | wc -l 的结果一致。
    # 存在属性underlying_dataset，指向实际使用的ImageFolder，这是torchcv提供的类，指向/home/zhidan/zhidan/PACS/art_painting这一级目录后，能智能地读取图片数据。
    # 可以通过in_splits[i][0][j]['x'/'y']访问到训练数据，其中i对应要访问的数据集，0是art_painting，1是cartoon，2是photo，3是sketch. j必须小于len(in_splits[i][0].keys)范围。'x'与'y'决定访问data或是target。
    # x是tensor，固定为[3, 224, 224]
    # y是int，范围为[0, 3]
```

由于在in_splits中取得了数据，其shape==[3, 224, 224]，判断为图片数据。故我们在31行要求的repo的数据处理方法也得到了，get_dataset方法调用了某些数据前处理，通过这个黑盒，我们取得了数据处理结果。  
get_dataset方法的四个要求参数test_envs, args, hparams, algorithm_class=None，在pdb中也是显然的，不赘述。故我们可以另起一个脚本，自行调用该方法，取得训练或测试数据了。  

解析了dataset，构造模型对象要求的四个参数input_shape, num_classes, num_domains, hparams也就能得到了。  
至此，两个条件达成，我们开始撰写infer脚本：

```py
    algorithm_class = ERM
    test_envs = [model_idx]  # 相当于先推model_idx
    # model =
    # test_envs:[0], [1], [2], [3]

    dataset, in_splits, out_splits = get_dataset(
        test_envs, config.args, config.hparams, algorithm_class
    )

    model = ERM(
        dataset.input_shape, dataset.num_classes, num_domains=3, hparams=config.hparams
    )
    # 载入模型
    ckpt = torch.load(ckpt_path)
    # 搜索一下torch.save，看看怎么存的，就怎么载入.
    model.load_state_dict(ckpt["model_dict"])
```

之前已经知道，模型对象具备predict方法，故我们准备好数据后，调用即可得到predict_result。  
这里有一些注意点：  
- predict接受的tensor的shape。
- CPU推理与GPU推理
- 避免推理被killed

稍微修改逻辑，对三个教师模型，用三个他们分别没见过的数据集进行推理，通过torch.save方法保存推理结果到外存。得到  
- in_.pt
- out_.pt
- pre_.pt

三个tensor结果，step1至此结束。

## step2: 训练学生模型

在step1中，我们很好地拆分出了数据集和模型对象的得到过程，故可以自己写train脚本。  
dl训练模型需要：
- 模型
- 数据
- 损失
- 优化器
- 主循环

先看损失：由于本repo将损失计算与优化器和反向传播等等都放在模型定义部分，故我们继承该模型类，重写损失计算部分：

```py
class ERMStudent(ERM):
    def __init__(self, input_shape, num_classes, num_domains, hparams):
        super().__init__(input_shape, num_classes, num_domains, hparams)
        self.distillation_loss = nn.KLDivLoss() # KL散度损失
        self.temperature = 4 # 温度4
        self.alpha = 0.25 # 蒸馏损失权重

    def update(self, x, y, teacher_pred):
        student_pred = self.predict(x)
        student_loss = F.cross_entropy(student_pred, y) # hard loss
        distillation_loss = self.distillation_loss(F.log_softmax(student_pred/self.temperature, dim=1), F.softmax(teacher_pred/self.temperature, dim=1))

        loss = (1-self.alpha)*student_loss + self.alpha*distillation_loss
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        return {"total_loss": loss.item(), "hard_loss":student_loss.item(), "distillation_loss":distillation_loss.item()}
```

蒸馏的损失计算，选用范例的KL散度。超参数随手选的。    

数据和主循环：我们的数据来源于刚刚保存的三个pt文件，将他们载入。为了方便切割batch_size大小的块，我们诉诸torch提供的dataloader，这要求我们实现一个可迭代对象（参考流畅的Python）：

```py
from torch.utils.data import Dataset, DataLoader

class DisDataset(Dataset):
    def __init__(self, x, y, teacher_pred) -> None:
        self.x = x.to(device)
        self.y = y.to(device)
        self.teacher_pred = teacher_pred.to(device)

    def __len__(self):
        return len(self.y)
    
    def __getitem__(self, idx):
        return self.x[idx, :, :, :], self.y[idx], self.teacher_pred[idx, :]

dis_dataset = DisDataset(input_dataset, true_dataset, pred_dataset)
data_loader = DataLoader(dis_dataset, batch_size)
```

这样，就能通过对data_loader的迭代行为取得数据了。  

由于优化器、反向过程都在模型部分定义，故主循环是简单的：

```py
for i_tensor, o_tensor, p_tensor in data_loader:
    loss = model.update(i_tensor, o_tensor, p_tensor)
```

为了迭代多个epoch，并隔一会儿保存一下模型，打印损失，我们加入一些细节：

```py
while True:
    for i_tensor, o_tensor, p_tensor in data_loader:
        loss = model.update(i_tensor, o_tensor, p_tensor)
        logging.info(f"{loss} at step {step_idx+1}")
        if (step_idx+1)%save_steps==0:
            save_path = os.path.join(model_save_path, f"S_ERM_{step_idx+1}.pt")
            torch.save(model.state_dict(), save_path)
            logging.warning(f"model save at {save_path}")
        step_idx+=1
        if step_idx>total_steps:
            break
    if step_idx>total_steps:
        break
```

执行模型训练，保存训练结果。
step2结束。

## step3: 验证

与step1的行为类似，只是换成调用4号模型和我们刚刚训练好的学生模型而已。不赘述

## 主要知识点

- 在ide中通过ctrl完成跳转
- 插入breakpoint()可以进入pdb模式，pdb模式的n, s, c，u。
- 通过dir(obj)可以取得obj的已定义方法和属性，dir()取得当前环境的已定义标识符。
- globals()的内省
- torch载入模型的routine
- torch保存张量或模型的api
- torch-data_loader的使用
- 可迭代对象
- torch- ImageFolder
- torch的张量操作
- torch的单条推理与批推理
- 生成器表达式
- 常用common组件

