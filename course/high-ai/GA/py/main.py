import sys
import os
import numpy as np
import matplotlib.pylab as plt

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import config


def score_function(x):
    return 10 * np.sin(5 * x) + 7 * abs(x - 5) + 10


def binary2decimal(pop):
    # 每行py个数，转为二进制
    _, py = pop.shape
    mask = np.array([np.power(2, py - index) for index in range(1, py + 1)])
    rst = np.sum(pop * mask, axis=1)
    return rst * 10 / np.sum(mask)


def initpop(popsize, chromlength):
    pop = np.random.randint(0, 2, (popsize, chromlength))
    return pop


def cal_objvalue(pop):
    x = binary2decimal(pop)
    return score_function(x)


def selection(old_pop, fitvalue):
    px, _ = old_pop.shape
    total_fit = np.sum(fitvalue)
    p_fitvalue = fitvalue / total_fit
    p_fitvalue = np.cumsum(p_fitvalue)
    ms = np.sort(np.random.rand(px))
    fitin, newin = 0, 0
    new_pop = np.zeros_like(old_pop)
    while newin < px:
        if ms[newin] < p_fitvalue[fitin]:
            new_pop[newin] = old_pop[fitin, :]
            newin += 1
        else:
            fitin += 1
    return new_pop


def crossover(old_pop, pc):
    px, py = old_pop.shape
    new_pop = np.ones_like(old_pop)
    for i in range(0, px, 2):
        if np.random.rand() < pc:
            cpoint = np.random.randint(1, py, 1)[0]
            new_pop[i] = list(old_pop[i, :cpoint]) + list(old_pop[i + 1, cpoint:])
            new_pop[i + 1] = list(old_pop[i + 1, :cpoint]) + list(old_pop[i, cpoint:])
        else:
            new_pop[i] = old_pop[i, :]
            new_pop[i + 1] = old_pop[i + 1, :]
    return new_pop


def mutation(old_pop, pm):
    px, py = old_pop.shape
    new_pop = np.ones_like(old_pop)
    for i in range(px):
        if np.random.rand() < pm:
            # 随机选一个点变异
            mpoint = np.random.randint(0, py, 1)[0]
            new_pop[i] = old_pop[i, :]
            new_pop[i, mpoint] ^= 1
        else:
            new_pop[i] = old_pop[i, :]

    return new_pop


def best(pop, fitvalue):
    max_index = fitvalue.argmax()
    return pop[max_index], fitvalue[max_index]


def main():
    pop = initpop(config.popsize, config.chromlength)
    for i in range(config.loops):
        objvalue = cal_objvalue(pop)
        # breakpoint()
        fitvalue = objvalue
        newpop = selection(pop, fitvalue)
        newpop = crossover(newpop, config.pc)
        newpop = mutation(newpop, config.pm)
        pop = newpop
    bestindividual, bestfit = best(pop, cal_objvalue(pop))
    x2 = binary2decimal(bestindividual.reshape((1, -1)))
    x1 = binary2decimal(pop)
    y1 = cal_objvalue(pop)
    # 目标函数曲线
    true_x = np.linspace(0, 10, 1000)
    true_y = score_function(true_x)
    plt.plot(true_x, true_y)
    plt.scatter(x1[:10], y1[:10], color="green", marker="d")
    plt.scatter(x2[0], bestfit, color="red", marker="*")
    plt.savefig("result.png")
    print(f"predict max:{bestfit}, true max is {np.max(true_y)}")

    # breakpoint(x2[0], bestfit)


if __name__ == "__main__":
    main()
