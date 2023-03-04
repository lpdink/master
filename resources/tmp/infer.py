import torch
import torch.nn as nn
import PIL
import os
import numpy as np

# model
from domainbed.algorithms.algorithms import ERM
from domainbed.datasets import get_dataset
from config import config

model_idx = 0
ckpt_path = f"/home/zhidan/zhidan/codes_Distill/train_output/PACS/230301_09-43-01_exp_name/checkpoints/TE{model_idx}_5000.pth"

device = "cuda:0" if torch.cuda.is_available() else "cpu"

def main():
    algorithm_class = ERM
    test_envs = [model_idx]  # 相当于先推model_idx
    # model =
    # test_envs:[0], [1], [2], [3]

    dataset, in_splits, out_splits = get_dataset(
        test_envs, config.args, config.hparams, algorithm_class
    )
    # in_splits size==4,
    # dtype = (_SplitDataset, None)
    # [(<domainbed.datasets._SplitDataset object at 0x7f246b786410>, None), (<domainbed.datasets._SplitDataset object at 0x7f246b786470>, None), (<domainbed.datasets._SplitDataset object at 0x7f246b786530>, None), (<domainbed.datasets._SplitDataset object at 0x7f246b7865f0>, None)]

    # _SplitDataset
    # 存在keys range(pic_num_under_folder)
    # 数量与在目录/home/zhidan/zhidan/PACS/art_painting下求：
    # find ./   -name "*.jpg" | wc -l 的结果一致。
    # 存在属性underlying_dataset，指向实际使用的ImageFolder，这是torchcv提供的类，指向/home/zhidan/zhidan/PACS/art_painting这一级目录后，能智能地读取图片数据。
    # 可以通过in_splits[i][0][j]['x'/'y']访问到训练数据，其中i对应要访问的数据集，0是art_painting，1是cartoon，2是photo，3是sketch. j必须小于len(in_splits[i][0].keys)范围。'x'与'y'决定访问data或是target。
    # x是tensor，固定为[3, 244, 244]
    # y是int，范围为[0, 3]
    dataset_1 = in_splits[model_idx][0]
    dataset_2 = out_splits[model_idx][1]

    # input_shape==[3, 244, 244]
    # num_classes==7
    # num_domains==3
    model = ERM(
        dataset.input_shape, dataset.num_classes, num_domains=3, hparams=config.hparams
    )
    # 载入模型
    ckpt = torch.load(ckpt_path)
    # 怎么存的，就怎么载入.
    model.load_state_dict(ckpt["model_dict"])

    model.eval()
    # 逐条推理
    # point = 0
    # for idx in range(len(dataset_1.keys)):
    #     with torch.no_grad():
    #         input_tensor = dataset_1[idx]['x'].unsqueeze(0) # 在第0维增加batch维度
    #         true_class = dataset_1[idx]['y']
    #         predict_rst = model.predict(input_tensor)
    #         if predict_rst.numpy().squeeze().argmax()==true_class:
    #             point+=1
    #             torch.stack()
    # print(f"正确率：{point/len(dataset_1.keys)}")

    # batch 推理
    batch_input_tensor = [dataset_1[idx]["x"] for idx in range(len(dataset_1.keys))]
    true_batch = np.array([dataset_1[idx]["y"] for idx in range(len(dataset_1.keys))])
    # 在第0维上堆叠，作为batch。
    batch_input_tensor = torch.stack(batch_input_tensor, 0)
    # batch_size太大，在GPU上推会爆显存，在CPU上推也不算慢。
    model = model
    batch_input_tensor = batch_input_tensor
    with torch.no_grad():
        predict_rst = model.predict(batch_input_tensor)
        print(f"准确率：{sum(predict_rst.argmax(1).numpy()==true_batch)/len(true_batch)}")
        breakpoint()

def infer():
    algorithm_class = ERM
    input_lists = []
    output_lists = []
    predict_lists = []
    for idx in range(3):
        test_envs = [idx]
        dataset, in_splits, out_splits = get_dataset(
        test_envs, config.args, config.hparams, algorithm_class
        )
        breakpoint()
        dataset_1 = in_splits[idx][0]
        dataset_2 = out_splits[idx][0]

        batch_input_tensor_1 = [dataset_1[idx]["x"] for idx in range(len(dataset_1.keys))]
        batch_input_tensor_2 = [dataset_2[idx]["x"] for idx in range(len(dataset_2.keys))]
        batch_input_tensor = batch_input_tensor_1+batch_input_tensor_2
        batch_input_tensor = torch.stack(batch_input_tensor, 0)
        # breakpoint()
        true_batch_1 = [dataset_1[idx]["y"] for idx in range(len(dataset_1.keys))]
        true_batch_2 = [dataset_2[idx]["y"] for idx in range(len(dataset_2.keys))]
        true_batch = torch.tensor(true_batch_1+true_batch_2)
        # np.concatenate()
        model = ERM(
            dataset.input_shape, dataset.num_classes, num_domains=3, hparams=config.hparams
        )
        # 载入模型
        ckpt_path = f"/home/zhidan/zhidan/codes_Distill/train_output/PACS/230301_09-43-01_exp_name/checkpoints/TE{idx}_5000.pth"
        ckpt = torch.load(ckpt_path)
        # 怎么存的，就怎么载入.
        model.load_state_dict(ckpt["model_dict"])
        model.eval()
        with torch.no_grad():
            predict_rst = model.predict(batch_input_tensor)# shape==[pic_nums, class_nums] like [2048, 7]
            # breakpoint()
        input_lists.append(batch_input_tensor)
        output_lists.append(true_batch)
        predict_lists.append(predict_rst)
    # 每轮的input在图片idx维度concat
    input_rst = torch.cat(input_lists, 0)
    output_rst = torch.cat(output_lists, 0)
    predict_rst = torch.cat(predict_lists, 0)
    return input_rst, output_rst, predict_rst


if __name__ == "__main__":
    # main()
    # 将输入，输出，推理得到的结果保存到外存中，作为学生模型的训练数据
    # 至此，数据准备阶段结束。
    in_, out_, pre_ = infer()
    torch.save(in_, "in_.pt")
    torch.save(out_, "out_.pt")
    torch.save(pre_, "pre_.pt")
    breakpoint()
