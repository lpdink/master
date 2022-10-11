# 本P说明了python垃圾回收的机制
# del something实际上在删除"something"标识符对对象的引用
# 某一对象不存在引用，或只存在循环引用时，cpython回收该对象。
import weakref

class Tese:
    def __init__(self):
        self.addr1 = 1
        self.addr2 = 2
        self.addr3 = [1, 2, 3]
        addr4 = 4
        
    def method(self):
        print("test.method is called")

    def close(self):
        del self

if __name__=="__main__":
    test = Tese() # 对对象强引用
    test_weak_ref = weakref.ref(test) # 对象弱引用，可以通过test_weak_ref()获取对象（如果它alive）
    method = test.method # 对对象的成员函数强引用
    method_weak_ref = weakref.ref(method) # 对函数弱引用
    test.method()
    funcs1 = dir(test) # dir出来的list是独立的。
    test.close() # 无效的。在close内的del self，只在作用域内删除了self对对象的引用。
    funcs2 = dir(test)
    test.method() # 正常调用,说明test.close()无效
    print(f"funcs1 is funcs2? {funcs1 is funcs2} funcs1==funcs2?{funcs1==funcs2}") # False，两个list是独立的
    print(f"test's obj is dead?(before del test): {test_weak_ref() is None}")
    del test # 这里删除了test对对象的引用，但是test此前指向的对象没有被回收，因为对方法的强引用method依然存在
    print(f"test's obj is dead?(after del test): {test_weak_ref() is None}")# False，test's obj没有被回收
    del method
    print(f"test's obj is dead?(after del method): {test_weak_ref() is None}")# True,删除方法后，obj被回收了。可见对于集合对象，如果集合内的任何一个对象没被回收，集合就不会被回收。
    print(funcs1, funcs2) # 正常打印了，dir出来的列表不依赖于对象。
    '''
    est.method is called
    test.method is called
    funcs1 is funcs2? False funcs1==funcs2?True
    test's obj is dead?(before del test): False
    test's obj is dead?(after del test): False
    test's obj is dead?(after del method): True
    '''