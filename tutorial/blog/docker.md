# 开始使用Docker

> 笔者的环境是win11 wsl2 ubuntu20.04

## 安装与启动

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

## 镜像加速

在国内拉取镜像是比较慢的，需要配置一下加速。

```sh
sudo vim /etc/docker/daemon.json

# 写入
{
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

## 拉取镜像

不妨先拉一个Ubuntu18.04下来，惊人的是，这只有25MB左右！

```sh
docker pull ubuntu:18.04
```

一次性使用的容器：

```sh
# -i是交互操作, -t是终端，--rm表示退出后删除，最后是使用bash
docker run -it --rm ubuntu:18.04 bash
```

这会让我们以root身份进入容器根目录。在根目录执行du命令，发现解压后系统只有仅仅69MB，真棒啊。
cat /etc/os-release可以看到Ubuntu18.04 LTS了。
通过exit可以退出容器了。

## 常用命令

> 傻瓜式使用，赞美！

```sh
# 列出镜像，添加-a参数可以看到中间层（复用层），不建议这么做
docker image ls

# 查看docker的实际占用空间。docker提供层复用，通过本命令查看真实的外存占用
docker system df 

# 删除镜像，注意是镜像，不是容器
docker image rm image_name

# 查看容器情况
docker container ls

# 从外部终止某容器运行
docker container stop container_id 

# 启动容器（一般是已经退出的），注意不是进入容器。
docker container start container_id 

# 进入容器
docker exec -it container_id bash 
# exec的格式为docker exec [OPTIONS] CONTAINER COMMAND [ARG...]同时需要容器和命令

# 导出容器到外存，这保存的是快照信息
docker export container_id > ubuntu.tar

# 导入容器到镜像，test/ubuntu将是镜像名，v1.0将是标签名
cat ubuntu.tar | docker import - test/ubuntu:v1.0

# 删除已exit的容器。如果要删除执行中的，添加-f参数
docker container rm container_id

# 删除所有已经终止运行的容器
docker container prune

```

## TODO：dockerfile与容器合并
