'''
    functools.singledispatch
    本装饰器用于根据第一个参数的type，应用不同行为的场景。
    是对if/else组的解耦。
    一个好的建议是，注册的函数处理抽象基类，如numbers.Integral，而不是具体实现int
'''
'''
本例演示一个正则化程序，
    对数字，转化为对应汉字。
    对列表/元组，转换为字符串
    对自定义类型，返回自定义类型的某一属性
'''
from functools import singledispatch
import numbers
from collections import abc


class MyType():
    def __init__(self, attr) -> None:
        self.attr = attr

    def __repr__(self) -> str:
        return "MyType"

@singledispatch
def normalize(obj):
    # 兜底方案
    return f"--->{obj}<---"

@normalize.register(str)
def _(obj):
    return f"str({obj})"

@normalize.register(numbers.Integral)
def _(obj):
    hanz = [char for char in "零一二三四五六七八九十"]
    dic = {str(index):value for index, value in enumerate(hanz)}
    return "".join([dic[char] for char in str(obj)])

# abc.MutableSequence指一切可变序列
@normalize.register(abc.MutableSequence)
@normalize.register(tuple)
def _(obj):
    return "".join([str(item) for item in obj])

@normalize.register(MyType)
def _(obj):
    return f"{obj.attr} in {obj}"

if __name__=="__main__":
    res = [123906, "test", [984,66,"sda"], (123,"tuple"), MyType("attr_instance"), {"key":"value"}]
    for item in res:
        print(normalize(item))
    """输出结果：
        一二三九零六
        str(test)
        98466sda
        123tuple
        attr_instance in MyType
        --->{'key': 'value'}<---
    这样就完成了解耦。
    """