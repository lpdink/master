# CMake教程
本文是对[CMake官方阅读教程](https://cmake.org/cmake/help/latest/guide/tutorial/index.html)的中文笔记，插入笔者自己的理解与改编，尽量与官方教程在目录结构上保持一致。建议读者搭配本文，本文附带的源码，及官方文档食用。
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
有需要的读者请访问[官方教程](https://cmake.org/cmake/help/latest/guide/tutorial/Adding%20Generator%20Expressions.html#exercise-2-adding-compiler-warning-flags-with-generator-expressions)
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
