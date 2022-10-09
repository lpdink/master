"""
Author: lpdink
Date: 2022-10-09 13:14:51
LastEditors: lpdink
LastEditTime: 2022-10-09 13:44:13
Description: 使用线程打印了一个等待动画，作为后面使用协程的方法的铺垫。
"""
# 这是超前的第18章asyncio的内容
# 由于项目要用，提前看一下
import threading
import itertools
import time
import sys


class Signal:
    go = True

def spin(msg, signal):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle("|/-\\"):
        status = char+" "+msg
        write(status)
        flush()
        write("\x08"*len(status))# 退格
        time.sleep(0.1)
        if not signal.go:
            break
    write(" "*len(status)+"\x08"*len(status))

def slow_func():
    time.sleep(5)
    return 42

def supervisor():
    signal = Signal()
    spinner = threading.Thread(target=spin, args=("waiting...",signal))
    spinner.start()
    slow_func()
    signal.go = False
    spinner.join()
    print("waiting done!")

if __name__=="__main__":
    supervisor()
