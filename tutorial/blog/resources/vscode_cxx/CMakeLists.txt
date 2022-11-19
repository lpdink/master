cmake_minimum_required(VERSION 3.2)
add_compile_options(-Wall -Wextra)
include_directories("./")
add_executable(myExec main.cc function.cc)