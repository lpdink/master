"""
reduce 接受一个2参数函数，和一组序列。
对该序列中的两两元素，都执行该2参数函数.
本例演示一个手写join函数
"""
from functools import reduce

CHAR = "."


def join(a, b):
    return f"{a}{CHAR}{b}"


if __name__ == "__main__":
    print(reduce(join, range(1, 10)))
    # 当然，也可以使用Lambda表达式
    print(reduce(lambda a, b: f"{a}{CHAR}{b}", range(1, 10)))
    # 使用Join
    print(".".join([str(i) for i in range(1, 10)]))
