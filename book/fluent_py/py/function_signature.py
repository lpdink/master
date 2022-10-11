"""
函数内省
用inspect.signature来查看函数的参数及返回值情况，以便使用函数去操作函数
"""
from inspect import signature


def func_test(a, b, c=1):
    print(f"in func test, with args:{a}{b}{c}")


if __name__ == "__main__":
    print(signature(func_test))
    print(str(signature(func_test)))
    for name, param in signature(func_test).parameters.items():
        print(param.kind, name, param.default)
    """
    (a, b, c=1)
    (a, b, c=1)
    POSITIONAL_OR_KEYWORD a <class 'inspect._empty'>
    POSITIONAL_OR_KEYWORD b <class 'inspect._empty'>
    POSITIONAL_OR_KEYWORD c 1
    """
    # 使用sig的Bind方法去尝试函数调用是否能够成功
    sig = signature(func_test)
    args = {"b": 2}
    sig.bind(**args)
