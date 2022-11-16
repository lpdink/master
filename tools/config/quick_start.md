# 快速开始：完成常用开发环境的配置
目标是在30min内，将新得到的电脑与服务器，配置成常用开发环境。  
## 本机
### 必要软件
[Chrome](https://www.google.cn/intl/zh-CN/chrome/)  
[Bywave](https://console.bywa.art/cart.php)  
[vscode](https://code.visualstudio.com/download)  
[FileZilla](https://filezilla-project.org/download.php)  
[Notion](https://www.notion.so/desktop)  
[Netron](https://github.com/lutzroeder/netron/releases/)  
### vscode插件
Remote-SSH  
WSL  
### remote配置
```
Host 一个很简单的名字
    HostName 服务器地址
    User 用户名
    Port 端口，一般是22
    IdentityFile 私钥位置，注意win下用\
```
如果需要跳板机
```
Host JumpMachine
    HostName A
    User username
    Port 22

Host TargetMachine
    HostName B
    User username
    Port 8080
    ProxyCommand "ssh.exe的路径，如果没有，安装openssh -W %h:%p JumpMachine
```
## 远程
### 手动配置
```
# 假如取得的是root权限;
# 添加用户
adduser user_name
# 修改用户密码
passwd user_name
# 进入用户
su user_name
# -------------
# 假如是密码登录的.
# 将公钥追加到~/.ssh/authorized_keys
vim ~/.ssh/authorized_keys
```
### 自动配置
参见quick_start.sh
### vscode插件
C/C++  
python  
jupyter  
audio-preview  
Image preview  
LaTeX Workshop  
LaTeX Utilities  
Markdown Preview Enhanced  

## 密钥生成
```
ssh-keygen -t ed25519 -C "your_email@example.com"
```