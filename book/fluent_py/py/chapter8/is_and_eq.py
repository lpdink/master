# 区分is和==
# is被推荐在单例中使用
"""不能滥用is，除非你确实要比较是否是同一个对象.
>>> s=1
>>> b=1
>>> s is b
True
>>> s=114514
>>> b=114514
>>> s is b
False
"""

if __name__ == "__main__":
    my_list = [1, 2, 3]
    other_use_my_list = my_list
    other_list = [1, 2, 3]
    print(f"other_use_my_list==my_list?{other_use_my_list==my_list}")
    print(f"other_use_my_list is my_list?{other_use_my_list is my_list}")
    print(f"other_list==my_list?{other_list==my_list}")
    print(f"other_list is my_list?{other_list is my_list}")
