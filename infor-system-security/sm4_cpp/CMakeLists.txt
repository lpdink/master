# project(benchmark)
option(RELEASE_MODE "Release mode?" ON)
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

# target_include_directories(benchmark PUBLIC include)

add_library(sm4 STATIC src/sm4.cc)

# target_include_directories(sm4 PUBLIC include)

target_link_libraries(benchmark PUBLIC sm4) 