add_library(MyMathFunction "add.cxx")
# interface为引用本library的对象添加include，而不是本library本身
# 文档的原文描述:
# anybody linking to MathFunctions needs to include the current source directory, while MathFunctions itself doesn't. This can be expressed with an INTERFACE usage requirement. Remember INTERFACE means things that consumers require but the producer doesn't.
target_include_directories(MyMathFunction
          INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}
          )