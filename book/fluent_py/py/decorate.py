"""
开始使用装饰器,本例将说明装饰语句，和装饰函数的调用的区别。
"""
import traceback
import time

# 装饰器在装饰时(即@调用时)被立即执行
# 完成对函数的装饰（注意不是执行被装饰的函数）
def timer(func):
    # 在这里打印堆栈，以说明装饰器在装饰时立即执行。
    traceback.print_stack()
    print("=" * 50)

    def timed_func(*args):
        # 在这里打印堆栈，以说明装饰好的函数在被调用时才被调用。
        traceback.print_stack()
        start = time.time()
        rst = func(*args)
        end = time.time()
        print(f"cost {(end-start)*1e3} ms")
        return rst

    return timed_func


@timer
def dotmul(A, B):
    return sum([a * b for a, b in zip(A, B)])


if __name__ == "__main__":
    num = int(1e5)
    A = range(-num, num)
    B = range(-num, num)
    rst = dotmul(A, B)
    print(f"the result is {rst}")
    """结果:
File ".../fluent_py/decorate.py", line 23, in <module>
def dotmul(A, B):
File ".../fluent_py/decorate.py", line 10, in timer
traceback.print_stack()
==================================================
File ".../fluent_py/decorate.py", line 30, in <module>
rst = dotmul(A, B)
File ".../fluent_py/decorate.py", line 14, in timed_func
traceback.print_stack()
cost 50.63223838806152 ms
the result is 666666666700000
    
    """
    """
    因此，可以看到，装饰行为是在23行执行的，@timer的位置
    而装饰好的函数是在实际调用时执行的，即30行。
    @是一个语法糖：
        @decorate
        def function(...)
        等同于
        function = decorate(function)
    """
