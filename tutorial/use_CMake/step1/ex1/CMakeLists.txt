cmake_minimum_required(VERSION 3.10) # 表示本项目构建需要的最低cmake版本。每个cmake项目都应该用这行命令开始。
project(HelloWorld) # 表示项目的开始
add_executable(HelloWorld helloworld.cxx) # 添加编译结果：向HelloWorld项目中，添加helloworld.cxx编译为一个可执行文件。
