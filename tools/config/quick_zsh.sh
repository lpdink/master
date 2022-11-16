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
fi
# 切换zsh为默认终端
chsh -s $zsh_path

# 检查oh my zsh安装情况
if [ ! -e $HOME"/.oh-my-zsh" ];then
echo "without oh-my-zsh, prepare to install"
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
fi
zsh
# 检查p10k安装情况
p10k_path=$(which p10k)
if [ $? -ne 0 ];then
echo "without p10k, prepare to install."
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
fi
# 拷贝主题配置
cp ./p10k.zsh $HOME"/.p10k.zsh"
echo "zsh config done."
echo "Use 'zsh' to activate."