import re
import os
from copy import deepcopy
from utils import *

BEGIN_INDEX = 523  # 分析开始行

with open("./ArrayList.java", "r") as file:
    LINES = [line.strip() for line in file.readlines()]


def get_func_dict():
    """
    得到函数名-起始行号和函数名-末尾行号
    判断是函数的规则是：
        行以public或private开始，以空格分割的第三项包含左括号(
        则第三项到左括号前为函数名
    寻找行末尾的方法是，找到函数名后第一个左大括号，逐行找左括号和右括号，直到配平
    """
    func2line_begin = dict()
    func2line_end = dict()
    for idx, line in enumerate(LINES):
        if line.startswith("public") or line.startswith("private"):
            line_split = line.split()
            if len(line_split) < 3:
                continue
            if "(" in line_split[2]:
                func_name = line_split[2][: line_split[2].index("(")]
                func2line_begin[func_name] = idx
                # 寻找末尾行号
                left = 0
                right = 0
                for jdx in range(idx, len(LINES)):
                    left += LINES[jdx].count("{")
                    right += LINES[jdx].count("}")
                    if left == right and left != 0:
                        func2line_end[func_name] = jdx
                        break
                else:
                    print_warning(f"func {func_name} end line find failed!")
    assert len(func2line_begin.values()) == len(
        func2line_end.values()
    ), "func2line_begin length not eq to end!"
    return func2line_begin, func2line_end


FUNC2LINE_BEGIN, FUNC2LINE_END = get_func_dict()


class LineType:
    NORMAL = 1001
    LOOP = 1002  # for and while
    BRANCH = 1003  # if
    RETURN = 1004
    FUNC = 1005


class Line:
    @classmethod
    def create_from_text(cls, line: str, line_idx):
        """
        判断每行属于哪种情况，并创建对应type的line
        Note:这里不考虑一行属于多type的情况，例如一行又是分支语句，又有函数调用，或又是循环语句，又有函数调用。
            这种情况下，分支和循环的优先级高于函数调用
        """
        type = None
        line_end = line_idx # 分支和循环可能有多条语句，需要被视为一行处理
        if line.startswith("if ("):
            type = LineType.BRANCH
        elif line.startswith("return ") or line_idx in FUNC2LINE_END.values():
            type = LineType.RETURN
        elif line.startswith("while (") or line.startswith("for ("):
            type = LineType.LOOP
        elif any(func_name in line for func_name in FUNC2LINE_BEGIN.keys()):
            type = LineType.FUNC
        else:
            type = LineType.NORMAL
        return cls(type, line, line_idx), line_end

    def __init__(self, type, line, line_idx) -> None:
        self.type = type
        self.line = line
        self.line_idx = line_idx

    @value_dispatch
    def analyze(self, path):
        print_error(
            f"Runtime Error: this line should not be exec, unexpected line type {self.type}"
        )

    @analyze.register(LineType.NORMAL)
    def _(self):
        pass

    @analyze.register(LineType.LOOP)
    def _(self):
        pass

    @analyze.register(LineType.BRANCH)
    def _(self):
        pass

    @analyze.register(LineType.RETURN)
    def _(self):
        pass

    @analyze.register(LineType.FUNC)
    def _(self):
        pass

class Path:
    def __init__(self, path) -> None:
        self.path = path

    def expand(self):
        self.path.append(self.path[-1].analyze())

def main():
    init_path = Path([Line.create_from_text(LINES[BEGIN_INDEX], BEGIN_INDEX)])
    paths = [init_path]
    while True:
        path_ptr = 0
        while path_ptr<len(paths):
            new_paths = deepcopy(paths)
            new_paths[path_ptr][-1]
            path_ptr+=1
        paths = new_paths
    pass


if __name__ == "__main__":
    main()
