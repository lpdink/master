add_library(MyMathFunction "add.cxx")
# interface为引用本library的对象添加include，而不是本library本身
target_include_directories(MyMathFunction
          INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}
          )

# compiler_flags来自于主CMakeLists,这是有些耦合的.
target_link_libraries(MyMathFunction compiler_flags)