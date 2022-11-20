# WSL: Windows下的轻量linux系统

# 导读

相信计算机专业的朋友们几乎都遇到过这样的情况——“需要一个linux系统”，或是在学习机器学习，老师推荐用，或是为windows下麻烦且暗雷无数的开发环境配置而烦心，急需apt或yum这样方便的包管理软件。或是需要一个shell终端，要摆脱windows愚蠢的\\\\路径分割和并不常用的批处理命令，或是某些软件的windows支持非常糟糕，甚至只有linux支持......
在几年前，你的选择不多：

- 在windows下，通过虚拟化软件创建Linux虚拟机。
- 装windows/linux双系统，或仅仅Linux系统。
- 租用远程服务器。

这三个选择的**缺点**都太大了！  
虚拟化软件(如vmware)太笨重，完全版还要收费，还需要自己去再找一个linux发行版镜像，如果找的源不好，下载速度感人。下载完还要导入镜像，填写各种我们从来不关心的配置。
双系统装起来太麻烦！开机时要做选择，对外存的分配也不灵活，两个系统间的文件同步困难。如果只装linux系统，我们只在windows下支持的软件咋办？像CAD,matlab，adobe全家桶...更重要的是，我们还要玩游戏呢！  
远程服务器的配置惊人地低，同时价格却并不便宜，我们从不想为不到1M/s的下行，可怜的2GB的内存和60GB平常都不太用的外存付费！更不要提可恶的云服务器厂商还常常无耻地侵占我们付过钱的资源。

我们花了几千乃至数万块买的电脑(win系统)，难道只能用来打电动吗？（虽然打电动很重要）

在今天，我们的拯救者来了，也就是这次的主角WSL(Windows Subsystem for Linux)，说人话就是，**一个触手可及的linux系统**——它没有上述的任何缺点，无需下载vmware或其他虚拟机软件，也就不需要想办法破解他们，不需要到处找各类系统镜像，然后在虚拟化软件中填写各种我们从来不关心的配置，不用你付钱租用远程服务器，为1M/s不到的下行带宽付费。你可以左手在CAD里画图，右手在子系统里做交叉编译。

使用WSL：

- 无需额外安装软件，且配置极为简单，跟随下面的正文，你只需要不到10分钟。
- 充分利用你平常只用来打游戏或ssh到远程服务器的电脑的性能，包括你的64G大内存，2T高速SSD，RTX4090，Intel-13900k，10000M带宽。虽然他们对打电动也至关重要，但今天，你可以用他们开发了！
- 你可以边在windows上玩游戏/刷B站/爱奇艺/和大家聊天/和网友对线，边在后台的linux子系统上训练模型、编译大型工程或执行其他耗时任务。
- 你放在 “C:\\我的文件” 下的文件，就会出现在Linux子系统的 “/mnt/c/我的文件” 下！反过来也是一样的，你在linux下写的代码，会原封不动地出现在windows文件管理器中！
- 通过VScode连接到WSL的子系统，和连接到远程服务器**一模一样**，同时，你断网的时候也能进行开发。
- 子系统无缝使用GPU，无缝联网，不用做任何配置。（用于模型训练会有少许性能损失）

跟随正文的指引，开始使用WSL吧！让我们的win-PC不再只是游戏机或无情的ssh终端机！

# 正文

> WSL(Windows Subsystem for Linux)是一个在Windows 10\11上能够运行原生Linux二进制可执行文件（ELF格式）的兼容层。它是由微软与Canonical公司合作开发，其目标是使纯正的Ubuntu、Debian等映像能下载和解压到用户的本地计算机，并且映像内的工具和实用工具能在此子系统上原生运行。

对开发者来说，Linux系统比windows更稳定，更方便，除了使用ssh连接到远程的linux服务器外，我们现在可以通过WSL取得一个本地的Linux环境了。本篇文章将说明WSL环境的配置，及在VScode中连接到WSL，就像你通过ssh到远程服务器一样。

## 安装WSL子系统

打开windows终端(CMD)（按下win+R组合键，输入cmd，回车），输入命令：

