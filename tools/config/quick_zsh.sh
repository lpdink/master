# 请手动下载并安装字体文件到本地计算机！
# https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Regular.ttf
# https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold.ttf
# https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold.ttf
# https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold%20Italic.ttf

# 快速配置zsh
zsh_path=$(which zsh)
# 下载
if [ $? -ne 0 ];then
echo "without zsh, prepare to install."
sudo apt-get install zsh
cp ./zshrc.sh $HOME"/.zshrc"
fi
# 切换zsh为默认终端
chsh -s $zsh_path

# 检查oh my zsh安装情况
if [ ! -e $HOME"/.oh-my-zsh" ];then
echo "without oh-my-zsh, prepare to install"
sh -c "$(curl -fsSL https://gitee.com/mirrors/oh-my-zsh/raw/master/tools/install.sh)"
fi
# 检查p10k安装情况
p10k_path=${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
if [ ! -e $p10k_path ];then
echo "without p10k, prepare to install."
git clone --depth=1 https://gitee.com/romkatv/powerlevel10k.git $p10k_path
fi
# 拷贝主题配置
cp ./p10k.zsh $HOME"/.p10k.zsh"
echo "zsh config done."
echo "Use 'zsh' to activate."
