"""
    带有参数的装饰器
    在本例中，@mark(color)，其实是先结算mark(color)得到返回值decorate只接受一个参数func，此时@decorate相当于将下面定义的函数作为func参数传入了。
    其余的与decorate.py中论述的一样
"""
GREEN = 32
RED = 31
BLUE = 34


def mark(color):
    def decorate(func):
        def make_mark(*args):
            print(f"\033[4;{color};1m func {func.__name__} is called begin\033[0m")
            rst = func(*args)
            print(f"\033[1;{color};1m func {func.__name__} is called end\033[0m")
            return rst

        return make_mark

    return decorate


"""
如果函数没有args，可以简化为2层:
def mark(color):
    def decorate(func):
        print(f"\033[4;{color};1m func {func.__name__} is called begin\033[0m")
        rst = func()
        print(f"\033[1;{color};1m func {func.__name__} is called end\033[0m")
        return rst
        return make_mark
    return decorate

这就与我们常用的工厂注册类的方法一致了.
"""


@mark(GREEN)
def add(a, b):
    return a + b


@mark(RED)
def minus(a, b):
    return a - b


@mark(BLUE)
def mul(a, b):
    return a * b


if __name__ == "__main__":
    a, b = 42, 24
    print(add(a, b), minus(a, b), mul(a, b))
