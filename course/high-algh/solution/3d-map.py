"""
3D-map法，将问题空间描述为2+1数组，形如：
{
    3,4,5,6,
    7,8,8,9,
    1,2,3,4
}
第i,j位置的值表示剩余的available的高度。
对新的obj，最佳利用是保证其长与宽所在的方块的高度都相等。这样就不会出现空间空悬。
"""
import time
import json
import numpy as np
import os

LENGTH = 10000
WIDTH = 10000
HEIGHT = 10000

INPUT_JSON = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "../resources/.input.json"
)


def print_warning(msg):
    print(f"\033[33m{msg}\033[0m")


def timer(func):
    def timed_func(*args):
        start = time.time()
        rst = func(*args)
        end = time.time()
        print(f"{func.__name__} cost {(end-start)*1e3} ms", end="")
        return rst

    return timed_func


class Cube:
    def __init__(self, l, w, h) -> None:
        self._l = l
        self._w = w
        self._h = h

    def __iter__(self):
        yield from [self._l, self._w, self._h]

    def __repr__(self) -> str:
        return f"{type(self).__name__}:{tuple(self)}"

    @property
    def length(self):
        return self._l

    @property
    def width(self):
        return self._w

    @property
    def height(self):
        return self._h

    @property
    def v(self):
        return self._h * self._l * self._w


class Space:
    def __init__(self) -> None:
        self.space = np.ones((LENGTH, WIDTH), dtype=np.int32) * HEIGHT

    @property
    def available(self):
        return np.sum(self.space)

    @property
    def usage_v(self):
        return LENGTH * WIDTH * HEIGHT - self.available

    @timer
    def put_in(self, cube: Cube):
        for l_index in range(0, LENGTH-cube.length+1):
            for w_index in range(0, WIDTH-cube.width+1):
                space_kernel = self.space[
                l_index : l_index + cube.length, w_index : w_index + cube.width
                ]
                if np.all(space_kernel>cube.height):
                    space_kernel -= cube.height
                    space_kernel = np.min(space_kernel)
                    return
        print_warning(f"obj {cube} can't put in.")


@timer
def get_objs_from_json(json_path):
    with open(json_path, "r") as file:
        content = json.load(file)
    return np.array(content["input"])


@timer
def main():
    space = Space()
    # objs = np.random.randint(1,200,(5,3))
    objs = get_objs_from_json(INPUT_JSON)
    all_v = 0
    for index, obj in enumerate(objs):
        obj = sorted(obj)
        cube = Cube(*obj)
        all_v += cube.v
        space.put_in(cube)
        print(f"---->{index} in {len(objs)} {index/len(objs)}%")
    print(
        f"space usage:{space.usage_v} in {LENGTH*WIDTH*HEIGHT}  {space.usage_v/(LENGTH*WIDTH*HEIGHT)}%"
    )
    print(f"in all_v:{space.usage_v/all_v}%")


if __name__ == "__main__":
    # for _ in range(10):
    main()
