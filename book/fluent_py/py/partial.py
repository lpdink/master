"""
使用functiontools.partial，冻结函数参数的一部分，以提供更方便可用的函数，不必重写。
在做框架时，提供给（代码用户），还是有用的
"""
from functools import partial


def connection(addr_res, addr_dst):
    print(f"set up link between {addr_res} and {addr_dst}")


if __name__ == "__main__":
    addr_res = "127.0.0.1:8000"
    addr_dst = "127.0.0.1:8080"

    connection(addr_res, addr_dst)
    # is eq to
    connection_with_8k = partial(connection, addr_res)
    connection_with_8k(addr_dst)
