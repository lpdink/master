cmake_minimum_required(VERSION 3.2)
project(sm4_cxx)
option(RELEASE_MODE "Release mode?" OFF)
if(RELEASE_MODE)
    set(CMAKE_BUILD_TYPE "Release")
    set(CMAKE_CXX_FLAGS "-O3")
else()
    set(CMAKE_BUILD_TYPE "Debug")
    set(CMAKE_CXX_FLAGS "-g -ggdb -O0")
endif(RELEASE_MODE)
add_compile_options(-fPIC -Wall -Wextra)

include_directories(include)
add_executable(benchmark src/benchmark.cc)

add_executable(sm4_bin src/bin.cc)
set_target_properties(sm4_bin PROPERTIES OUTPUT_NAME sm4)

add_library(sm4 STATIC src/sm4.cc src/core.cc)

target_link_libraries(benchmark PUBLIC sm4) 
target_link_libraries(sm4_bin PUBLIC sm4) 