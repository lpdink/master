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

USE_SCIPY = True
try:
    from scipy import signal
except ModuleNotFoundError:
    USE_SCIPY = False

LENGTH = 1000
WIDTH = 1000
HEIGHT = 1000

INPUT_JSON = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "../resources/input.json"
)


def print_warning(msg):
    print(f"\033[33m{msg}\033[0m")


def timer(func):
    def timed_func(*args):
        start = time.time()
        rst = func(*args)
        end = time.time()
        print(f"{func.__name__} cost {(end-start)*1e3} ms")
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
        # 创建一个length*width的框
        # length*width卷积核对space卷积
        if USE_SCIPY:
            kernel = np.ones((cube.length, cube.width))
            conv2d_ = signal.convolve2d(self.space, kernel, mode="valid")
        else:
            conv2d_ = np.zeros((LENGTH - cube.length + 1, WIDTH - cube.width + 1))
            for l_index in range(conv2d_.shape[0]):
                for w_index in range(conv2d_.shape[1]):
                    conv2d_[l_index][w_index] = np.sum(
                        self.space[
                            l_index : l_index + cube.length,
                            w_index : w_index + cube.width,
                        ]
                    )
        conv2d_sort = sorted(conv2d_.flatten())
        for ker_num in conv2d_sort:
            # 找到位置
            # position = conv2d_.flatten().tolist().index(ker_num)
            position = np.where(conv2d_.reshape(-1) == ker_num)[0][0]
            l_index, w_index = (
                int(position / conv2d_.shape[1]),
                position % conv2d_.shape[1],
            )
            # 确保卷积核内的值都大于cube.height
            space_kernel = self.space[
                l_index : l_index + cube.length, w_index : w_index + cube.width
            ]
            if all((space_kernel >= cube.height).flatten()):
                space_kernel -= cube.height
                space_kernel = np.min(space_kernel)
                break
        else:
            print_warning(f"obj {cube} can't put in.")
            pass


@timer
def get_objs_from_json(json_path):
    with open(json_path, "r") as file:
        content = json.load(file)
    return np.array(content["input"])


@timer
def main():
    space = Space()
    objs = np.random.randint(1,200,(5,3))
    # objs = get_objs_from_json(INPUT_JSON)
    # breakpoint()
    # 逐个遍历输入
    all_v = 0
    for obj in objs:
        obj = sorted(obj)
        cube = Cube(*obj)
        all_v += cube.v
        space.put_in(cube)
    print(
        f"space usage:{space.usage_v} in {LENGTH*WIDTH*HEIGHT}  {space.usage_v/(LENGTH*WIDTH*HEIGHT)}%"
    )
    print(f"in all_v:{space.usage_v/all_v}%")


if __name__ == "__main__":
    # for _ in range(10):
    main()
