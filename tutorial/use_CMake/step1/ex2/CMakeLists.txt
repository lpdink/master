cmake_minimum_required(VERSION 3.10) # 表示本项目构建需要的最低cmake版本。每个cmake项目都应该用这行命令开始。

project(HelloWorld) # 表示项目的开始

# 如果不设置这两行，shared指针依然能发挥作用，这让人疑惑。
# set(CMAKE_CXX_STANDARD 11) # 设置C++标准为11
# set(CMAKE_CXX_STANDARD_REQUIRED True) # 启用C++标准设置，与上条语句一起使用

add_executable(HelloWorld helloworld.cxx) # 添加编译结果：向HelloWorld项目中，添加helloworld.cxx编译为一个可执行文件。
