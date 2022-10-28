root=$(cd $(dirname $0); pwd)
cd $root
# 如果构建目录不存在，创建它
if [ ! -d "./rst" ];then
    mkdir ./rst
    mkdir ./install_rst
else
# 如果存在，清理，并重新创建
    rm -rf ./rst
    rm -rf ./install_rst
    mkdir rst
    mkdir install_rst
fi
cd ./rst
# 执行cmake构建，将结果存放到当前目录(rst)
cmake ../
# 执行cmake编译，将编译的可执行文件存放到当前目录(rst)
cmake --build .

# 安装。这里通过DESTDIR="../install_rst"指定了安装路径。
## 毕竟是测试工程，不便安装到/use/bin下。
make install DESTDIR="../install_rst"