cmake_minimum_required(VERSION 3.10)
project(HelloLibrary VERSION 1.0)

option(USE_LIBRARY "Use add in library." ON)

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

# 以创建库的形式,传入编译flags
add_library(compiler_flags INTERFACE)
target_compile_features(compiler_flags INTERFACE cxx_std_11)

# 将创建的flags库链接进来
target_link_libraries(HelloLibrary PUBLIC ${EXTRA_LIBS} compiler_flags) 

# 将可执行文件安装到bin中
install(TARGETS HelloLibrary DESTINATION bin)
# 将映射文件也安装到include中
install(FILES "./rst/config.h" DESTINATION include)
# 将编译选项库安装到lib中？
install(TARGETS compiler_flags DESTINATION lib)

# CTest将帮助我们激活测试。
# enable_testing()
include(CTest)
# 基础测试，可运行、不segfault或以其他方式崩溃，并且返回值为零
add_test(NAME Runs COMMAND HelloLibrary 1 99) 

# 使用测试properties下的PASS_REGULAR_EXPRESSION将描述打印内容是否包含字符串（正则表达式）
# 此处，我们验证99+99的结果是否包含198
add_test(NAME Usage COMMAND HelloLibrary 99 99)
set_tests_properties(Usage
  PROPERTIES PASS_REGULAR_EXPRESSION ".*198"
  )

# 可以定义一个cmake函数，来添加足够多的测试：
# 函数定义很简单function(函数名 参数列表)
function(do_test target arg1 arg2 result)
  add_test(NAME Comp${arg1}${arg2} COMMAND ${target} ${arg1} ${arg2})
  set_tests_properties(Comp${arg1}${arg2}
    PROPERTIES PASS_REGULAR_EXPRESSION ${result}
    )
endfunction()

# 调用函数以添加测试
do_test(HelloLibrary 1 98 ".*99")
do_test(HelloLibrary 200 201 ".*401")
do_test(HelloLibrary 114514 415411 ".*529925")