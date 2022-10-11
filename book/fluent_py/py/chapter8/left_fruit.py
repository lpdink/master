# 本P演示一个很隐蔽的对象不被回收的情况
# weakref.WeakKeyDictionary 的key是弱引用，需要保证key能被弱引用
# weakref.WeakValueDictionary 的value是弱引用，需要保证value能被弱引用
import weakref


class Color:
    def __init__(self, color) -> None:
        self.color = color

    def __repr__(self) -> str:
        return self.color


if __name__ == "__main__":

    fruit2id = {
        "apple": Color("red"),
        "banana": Color("yellow"),
        "peer": Color("yellow"),
        "peach": Color("pink"),
    }
    stock = weakref.WeakValueDictionary()
    for key, value in fruit2id.items():
        stock[key] = value
    print(list(stock.keys()))
    del fruit2id
    print(list(stock.keys()))
    """
    ['apple', 'banana', 'peer', 'peach']
    ['peach']
    为什么peach没有被删掉？因为for循环的key保留了对peach的引用
    """
    # 不过列表推导不会泄露变量
