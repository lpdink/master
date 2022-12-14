"""
    lru_cache是这样的装饰器：
        用于多次以相同参数调用的，计算时间较长的函数。
        lru_cache将会散列{args:result}，以避免多次计算相同的函数.
"""
from functools import lru_cache
from clock import clock


@clock
@lru_cache()
def dotmul(A, B):
    return sum([a * b for a, b in zip(A, B)])


if __name__ == "__main__":
    num = int(1e7)
    A = range(-num, num)
    B = range(-num, num)
    for i in range(5):
        dotmul(A, B)
        print("=" * 50)
    """
    可以看到，只有第一次实际计算了，用了3.5S，其余都是在访问缓存。
    lru_cache应该实现了多级缓存，第三次访问比第二次访问更快一个数量级。
    [3.54046649672091s] -> dotmul(range(-10000000, 10000000), range(-10000000, 10000000))-> 666666666666670000000
==================================================
[3.034248948097229e-06s] -> dotmul(range(-10000000, 10000000), range(-10000000, 10000000))-> 666666666666670000000
==================================================
[6.891787052154541e-07s] -> dotmul(range(-10000000, 10000000), range(-10000000, 10000000))-> 666666666666670000000
==================================================
[6.426125764846802e-07s] -> dotmul(range(-10000000, 10000000), range(-10000000, 10000000))-> 666666666666670000000
==================================================
[6.388872861862183e-07s] -> dotmul(range(-10000000, 10000000), range(-10000000, 10000000))-> 666666666666670000000
==================================================
    """
