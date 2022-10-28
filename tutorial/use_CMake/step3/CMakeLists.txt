cmake_minimum_required(VERSION 3.10)
project(HelloLibrary VERSION 1.0)

option(USE_LIBRARY "Use add in library." OFF)

# 添加可执行文件
add_executable(HelloLibrary "hellolibrary.cxx")

if(USE_LIBRARY)
    # 指示待编译的子目录，子目录需要包含一个它的CMakeLists.txt文件
    add_subdirectory("./add")
    # 库自行描述了需求,故这里不再需要主动添加库头文件了.
    # set(EXTRA_INC ${EXTRA_INC} "./add")
    # 标注启用LIBRARY后的库
    set (EXTRA_LIBS ${EXTRA_LIBS} MyMathFunction)

endif(USE_LIBRARY)

# 添加映射
configure_file("config.h.in" "config.h")
# 库自行描述了需求,故这里不再需要主动添加库头文件了.(这里删除了${EXTRA_INC})
target_include_directories(HelloLibrary PUBLIC "./rst")

# 将可执行文件与静态库文件链接，静态库文件的标识符被定义在子CMakeLists.txt中
target_link_libraries(HelloLibrary PUBLIC ${EXTRA_LIBS})