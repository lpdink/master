# 通过docker获取torch-gpu

> 笔者的环境是原生Linux ubuntu 20.04

## 1. 安装docker

与另一篇blog中的做法一致：

> 参考[阿里云docker-ce](https://developer.aliyun.com/mirror/docker-ce/)

```sh
# step 1: 安装必要的一些系统工具
sudo apt-get update
sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common
# step 2: 安装GPG证书
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
# Step 3: 写入软件源信息
sudo add-apt-repository "deb [arch=amd64] https://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
# Step 4: 更新并安装Docker-CE
sudo apt-get -y update
sudo apt-get -y install docker-ce

# 启动
## 如果在原生linux系统下：
sudo systemctl enable docker # 设置开机自启动
sudo systemctl start docker # 启动服务
## 如果在WSL2下：
## wsl不能原生设置开机自启动服务，故每次要在wsl下使用docker，都需要手动启动服务。
## 除非你不关机...？
sudo service docker start
```

## 2. docker根目录修改与镜像加速

docker的默认目录在/var/lib/docker，下载很多镜像并生成容器，有时候会爆外存，有必要将存储目录放到/mnt下。

在国内拉取镜像是比较慢的，需要配置一下加速。

> 这里提供的网易和百度的公共加速是比较慢的，推荐使用阿里云镜像，不过那是私有加速源。

```sh
sudo vim /etc/docker/daemon.json

# 写入
# 如果要修改根目录，注意修改data-root字段
{
  "data-root": "你希望docker根目录的位置，选一个大一点的磁盘",
  "registry-mirrors": [
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com"
  ]
}
# 之后重启docker服务
sudo service docker restart
# 查看是否配置成功
docker info
# 看到Registry Mirrors下是我们的配置项即成功。
```

## 3. 安装nvidia-container-toolkit

有这个工具，才能使用docker的--gpu命令，将gpu分配给容器。

> 参考链接：https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker

```sh
# 设置包仓库和GPG key
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
      && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
      && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
            sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
            sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

## 4. 为当前用户添加docker命令组，以使用vscode-docker插件

```
sudo usermod -aG docker $USER
sudo chmod 666 /var/run/docker.sock
sudo groupadd docker
sudo gpasswd -a $USER docker
newgrp docker
```

## 5. 拉取pytorch-cuda镜像

```sh
sudo docker pull pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

# 启动容器，这里创建了一个名为pdl_obj的容器，将所有的gpu都分配给了容器，
# 将目录/mnt/data/8bitpd挂在在/root/8bitpd下面。
# 将主机9317端口映射到容器的22端口，以便之后能通过ssh直接连接docker
# 添加--shm-size 32G，将共享内存大小提高到32G，保证torch的DataLoader能够多开
sudo docker run --name pdl_obj -it -p 9317:22 --runtime=nvidia --gpus all --shm-size 32G -v /mnt/data/8bitpd:/root/8bitpd pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime bash
```

这一镜像是携带11.6版本的nvcc的，pytorch使用的cuda环境由它决定，而不是nvidia-smi。

## 6. 使得docker可以被ssh访问

### 6.1 远程容器配置

进入容器;
```sh
apt-get update && apt-get install openssh-server openssh-client ssh vim -y
```

修改ssh的配置文件：
```sh
# vim /etc/ssh/sshd_config
# port与之前配置的容器被映射到的端口一致
Port 22 
PermitRootLogin yes
```

重启ssh服务：  
```
/etc/init.d/ssh restart
```

设置root密码：
```
passwd
```

配置ssh-key登录
```sh
将远程服务器的公钥写入远程容器的~/.ssh/authorized_keys中
```

### 6.2 本地vscode配置

由于远程容器并没有公网IP，只能通过远程服务器连接，故这里使用跳板机：

```
Host jump
    HostName jump_ip(就是你远程服务器的Ip)
    User ubuntu
    Port 20310
    IdentityFile 你登录远程服务器的私钥

Host target
    HostName 127.0.0.1
    User root
    Port 9317(我们刚才配置的，远程服务器的9317端口映射到容器的22端口)
    ProxyJump jump
```
> 这里挺绕的，涉及三个主体，即本地，远程服务器，远程服务器的容器。

## 7. 容器的额外配置

### 7.1 apt换源

> 也可以不换，在笔者这里，默认的apt源就挺快的。  

修改/etc/apt/sources.list，推荐在更改前备份。  
与我们刚才下载的一致，这是Ubuntu18.04的apt阿里源  
```
deb https://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb-src https://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse

deb https://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb-src https://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse

deb https://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb-src https://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse

# deb https://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
# deb-src https://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse

deb https://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
deb-src https://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse

```

### 7.2 下载常用的

```sh
apt-get update && apt-get install wget git vim -y
```

### 7.3 git配置

首先生成或者拷贝一个你已经绑定到github/gitlab的私钥给容器的~/.ssh下面。  
注意修改密钥文件权限

```sh
# 密钥生成
ssh-keygen -t ed25519 -C "your_email@email.com"
```

```sh
# 修改权限
chmod 600 ed_25519
chmod 700 ~/.ssh
```

将密钥添加到agent，尝试ssh到github
```sh
ssh-agent bash # 一定要启动才行。
ssh-add ~/.ssh/ed_25519
ssh -T git@github.com
# 看到Hi lpdink! You've successfully authenticated, but GitHub does not provide shell access.就ok了。
```

## 8. 容器的管理与快照

注意：

- 不要终止远程容器的运行，总是将它挂在后台。如果你是从远程服务器进入的docker，使用ctrl+P ctrl+Q将当前容器的终端挂到后台。
- 除非要管理容器，否则不要通过远程服务器登录容器，只使用跳板机从本地直接登录。

容器管理命令：

```sh
# 查看当前所有容器
docker container ls -a

# 连接到执行中的某个容器终端
docker attach container_name
# 或者，注意，此时不再需要进行gpu和端口等资源的分配。
docker exec -it container_id bash 

# 启动容器（一般是已经退出的），注意不是进入容器。
docker container start container_id 

# 将容器提交为镜像
docker commit <container_id> <image_name>:<tag>

# 删除容器，请谨慎操作，确保容器中的重要数据已经被保存为镜像
docker container rm container_name/id
```