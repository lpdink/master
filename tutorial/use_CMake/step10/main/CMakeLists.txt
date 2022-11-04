cmake_minimum_required(VERSION 3.10)
# NOTE:指定链接库路径，需要出现在add_executable之前
link_directories("./lib")

add_executable(main main.cxx)

target_include_directories(main PUBLIC "./include")
target_link_libraries(main PUBLIC own_math)