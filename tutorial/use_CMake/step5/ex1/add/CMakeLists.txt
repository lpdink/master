add_library(MyMathFunction "add.cxx")
# interface为引用本library的对象添加include，而不是本library本身
target_include_directories(MyMathFunction
          INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}
          )

# compiler_flags来自于主CMakeLists,这是有些耦合的.
target_link_libraries(MyMathFunction compiler_flags)

# 指定待安装的lib，
# 这里不能指定非本文件产生的compiler_flags
set(installable_libs MyMathFunction)
install(TARGETS ${installable_libs} DESTINATION lib)

# 指定待安装的头文件
install(FILES add.h DESTINATION include)