"""
Description: Astar算法解决迷宫问题
"""
from queue import PriorityQueue
from copy import deepcopy


def read_space():
    with open("space.txt", "r") as file:
        lines = file.readlines()
    SPACE = [line.strip().split() for line in lines]
    for line_index, line in enumerate(SPACE):
        try:
            col_index = line.index("2")
            START = (line_index, col_index)
        except:
            pass
        try:
            col_index = line.index("3")
            END = (line_index, col_index)
        except:
            pass
    if "START" in dir() and "END" in dir():
        return SPACE, START, END
    else:
        print("can't find origin 2 or end 3 in space.txt")
        exit()


SPACE, START, END = read_space()


class Node:
    def __init__(self, x, y, father=None, depth=0, show_char="S") -> None:
        self._x = x
        self._y = y
        self.depth = depth
        self.cost = self.get_cost()
        self.father = father
        self.show_char = show_char

    # 添加x和y的getter，以向User传递不希望_x和_y被修改的信息。
    # _x与_y不应该被修改，因为对象的__hash__依赖于这两个属性
    # 但是可hash的对象，一经创建，其hash绝不应该变化.
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def _hmd(self, dst):
        return abs(self.x - dst[0]) + abs(self.y - dst[1])

    def get_cost(self):
        return 2 * self._hmd(END) + self._hmd(START) + self.depth

    def _pos_is_valid(self, x, y):
        return not SPACE[x][y] == "1"

    def transfer(self):
        rst = []
        if self.x >= 1 and self._pos_is_valid(self.x - 1, self.y):
            rst.append(Node(self.x - 1, self.y, self, self.depth + 1, "↑"))
        if self.y >= 1 and self._pos_is_valid(self.x, self.y - 1):
            rst.append(Node(self.x, self.y - 1, self, self.depth + 1, "←"))
        if self.y < len(SPACE[0]) - 1 and self._pos_is_valid(self.x, self.y + 1):
            rst.append(Node(self.x, self.y + 1, self, self.depth + 1, "→"))
        if self.x < len(SPACE) - 1 and self._pos_is_valid(self.x + 1, self.y):
            rst.append(Node(self.x + 1, self.y, self, self.depth + 1, "↓"))
        return rst

    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y

    def __getitem__(self, index):
        return [self.cost, self.x, self.y, self.father][index]

    def __lt__(self, __o: object) -> bool:
        return self.cost < __o.cost

    def __repr__(self) -> str:
        return f"cost:{self.cost} x:{self.x} y:{self.y} father:{self.father}"

    def __hash__(self) -> int:
        # ^: 异或
        # 这一哈希函数也是可用的。但交换xy的顺序会产生相同的哈希。
        # 不同对象有相同的哈希，即产生哈希碰撞，会导致性能的降低，但不导致两个对象的id相同，或是eq。
        # 因而也不会在字典中被认为是同一个key。
        # return hash(self.x)^hash(self.y)
        # 一个更好的方案是：
        # return hash(tuple(self.x, self.y))
        return int(self.x * 1e9 + self.y)


def astar():
    closed = set()
    start, end = Node(*START), Node(*END)
    open = PriorityQueue()
    open.put(start)
    while not open.empty():
        now: Node = open.get()
        if now == end:
            return now
        # 考察now节点，未考察的子节点加入open表中
        for sub_node in now.transfer():
            if sub_node not in closed:
                open.put(sub_node)
        closed.add(now)
    else:
        print("can't find solution, check the space.")
        exit()


if __name__ == "__main__":
    end = astar()
    path = []
    tmp = end
    while tmp.father is not None:
        path.append(tmp)
        tmp = tmp.father
    # 根据path修改SPACE
    ret = deepcopy(SPACE)
    for node in path:
        ret[node.x][node.y] = node.show_char
    for line in ret:
        print(" ".join(line))
