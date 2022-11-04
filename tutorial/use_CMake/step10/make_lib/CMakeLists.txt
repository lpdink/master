cmake_minimum_required(VERSION 3.10)

option(RELEASE_MODE "Release mode?" ON)
if(RELEASE_MODE)
    set(CMAKE_BUILD_TYPE "Release")
    set(CMAKE_CXX_FLAGS "-O2")
else()
    set(CMAKE_BUILD_TYPE "Debug")
    set(CMAKE_CXX_FLAGS "-g -ggdb -O0")
endif(RELEASE_MODE)
# -fPIC是共享库必须的，让共享库使用任意地址而不是固定地址 ## 这会允许恶意重用
# 注意，这里不能用""包裹三个选项，这会让cmake把三个选项认为是一个.
add_compile_options(-fPIC -Wall -Wextra)

message(">>>>>>CMAKE using CXX flags: ${CMAKE_CXX_FLAGS} in ${CMAKE_BUILD_TYPE}")
message(">>>>>>CMAKE using C flags: ${CMAKE_C_FLAGS} in ${CMAKE_BUILD_TYPE}")
# 1.8K Nov  4 08:15 libown_math.a
# -rwxrwxr-x 1 ubuntu ubuntu 5.7K Nov  4 08:35 libown_math.so

set(LIBOWN_MATH_SRC "own_math.cxx")
# 构建动态库
add_library(own_math SHARED ${LIBOWN_MATH_SRC})

# 不能直接通过add_library创建同名静态库，会只编译动态库出来
# 因此，先创建一个别名静态库，再将输出名更改为同名的
add_library(own_math_static STATIC ${LIBOWN_MATH_SRC})
# 内置属性是需要大写的,包括PROPERTIES, OUTPUT_NAME, STATIC/SHARED等等
set_target_properties(own_math_static PROPERTIES OUTPUT_NAME own_math)

# 安装
install(TARGETS own_math DESTINATION lib)
install(TARGETS own_math_static DESTINATION lib)
install(FILES own_math.h DESTINATION include)