exit 0
# 手动完成
## apt 换源
## 你不一定需要做这一工作(尤其在入职企业时)，先检查你的apt源。
## cat /proc/version 查看系统版本
## sudo cp /etc/apt/sources.list /etc/apt/sources.list.bk
## visit: https://developer.aliyun.com/mirror/
## sudo vim /etc/apt/sources.list, :1, $d
## paste
## save.
## sudo apt update
mkdir downloads
cd downloads

## miniconda
conda_path=$(which conda)
if [ $? -ne 0 ];then
wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-Linux-x86_64.sh
bash Miniconda3-py39_4.12.0-Linux-x86_64.sh
vim ~/.condarc
# 去掉注释
# channels:
#   - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
#   - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
#   - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
#   - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
# ssl_verify: true
fi

nvcc_path=$(nvcc -V)
if [ $? -ne 0 ];then
sudo apt-get install nvidia-cuda-toolkit
fi