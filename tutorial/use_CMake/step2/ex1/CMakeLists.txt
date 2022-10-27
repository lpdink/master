cmake_minimum_required(VERSION 3.10)
project(HelloLibrary VERSION 1.0)
# 指示待编译的子目录，子目录需要包含一个它的CMakeLists.txt文件
add_subdirectory("./add")
# 添加可执行文件
add_executable(HelloLibrary "hellolibrary.cxx")
# 将可执行文件与静态库文件链接，静态库文件的标识符被定义在子CMakeLists.txt中
target_link_libraries(HelloLibrary PUBLIC MyMathFunction)
# 指示暴露出的库的头文件路径
target_include_directories(HelloLibrary PUBLIC "./add")