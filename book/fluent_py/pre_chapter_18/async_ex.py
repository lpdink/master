"""
Author: lpdink
Date: 2022-10-09 13:44:37
LastEditors: lpdink
LastEditTime: 2022-10-09 14:46:29
Description: 等待动画的协程实现，相比原书，使用await替换了yield from，使用async def 替换了@asyncio.coroutine
"""
import asyncio
import sys
import itertools

# 负责打印等待动画
async def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle("|/-\\"):
        status = f"{char} {msg}"
        write(status)
        flush()
        write("\x08" * len(status))
        try:
            await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            print("error is catched")
            break


async def slow_func():
    await asyncio.sleep(3)
    return 42


async def supervisor():
    spinner = asyncio.create_task(spin("waiting..."))
    print(f"spinner is {spinner}")
    result = await slow_func()
    spinner.cancel()
    return result


if __name__ == "__main__":
    # asyncio.run(supervisor())
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(supervisor())
    loop.close()
    print("done")
