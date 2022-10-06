'''
本例使用dis.dis查看函数的字节码，
以说明解释器是如何理解高层语句的。
dis标准库的文档： 
https://docs.python.org/3/library/dis.html
是开始理解Cpython的很好的切入点。

'''
# 有趣的是，本例一开始文件被命名为dis.py，这显然覆盖了标准库的import。
# 因此出现了循环import，我还思考了半天为什么...
import dis
global_num = 10
def f1(a):
    print(a)
    print(global_num)

def f2(a):
    print(a)
    print(global_num)
    global_num=2

if __name__=='__main__':
    dis.dis(f1)
    print("="*20)
    dis.dis(f2)
    '''
10           0 LOAD_GLOBAL              0 (print)
            2 LOAD_FAST                0 (a)
            4 CALL_FUNCTION            1
            6 POP_TOP

 11           8 LOAD_GLOBAL              0 (print)
             10 LOAD_GLOBAL              1 (global_num)
             12 CALL_FUNCTION            1
             14 POP_TOP
             16 LOAD_CONST               0 (None)
             18 RETURN_VALUE
====================
 14           0 LOAD_GLOBAL              0 (print)
              2 LOAD_FAST                0 (a)
              4 CALL_FUNCTION            1
              6 POP_TOP

 15           8 LOAD_GLOBAL              0 (print)
             10 LOAD_FAST                1 (global_num)
             12 CALL_FUNCTION            1
             14 POP_TOP

 16          16 LOAD_CONST               1 (2)
             18 STORE_FAST               1 (global_num)
             20 LOAD_CONST               0 (None)
             22 RETURN_VALUE
    
    
    '''
    '''
    第29和第41很好地说明了python对函数的某种编译行为。
    对于函数体来说，后面的语句是可能影响前面的语句的。（因为编译发生了）
    '''