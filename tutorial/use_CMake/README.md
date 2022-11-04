# CMake教程
本文是对 [CMake官方阅读教程](https://cmake.org/cmake/help/latest/guide/tutorial/index.html) 的中文笔记，插入笔者自己的理解与改编，尽量与官方教程在目录结构上保持一致。建议读者搭配本文，本文附带的源码，及官方文档食用。
## Step0: 安装
本文基于Linux-ubuntu编写，在ubuntu上安装cmake，只需在终端键入: 
```
sudo apt-get install cmake
```
## Step1: 从基础开始
### Exercise1: 构建基础CMake工程
最简单的CMake工程包含两个文件: 一个将被编译为可执行文件的代码文件，一个CMakeLists.txt文件用于描述项目如何构建。  
尽管大小写或大小写混合的语法都被cmake接受，但推荐用小写命令。  
./step1/ex1中创建了这样的最小cmake工程:一个最简单的cxx文件，和cmake文件。  
本cmake文件遵循了这样的规则:   
- 总是以cmake_minimum_required(VERSION x.xx)开始，表示本项目构建需要的最低cmake版本。
- 以project(YourProjectName)作为你项目的开始。
- add_executable(YourProjectName src.cxx)编译一个指定项目下的可执行文件。

step1中额外包含一个shell脚本build.sh，创建构建结果与编译结果目录，执行cmake构建，并执行编译。
其中包含了cmake的构建与编译命令: 
```
# 在cmake_file_path中寻找CMakeLists.txt文件，根据规则构建，将构建结果存放到当前目录下。
cmake cmake_file_path 
# 在cmake_rst_path中寻找cmake构建文件，执行编译，将编译结果存放到当前目录。
cmake --build cmake_rst_path 
```
执行build.sh文件后，构建出的可执行文件与项目名同名(HelloWorld)，可以直接执行。
## Exercise2:指定C++标准
CMake保留了以CMAKE_开头的变量作为标识符，在创建项目时避免使用这样的命名。  
有两个这样的标识符对用户开放，CMAKE_CXX_STANDARD 和CMAKE_CXX_STANDARD_REQUIRED 现在只能推荐你一起用，以支持C++11（或其他标准）  
在project之下，add_executable之前添加:
```
set(CMAKE_CXX_STANDARD 11) # 设置C++标准为11
set(CMAKE_CXX_STANDARD_REQUIRED True) # 启用C++标准设置，与上条语句一起使用
```
有趣的是，如果你不设置这两行，C++11标准依然能使用，且生成的Makefile一模一样。(CMake Version==3.10.2)
## Exercise3: 指定项目版本
可以在CMakeLists.txt中指定项目版本，并且允许源码获取CMakeLists.txt中的宏定义。
在CMakeLists.txt中，通过: 
```
set (HelloWorld_VERSION_MAJOR 1)
```
设置变量，这些变量可以在src中，通过宏定义获取。  
在源码中定义config.h.in文件，在CMakeLists.txt中，通过: 
```
configure_file(config.h.in config.h) 
```
将.h.in文件替换为.h文件，.h文件将出现在构建结果目录中，其中被@@包围的（定义在CMakeLists.txt的）变量也会被替换。  
由于.h文件也是cmake生成的，故在include头文件时，也需要把构建目录include进去: 
```
include_directories("./rst") # 这行命令添加在编译可执行文件前
# target_include_directories(HelloWorld PUBLIC "./rst") # 如果前置target_，则添加在编译可执行文件后。
```
## Step2: 编译并使用库文件
### Exercise1: 创建库文件
本节将编译静态库并在主代码中使用它。  
创建了add子目录，子目录下包含了本静态库的所有源码文件(add.cxx)，向库外暴露的头文件(add.h)，用于编译子目录的CMakeLists.txt文件。  
在该CMakeLists.txt中，我们指定将src编译为一个库文件：
```
add_library(MyMathFunction "add.cxx")
```
add.cxx与add.h的实现十分简单，只要保证向外开放的库头文件(add.h)包含了你想向外提供的函数的信息即可。  
在最外层主目录，创建hellolibrary.cxx调用库中函数。  
外层主CMakeLists.txt的核心命令：
```
# 指示待编译的子目录，子目录需要包含一个它的CMakeLists.txt文件
add_subdirectory("./add")
# 添加可执行文件
add_executable(HelloLibrary "hellolibrary.cxx")
# 将可执行文件与静态库文件链接，静态库文件的标识符被定义在子CMakeLists.txt中
target_link_libraries(HelloLibrary PUBLIC MyMathFunction)
# 指示暴露出的库的头文件路径
target_include_directories(HelloLibrary PUBLIC "./add")
```
可以说，这四句命令都必不可少。  
同上，target_开头的命令需要出现在构建可执行文件的命令之后。  
## Exercise2: 将库文件设置为可选的
场景是：如果你有一个本地实现的库函数，和一个引入的库函数，希望通过cmake决定用哪个。  
需要搭配step1-ex3的config映射来使用，cmake提供了简单的分支语句和追加变量的语法，可以达到我们的目的。  
```
# 全局唯一控制是否使用库文件选项
option(USE_LIBRARY "Use add in library." OFF)

# 让分支语句包裹添加库文件需要的命令。
if(USE_LIBRARY)
    add_subdirectory("./add")
    set(EXTRA_INC ${EXTRA_INC} "./add")
    set (EXTRA_LIBS ${EXTRA_LIBS} MyMathFunction)
endif(USE_LIBRARY)

# 将分支中追加的EXTRA参数追加到头文件设置和库文件链接中
target_include_directories(HelloLibrary PUBLIC "./rst" ${EXTRA_INC})
target_link_libraries(HelloLibrary PUBLIC ${EXTRA_LIBS})
```
如果不使用库文件，但是代码中却调用了同名函数，这显然就要求我们本地实现。  
因此，需要将USE_LIBRARY传入src中。方法同step1-ex3，使用config映射
```
configure_file("config.h.in" "config.h")
```
在in文件中配置:
```
#cmakedefine USE_LIBRARY 
//这很可能又是一个语法糖，实际上等于
//#define USE_LIBRARY @USE_LIBRARY@
```
之后，在src的源码中就可以决定是本地实现，还是使用库文件了:
```
#ifdef USE_LIBRARY
#include "add.h"
#else
int myadd(int a, int b){
    return int((a+b)*100);
}
#endif
```
## Step3: 为Library添加使用需求
让Library自己描述自己的使用需求，调用方只需要简单地链接这个库就可以了。  
达到这一目的，需要做到：任何试图使用库Library的CMakeLists，都必须将库的头文件include进来。除了库Library本身。  
这需要在Library的CMakeLists.txt中添加:
```
target_include_directories(MyMathFunction
          INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}
          )
```
interface为引用本library的对象添加include，而不是本library本身.  
这样,我们就能删除step2-ex2中include add的命令了.这就构成了step3.  
## Step4: 添加生成器表达式
### Exercise1: 让CMakeLists之间共享编译选项
在主CMakeLists中创建一个额外的interface库,用于传递编译选项,需要使用该选项的库,只需要将interface库链接进来即可.
```
# 以创建库的形式,传入编译flags
add_library(compiler_flags INTERFACE)
target_compile_features(compiler_flags INTERFACE cxx_std_11)
```
我们让add库使用这个编译选项(使用C++11标准),修改它的CMakeLists,将库链接进来.
```
# compiler_flags来自于主CMakeLists,这是有些耦合的.
target_link_libraries(MyMathFunction compiler_flags)
```
由于它是被调用方,所以compiler_flags来自于调用方,这很合理.  
### Exercise2: 使用生成器表达式添加编译选项
本节需要CMake3.15, 超出了笔者正在使用的3.10，本节略去.  
有需要的读者请访问 [官方教程](https://cmake.org/cmake/help/latest/guide/tutorial/Adding%20Generator%20Expressions.html#exercise-2-adding-compiler-warning-flags-with-generator-expressions) 
## Step5: 安装与测试
### Exercise1: 安装规则
通常，仅构建可执行文件是不够的，它还应该是可安装的。使用 CMake，我们可以使用 install() 命令指定安装规则。  
接下来，我们通过安装命令：
- 将使用的库文件安装到lib目录下。
- 将库文件的头文件安装到include目录下。
- 将可执行文件安装到bin目录下。
- 映射头文件config.h也应该放置在include目录下。
install命令看上去只在执行copy一样，命令十分简单：
```
# 如果是编译产物，第一个参数用TARGETS
install(TARGETS HelloLibrary DESTINATION bin)
# 如果是文件，第一个参数用FILES
install(FILES "./rst/config.h" DESTINATION include)
# 在库内部指定库自己的安装位置，在主文件指定bin文件的安装位置
# 即谁生产，谁负责（安装）
```
参考step5，完成头文件，库文件，bin文件，interface库文件的安装后，在build.sh目录中追加了安装命令：
```
# 安装。这里通过DESTDIR="../install_rst"指定了安装路径。
## 毕竟是测试工程，不便安装到/use/bin下。
make install DESTDIR="../install_rst"
```
这一命令是在编译结果同级目录(rst)执行的。如果cmake版本大于3.15，则可以使用：
```
cmake --install .
```
### Exercise2: 测试支持
使用cmake添加测试，首先在CMakeLists.txt文件中enable测试
```
enable_testing()
```
进行测试有两个关键：
- 执行测试的命令
- 校验程序输出结果是否正确。
```
# 添加测试，NAME和COMMAND是保留字，Usage是本测试名，任意取。COMMAND后面是执行测试的命令。
# 测试往往是对bin文件进行的，只要是本cmake文件编译出的target，就不用进行路径配置。
add_test(NAME Usage COMMAND HelloLibrary 99 99)


# 为Usage测试校验结果，PASS_REGULAR_EXPRESSION表明进行正则表达式校验，检验程序的命令行打印是否包含后面的正则表达式。
set_tests_properties(Usage
  PROPERTIES PASS_REGULAR_EXPRESSION ".*198"
  )
```
可以定义函数以快速地添加测试，本节也引入在cmake中定义函数的方法：
```
# 函数定义很简单function(函数名 参数列表)
function(do_test target arg1 arg2 result)
  add_test(NAME Comp${arg1}${arg2} COMMAND ${target} ${arg1} ${arg2})
  set_tests_properties(Comp${arg1}${arg2}
    PROPERTIES PASS_REGULAR_EXPRESSION ${result}
    )
endfunction()
```
这样，就能通过调用函数来快速地添加测试了。
```
do_test(HelloLibrary 1 98 ".*99")
do_test(HelloLibrary 200 201 ".*401")
do_test(HelloLibrary 114514 415411 ".*529925")
```
## Step6: 添加周期测试并转发结果
即daily test，通过在CTestConfig.cmake中配置每日执行测试的时间，测试结果上传的url，就能定期执行测试，并将结果发送到URL。  
在顶层CMakeLists.txt中添加：
```
include(CTest)
```
在项目顶层CMakeLists.txt同级创建CTestConfig.cmake，填写：
```
set(CTEST_PROJECT_NAME "CMakeTutorial")
set(CTEST_NIGHTLY_START_TIME "00:00:00 EST")

set(CTEST_DROP_METHOD "http")
set(CTEST_DROP_SITE "my.cdash.org")
set(CTEST_DROP_LOCATION "/submit.php?project=CMakeTutorial")
set(CTEST_DROP_SITE_CDASH TRUE)
```
完成配置。my.cdash.org是某个开放的供给提交测试的网站。  
如果想立即执行测试，可以编译二进制文件后执行：
```
ctest -D Experimental
```
这也会上传测试结果。  
但感觉cmake提供daily test不是很有用，多数情况下，只有大型工程需要daily test，但真正由企业主导的大型工程往往又有自己的工具。  
## Step7: 添加系统内省
这将根据目标系统是否包含我们想要使用的特定函数，来决定**编译**行为。（即是否使用替代函数）  
这对跨平台情况当然是有用的，但也很难说很有用，跨平台的交叉编译常出现在嵌入式设备上，但你不会希望在家里的微波炉上编译让它唱歌的程序。  
更常见的情况是，使用交叉编译工具链，在x86上编译微波炉能执行的程序。
感兴趣的读者请访问 [官方文档](https://cmake.org/cmake/help/latest/guide/tutorial/Adding%20System%20Introspection.html)
## Step8: 添加自定义命令和生成的文件
TODO
## Step9: 使用CPack打包一个installer.
TODO
## Step10: 使用动态链接库
本节的官方教程显得费解，故笔者在这里独立于教程提供一个使用动态库的良好实践。  
本节的目标是编译并使用动态链接库，同时编译产生同名静态库。保证动态库和静态库，在第三方得到头文件和库文件后可以直接使用。  
### 编译动态链接库
编译动态库与静态库的方法一致，都是通过add_library方法：
```
add_library(<name> [STATIC | SHARED | MODULE]
            [EXCLUDE_FROM_ALL]
            [<source>...])
```
注意STATIC/SHARED需要大写。  
我们创建一个make_lib目录，用于编译库文件，一个main目录，用于调用生成的库文件，两者的编译是分开的。  
在make_lib下，我们要同时编译同名的动态库和静态库，但不能简单通过add_library达成，此时只会产生动态库，不会生成静态库。需要先编译成别名静态库，再通过property改名。  
```
add_library(own_math SHARED ${LIBOWN_MATH_SRC})

# 不能直接通过add_library创建同名静态库，会只编译动态库出来
# 因此，先创建一个别名静态库，再将输出名更改为同名的
add_library(own_math_static STATIC ${LIBOWN_MATH_SRC})
# 内置属性是需要大写的,(命令是大小写都可以的),包括PROPERTIES, OUTPUT_NAME, STATIC/SHARED等等
set_target_properties(own_math_static PROPERTIES OUTPUT_NAME own_math)
```
这样，就能同时编译产生静态和动态库了。
### 初探编译选项
我们根据不同的编译模式，选择添加不同的编译选项。  
这里采用一个option来选择编译模式，在Release下使用O3，Debug下使用O0, g和ggdb。  
> 我不确定-g和-ggdb是否一起使用，我不明白他们具体在做什么工作。编译选项就是这样，你可以多加，但是最好不要少加。

> Release下，编译器也不会主动为你选择O3的，O3优化并不总令程序变快，O2反而是开发人员对齐的标准。编译器的编写者不会主动做他们不100%肯定的事，所以锅都得我们来背。

> 但我很信任O3，所以这里加上了。在生产环境下，建议O3一版，O2一版，Os一版，让测试同学跑一版速度测试，然后问问下游部门接受哪个。

这里只为CXX添加了编译选项，如果你有C代码，记得给C_FLAGS也添加选项。  
add_compile_options则作用于所有类型的代码。-fPIC使得动态库使用动态地址，这样它可以被其他人重用了，但也有被未授权第三方重用的风险。  
> 没有-fPIC时默认使用静态地址，盲猜是一种控制流完整性策略。

你几乎总应该开启-Wall -Wextra，他们没什么损失，而且会告诉你warning。
```
option(RELEASE_MODE "Release mode?" ON)
if(RELEASE_MODE)
    set(CMAKE_BUILD_TYPE "Release")
    set(CMAKE_CXX_FLAGS "-O3")
else()
    set(CMAKE_BUILD_TYPE "Debug")
    set(CMAKE_CXX_FLAGS "-g -ggdb -O0")
endif(RELEASE_MODE)
# -fPIC是共享库必须的，让共享库使用任意地址而不是固定地址 ## 这会允许恶意重用
# 注意，这里不能用""包裹三个选项，这会让cmake把三个选项认为是一个.
add_compile_options(-fPIC -Wall -Wextra)
```
### 编译选项的影响
这里在Release和Debug模式下分别编译动态库和静态库，查看其外存大小。

| 模式\库 | a库 | so库 |
| ----| ---- | ---- | 
| Debug | 3784 | 8912 |
| Debug-Strip| 996 | 5760 |
| Release | 1680  | 7544 |
| Release-Strip | 908 | 5760 |
> 在release模式下尝试了O3，O2与Os三种优化，结果都是一致的。  

> 对动态库，Debug和Release的剪裁结果一样，应该是由于我们的代码太简单，没有优化余地导致的。

Strip和Release对空间的减小都是必须的。但Strip -D是有风险的优化，有可能导致动态链接库无法被链接到，因此编译器的作者不会主动为你做这样的工作。他们优先考虑可用性。  
> 所以锅得你来背，在发布上线前，记得strip，并测试保证程序没问题。
### 引用动态链接库
引用第三方库需要三个部分:
- 通过link_directories指定库文件路径。
- 通过target_include_directories引用第三方库头文件。
- 通过target_link_libraries将库链接进来。
```
# NOTE:指定链接库路径，需要出现在add_executable之前
link_directories("./lib")

add_executable(main main.cxx)

target_include_directories(main PUBLIC "./include")
target_link_libraries(main PUBLIC own_math)
```
TODO: 动态库与静态库的优先级