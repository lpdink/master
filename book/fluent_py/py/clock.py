'''
    本节实现了一个简单的函数计时器，
    难得的是，它同时打印调用的函数名，参数和返回值.
'''

import time
import functools
def clock(func):
    @functools.wraps(func) # 这将func的__name__和__doc__属性复制给clocked
    def clocked(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        duration = end - start
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = [f"{k}={w}" for k, w in sorted(kwargs.items())]
            arg_lst.append(', '.join(pairs))
        arg_str = ", ".join(arg_lst)
        print(f"[{duration}s] -> {name}({arg_str})-> {result}")
        return result
    return clocked

@clock
def dotmul(A, B):
    return sum([a*b for a, b in zip(A, B)])

if __name__=="__main__":
    num = int(100000)
    A = range(-num, num)
    B = range(-num, num)
    # print(dotmul(A, B))
    dotmul(A,B)