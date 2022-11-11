# WSL: windows下的轻量linux系统
> WSL(Windows Subsystem for Linux)是一个在Windows 10\11上能够运行原生Linux二进制可执行文件（ELF格式）的兼容层。它是由微软与Canonical公司合作开发，其目标是使纯正的Ubuntu、Debian等映像能下载和解压到用户的本地计算机，并且映像内的工具和实用工具能在此子系统上原生运行。

对开发者来说，Linux系统比windows更稳定，更方便，除了使用ssh连接到远程的linux服务器外，我们现在可以通过WSL取得一个本地的Linux环境了。本篇文章将说明WSL环境的配置，及在VScode中连接到WSL，就像你通过ssh到远程服务器一样。
## 安装WSL
打开windows终端(CMD)，输入命令：
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
设置免密后，使用user的sudo命令就不再需要输入root密码。  
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
换源几乎总会导致你缺少新源的公钥，结合错误信息，使用以下命令获得公钥：
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