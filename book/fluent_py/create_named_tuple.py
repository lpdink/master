"""
使用具名元组，创建简单的只包含数据成员的类
"""
from collections import namedtuple

Student = namedtuple("Student", ["name", "age", "clazz", "id"])

if __name__=="__main__":
    xiaoming = Student("xiaoming", 12, 3, 20183021101203)
    print(f"{xiaoming.name} {xiaoming.age} {xiaoming.clazz} {xiaoming.id}")