```
wsl --list --online
```

这将显示当前可下载的linux发行版子系统。  
笔者这里显示为：

```
NAME               FRIENDLY NAME
* Ubuntu             Ubuntu
  Debian             Debian GNU/Linux
  kali-linux         Kali Linux Rolling
  SLES-12            SUSE Linux Enterprise Server v12
  SLES-15            SUSE Linux Enterprise Server v15
  Ubuntu-18.04       Ubuntu 18.04 LTS
  Ubuntu-20.04       Ubuntu 20.04 LTS
  OracleLinux_8_5    Oracle Linux 8.5
  OracleLinux_7_9    Oracle Linux 7.9
```

这里，笔者选择安装Ubuntu-20.04。
> 虽说Debian更稳定，内存消耗也更小，但WSL安装的debian行为奇怪，甚至不能很好地安装vim。

在终端输入：

```
wsl --install -d Ubuntu-20.04
```

需要等待一会儿，这将安装虚拟机平台，适用于 Linux 的 Windows 子系统，及Ubuntu-20.04。  
提示安装完成后，请重启你的电脑。  

## 启动wsl

重启电脑后再次打开CMD终端，尝试输入：

```
wsl
```

如果你只安装了一个子系统，会尝试进入该子系统。  
经过上述步骤，如果提示错误：Error code: Wsl/WSL_E_DEFAULT_DISTRO_NOT_FOUND，可以再次输入：

```
wsl --install -d Ubuntu-20.04
```

这将进入子系统的用户名和密码配置步骤，配置你的用户名和密码，不需要和你的windows系统的用户名或密码有什么关系。  

## 修改root密码

配置完成后会直接进入该用户，但此时不能切换到root身份，因为root密码被随机选定了，你需要手动配置root密码：

```
sudo passwd root
```

这将要求你输入你此前配置用户名和密码时的密码。  
配置完root密码后，你就可以通过su root切换到root身份了。

## 通过vscode连接

在vscode“拓展”中下载插件WSL，之后可以在侧边栏进入远程资源管理器，选择WSL Targets，就可以看到我们刚才安装的ubuntu子系统了。  
点击启动，vscode会帮助我们启动子系统进程(Vmmem)。
一切都很美好，就像你通过vscode-remote连接到远程服务器一样。  

## 卸载WSL子系统

如果你不再使用子系统，或者系统损坏了，可以通过以下命令卸载它：

```
wsl --unregister 子系统名
```

## 附带

新安装的Linux系统需要做一些环境配置，这里附带提及。

### 设置sudo免密

设置免密后，该user的sudo命令就不再需要输入root密码。  

```
sudo vim /etc/sudoers
# 在最后一行添加
要免密的用户名 ALL=(ALL:ALL) NOPASSWD: ALL
```

### 更换apt源

修改/etc/apt/sources.list，推荐在更改前备份。  
这里附带ubuntu 20.04(focal)的阿里源：

```
deb https://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb-src https://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse

deb https://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb-src https://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse

deb https://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb-src https://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse

# deb https://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
# deb-src https://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse

deb https://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
deb-src https://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse

```

注意，apt源与系统版本是对应的，不要使用不匹配的源。  
其他版本的系统源请访问 [阿里云官方镜像站](https://developer.aliyun.com/mirror/)  
> 你可以通过uname -a命令或cat /proc/version来查看系统版本，不过在WSL下，貌似看不出来。不过你能记得自己上面装了哪个系统的。

修改完成后重新获取apt源的软件list:

```
sudo apt update
```

如果你想要升级本地的旧版本软件：

```
sudo apt upgrade
```

换源有时会导致你缺少新源的公钥，结合错误信息，使用以下命令获得公钥：

```
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 报错信息提示的公钥(可以是多个，用空格分割)
```

### 安装miniconda

```
wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-Linux-x86_64.sh
```

换源：

```
# vim 创建或修改~/.condarc为
channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
ssl_verify: true
```

### 安装nvidia的工具包

```
sudo apt install nvidia-cuda-toolkit
```
