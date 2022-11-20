# 在Vscode中使用C++调试

本文将帮助你在VScode中进行cmake的C++工程的可视化调试。  
参考cmake tools [官方教程](https://code.visualstudio.com/docs/cpp/CMake-linux)

## 环境准备

```
vscode
cmake
gdb
插件: C/C++
插件: CMake Tools
```

## 快速开始

要快速创建一个cmake文件，在vscode中输入命令cmake:quick start(通过ctrl+shift+P呼出vscode命令界面)  
这将创建一个包含基本配置的CMakeLists.txt和main.cpp文件。  

## 选择编译器

可以通过命令cmake select a kit来扫描并选择一个编译器，或者点击vscode下方的扳手图标来选择编译器。  
如果你的项目没有配置cmake.sourceDirectory，可以在.vscode/settings.json下配置，索引到CMakeLists.txt所在的目录路径即可。  
或者按照不时出现的提示，选择根CMakeLists.txt文件。  

## 选择编译模式

可以通过vscode下方的警告符号选择，或者输入命令cmake select variant。提供了Debug，Release，MinSizeRel，RelWithDebugInfo四种选项。  
不同选项的附加命令，可以在cmake ui中查看。  

## 编译，运行与调试

可以通过下方的build, 调试符号与倒三角(运行符号)进行，也可以通过命令。  
可以直接在cmakelists.txt涉及的源文件中，在一行代码前单击，出现红点来插入断点。  

## 注意

对多CMakeLists.txt的支持很差，不支持平行项目。  
要debug时，variant模式请选择debug，否则可能出现断点无法激活的问题。  
