# 从零开始的go语言笔记

## 引言

go在web开发上的优势无需多言，作为新兴语言，没有java那样沉重的历史包袱（与相当多的过度设计），适合作为高性能web服务端开发的工具语言。docker, k8s等明星项目为go在云计算方向的应用铺平了道路，使得它在足够简单的基础下，又具备很高的上限。  

以上都足以作为笔者（及读者你）开始学习go的原因：它十分简单，高效开发，性能强劲，在部署上的便利性令人震撼。  

## 环境配置

笔者选择在ubuntu下进行go开发，vscode提供ide支持。  
访问 [go开发者官网](https://go.dev/) 获取最新提供的稳定版：

```shell
wget https://go.dev/dl/go1.19.3.linux-amd64.tar.gz
```

将它解压到/usr/local下：

```shell
# 先确保/usr/local下没有go目录，可以用rm -rf /usr/local/go删除。否则会破坏go安装。
sudo tar -C /usr/local -xzf go1.19.3.linux-amd64.tar.gz
```

添加到环境变量：

```sh
export PATH="$PATH:/usr/local/go/bin"
```

查看go版本

```sh
go version
# go version go1.19.3 linux/amd64
```

## install换源

go 1.13以上：

```
go env -w GO111MODULE=on
go env -w GOPROXY=https://mirrors.aliyun.com/goproxy/,direct
```

## Hello World

### 启动依赖追踪

```sh
go mod init hello_world # 最后一项是你的项目名
```

这将在当前目录下创建go.mod文件，用于保存项目依赖。

### src与执行

```go
package main // 类似namespace?

import "fmt" // 标准库，包括格式化字符串和打印到终端

func main() {
	fmt.Println("Hello, World!")
}
```

执行：

```sh
go run .
```
