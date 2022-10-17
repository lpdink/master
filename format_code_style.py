# 用black格式化代码
import os


def find_all_py(path, dst):
    files = [os.path.join(path, file) for file in os.listdir(path)]
    for file in files:
        if os.path.isdir(file):
            find_all_py(file, dst)
        elif file.endswith(".py"):
            dst.append(file)


if __name__ == "__main__":
    py_files = []
    base = os.path.realpath("./")
    find_all_py(base, py_files)
    py_files = " ".join(py_files)
    os.system(f"black {py_files}")
