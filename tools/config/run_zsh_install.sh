#!/bin/bash

# 快速配置zsh
echo "开始配置ZSH环境..."

# 检查zsh是否安装
zsh_path=$(which zsh)
if [ $? -ne 0 ]; then
    echo "未找到ZSH，准备安装..."
    if ! sudo apt-get install -y zsh; then
        echo "ZSH安装失败，脚本退出。" >&2
        exit 1
    fi
    zsh_path=$(which zsh)
    if [ $? -ne 0 ]; then
        echo "ZSH安装后仍未找到，脚本退出。" >&2
        exit 1
    fi
fi
echo "ZSH已安装: $zsh_path"

# 切换zsh为默认终端
if ! chsh -s "$zsh_path"; then
    echo "警告: 切换默认shell失败，可能需要手动执行。" >&2
fi

# 检查oh my zsh安装情况
oh_my_zsh_dir="$HOME/.oh-my-zsh"
if [ ! -d "$oh_my_zsh_dir" ]; then
    echo "未找到oh-my-zsh，准备安装..."
    if ! sh -c "$(wget -O- https://gitee.com/mirrors/oh-my-zsh/raw/master/tools/install.sh)"; then
        echo "oh-my-zsh安装失败，脚本退出。" >&2
        exit 1
    fi
fi
echo "oh-my-zsh已安装"

# 检查p10k安装情况
p10k_path="${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k"
if [ ! -d "$p10k_path" ]; then
    echo "未找到Powerlevel10k主题，准备安装..."
    if ! git clone --depth=1 https://gitee.com/romkatv/powerlevel10k.git "$p10k_path"; then
        echo "Powerlevel10k安装失败，脚本退出。" >&2
        exit 1
    fi
fi
echo "Powerlevel10k主题已安装"

# 检查配置文件是否存在并复制
resource_dir="$(dirname "$0")/resources"
if [ -d "$resource_dir" ]; then
    if [ -f "$resource_dir/p10k.zsh" ]; then
        cp "$resource_dir/p10k.zsh" "$HOME/.p10k.zsh"
        echo "已复制Powerlevel10k配置"
    else
        echo "警告: 未找到p10k.zsh配置文件" >&2
    fi
    
    if [ -f "$resource_dir/zshrc.sh" ]; then
        cp "$resource_dir/zshrc.sh" "$HOME/.zshrc"
        echo "已复制ZSH配置"
    else
        echo "警告: 未找到zshrc.sh配置文件" >&2
    fi
else
    echo "警告: 资源目录不存在: $resource_dir" >&2
fi

echo "ZSH配置完成！"
echo "请重启终端或执行 'zsh' 以激活配置"
echo "如果在VSCode中使用，请搜索 'terminal.integrated.fontFamily' 并修改为 'MesloLGS NF'"
echo "如果使用Windows终端，请修改字体为 'MesloLGS NF'"
