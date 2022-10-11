"""
    闭包允许我们将数据成员托管给函数（这本常用于类的情况）
    在不使用global时，python仍然允许我们获取或使用全局变量，个人认为这是对实现闭包特性的妥协。
    （因为这使得python变量的作用域不清晰了）

"""
"""
    一个示例：
    有avg函数，不断计算进入参数后，历史的均值：
    avg(10)->10
    avg(0)->5
    avg(1)->3
    ...
    使用类实现这样的效果是简单的
    class Avg():
        def __init__(self):
            self.history = []
        def __call__(self, value):
            self.history.append(value)
            return sum(self.history)/len(self.history)

    但可以用函数来实现同一效果
    def Avg():
        history = []
        def avg(value):
            history.append(value)
            return sum(history)/len(history)
        return avg
    avg = Avg()
    这样，history就成为了函数avg的自由变量(free variable)
    它的名称被保存在avg.__code__.co_varnames/co_freevars(分别代表local变量和本函数使用的自由变量)
    自由变量的值保存在avg.__closure__[0].cell_contents
"""
"""
    但像之前阐述的，如果你要在local作用域内修改自由变量的指向，同时企图读该自由变量，就会出问题。
    因为你将该标识符分配给局部变量了，此时就不能读。你总得舍弃一个。
    如下，就会出错，因为企图读count，且将它声明为local的了。
    def make_averager():
        count = 0
        total = 0
        def averager(new_value):
            count += 1
            total += new_value
            return total / count
            return averager
    此时，使用nonlocal，将变量声明为自由的。这很像global，但功能比global更强大。
    def make_averager():
        count = 0
        total = 0
        def averager(new_value):
            nonlocal count, total
            count += 1
            total += new_value
            return total / count
            return averager
    我认为，global是nonlocal的特殊情况，不知道这个观点是否正确？
    对于一阶函数，nonlocal与global是一致的？
    这样的设计相当诱人，但python的nonlocal关键字不允许绑定一个global作用域的变量。
    会抛出error:
    SyntaxError: no binding for nonlocal 'num' found
    这样的设计很好，很好地区分了global和nonlocal关键字的权能。
    将nonlocal用于global声明是晦涩的，出error实在太好了！
    如：
    num = 1
    def test():
        global num
        num+=1
    或者：
    num = 1
    def test():
        nonlocal num
        num+=1

    查看字节码：
    0 LOAD_GLOBAL              0 (num)
              2 LOAD_CONST               1 (1)
              4 INPLACE_ADD
              6 STORE_GLOBAL             0 (num)
              8 LOAD_CONST               0 (None)
             10 RETURN_VALUE
    ==========================
    SyntaxError: no binding for nonlocal 'num' found
"""
