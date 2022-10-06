'''
使用global函数获取上下文的变量定义信息吧~
在pdb里尤其有用。可以看到哪些变量是我们可以查看的。之后对这些变量使用dir方法，查看他们的属性和方法吧~
'''
from collections import namedtuple
class Myclass:
    def __init__(self) -> None:
        self.name="name"
        self.age = "age"

Same2Student = namedtuple("Student",["name", "id", "age"])

if __name__=="__main__":
    num = 1
    nums = range(3)
    student = Same2Student("xiaoming", "1001", 12)
    clazz = Myclass()
    print(globals())
    breakpoint()
    '''
    {'__name__': '__main__', '__doc__': '\n使用global函数获取上下文的变量定义信息吧~\n在pdb里尤其有用。\n', '__package__': None, '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x7f204572bc10>, '__spec__': None, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>, '__file__': 'Your script Path, '__cached__': None, 'namedtuple': <function namedtuple at 0x7f20444ad940>, 'Myclass': <class '__main__.Myclass'>, 'Same2Student': <class '__main__.Student'>, 'num': 1, 'nums': range(0, 3), 'student': Student(name='xiaoming', id='1001', age=12), 'clazz': <__main__.Myclass object at 0x7f204442e520>}
    '''