from queue import PriorityQueue, Queue
from copy import deepcopy
import json
import numpy as np
import sys

LENGTH = 1000
WIDTH = 1000
HEIGHT = 1000

INPUT_JSON = "../resources/input.json"


def print_warning(msg):
    print(f"\033[33m{msg}\033[0m")


def print_error(msg):
    print(f"\033[31m{msg}\033[0m")


class Cube:
    @classmethod
    def flow_cube(cls, l, w, h):
        return cls(None, None, None, l, w, h)

    def __init__(self, l_s, w_s, h_s, l, w, h) -> None:
        # 长宽高的起始点坐标
        self.l_s = l_s
        self.w_s = w_s
        self.h_s = h_s
        # 长宽高
        self.l = l
        self.w = w
        self.h = h

    def __iter__(self):
        # 选cube时，
        # 先定位置：优先选择远离h*w面的
        # 再定大小：优先h小的
        yield from [self.l_s, self.h_s, self.w_s, self.h, self.l, self.w]

    def __lt__(self, other):
        return tuple(self) < tuple(other)

    def __eq__(self, __o: object) -> bool:
        return tuple(self) == tuple(__o)

    def __repr__(self) -> str:
        if self.l_s is None or self.w_s is None or self.h_s is None:
            return (
                f"Flow {type(self).__name__}:(h, l, w) is ({self.h},{self.l},{self.w})"
            )
        return f"{type(self).__name__} (l_s, h_s, w_s, h, l, w) is {tuple(self)}"

    @property
    def v(self):
        return self.l * self.h * self.w

    def get_origin(self):
        return (self.l_s, self.w_s, self.h_s)

    def set_origin(self, l_s, w_s, h_s):
        self.l_s = l_s
        self.w_s = w_s
        self.h_s = h_s

    def bigger_than(self, other):
        return self.l >= other.l and self.w >= other.w and self.h >= other.h

    def put_in(self, other):
        if not self.bigger_than(other):
            print_error(f"{other} is bigger than {self}, put_in failed.")
            sys.exit(-1)
        # 放入obj的原点与当前box重合
        other.set_origin(*(self.get_origin()))
        # 假设一个obj的h>l>w, 放入obj后产生空间
        # 优先令h,l,w依次最大
        new_space = []
        if other.w < self.w:
            new_space.append(
                type(self)(
                    self.l_s,
                    self.w_s + other.w,
                    self.h_s,
                    self.l,
                    self.w - other.w,
                    self.h,
                )
            )
        if other.l < self.l:
            new_space.append(
                type(self)(
                    self.l_s + other.l,
                    self.w_s,
                    self.h_s,
                    self.l - other.l,
                    other.w,
                    self.h,
                )
            )
        if other.h < self.h:
            new_space.append(
                type(self)(
                    self.l_s,
                    self.w_s,
                    self.h_s + other.h,
                    other.l,
                    other.w,
                    self.h - other.h,
                )
            )
        return new_space


def get_objs_from_json(json_path):
    with open(json_path, "r") as file:
        content = json.load(file)
    return np.array(content["input"])


def main():
    pq = PriorityQueue()
    start = Cube(0, 0, 0, LENGTH, WIDTH, HEIGHT)
    pq.put(start)
    objs = get_objs_from_json(INPUT_JSON)
    # objs = np.array([[100,100,100]*1000]).reshape(1000, 3)
    # 逐个遍历输入
    for obj in objs:
        flow_cube = Cube.flow_cube(*obj)
        less_cubes = Queue()
        # 遍历所有的空闲空间
        while not pq.empty():
            fix_cube: Cube = pq.get()
            if fix_cube.bigger_than(flow_cube):
                new_space = fix_cube.put_in(flow_cube)
                # 放入new_space和小于的
                while not less_cubes.empty():
                    pq.put(less_cubes.get())
                for cube in new_space:
                    pq.put(cube)
                break
            else:
                less_cubes.put(fix_cube)
        else:
            # 正常遍历结束,说明没找到
            print_warning(f"obj {flow_cube} can't put in.")
            while not less_cubes.empty():
                pq.put(less_cubes.get())
    all_v = 0
    while not pq.empty():
        all_v += pq.get().v
    print(f"available v is {all_v} used {1-all_v/(WIDTH*HEIGHT*LENGTH)}")
    breakpoint()


if __name__ == "__main__":
    main()
