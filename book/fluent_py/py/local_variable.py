"""
    本例描述了python的变量作用域，及global关键词的使用场景。
    例子中的local_function可以正常执行，但去除修改变量global_num一行的注释后，不再能正常执行了。且出错是在此前的行。
    说明了python中的函数不是简单的“放函数签名进堆栈，执行时调用”
    而存在某种编译过程。
    这点很反直觉，一般我们都认为py是逐行的脚本语言的
"""
global_num = 10


def local_function(local_param):
    print("local_function is called")
    print(local_param)
    print(global_num)
    # without # line 15 will throw error.UnboundLocalError: local variable 'global_num' referenced before assignment
    global_num = 11


local_function(-99)
"""
此时，global关键词会有帮助，对global_num做global声明，就不会报错了，且允许你在函数体内修改全局变量。
def local_function(local_param):
    print("local_function is called")
    global global_num
    print(local_param)
    print(global_num)
    global_num=11
这个关键词极少被使用，也完全不推荐使用，因为它破坏了模块的封闭性。
"""
