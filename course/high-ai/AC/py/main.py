from utils import config,abs_distance,get_path_length
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

FILE_PATH = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "../resources/space.txt")


def read_space():
    with open(FILE_PATH, "r") as file:
        lines = file.readlines()
    SPACE = np.array([line.strip().split() for line in lines], dtype=np.int32)
    assert len(np.where(SPACE == 2)[0]) == 1, "space should have only one '2'!"
    assert len(np.where(SPACE == 3)[0]) == 1, "space should have only one '3'!"
    # 返回的是SPACE, START, END
    # START和END是数字2和3的索引
    return SPACE, (np.where(SPACE == 2)[0][0], np.where(SPACE == 2)[1][0]), (np.where(SPACE == 3)[0][0], np.where(SPACE == 3)[1][0])


SPACE, START, END = read_space()
# 初始化信息素矩阵
tau = np.ones_like(SPACE, dtype=np.float32)*8
# 下一轮要增加的信息素
next_tau_plus = np.ones_like(tau)

class Ant:
    def __init__(self, pos) -> None:
        self.pos = pos
        self.path = [pos]
        # 禁忌表
        self.tabu_km = deepcopy(SPACE)

    def move(self):
        # 蚂蚁移动一步,允许斜走，8种可能的移动方法
        possible_next_pos = []
        for idx in range(1, -2, -1):
            for jdx in range(1, -2, -1):
                # 不允许不移动
                if idx==0 and jdx==0:
                    continue
                # 可能的移动位置
                new_x = self.pos[0]+idx
                new_y = self.pos[1]+jdx
                # 不能超出SPACE范围
                if new_x<0 or new_y<0 or new_x>=len(SPACE) or new_y>=len(SPACE[0]):
                    continue
                # 查询禁忌表,1不可走
                if int(self.tabu_km[new_x][new_y])!=1:
                    possible_next_pos.append((new_x, new_y))
        if len(possible_next_pos)==0:
            return None, False
        # 根据启发式信息和信息素进行轮盘赌，决定下一步
        scores = []
        for next_pos in possible_next_pos:
            new_x, new_y = next_pos
            # alpha: 信息素重要程度，beta:启发式信息重要程度
            # 这里的启发式信息取当前点到目标点的直线距离的倒数
            dis_score = 1/abs_distance((new_x, new_y), (END[0], END[1])) if next_pos !=END else 100
            score = (tau[new_x, new_y]**config.Alpha)*(dis_score**config.Beta)
            scores.append(score)
        # 对得分归一化
        scores = np.array(scores)/np.sum(scores)
        # 累计求和
        score_ranges = np.cumsum(scores)
        rand_num = np.random.rand()
        select_idx = 0
        for idx, score_range in enumerate(score_ranges):
            if score_range>rand_num:
                select_idx = idx
                break
        # 步进
        self.tabu_km[self.pos] = 1
        self.pos = possible_next_pos[select_idx]
        self.path.append(self.pos)
        # 如果到达终点，留下信息素
        if self.pos==END:
            for idx, pos in enumerate(self.path):
                next_tau_plus[pos]+=config.Q/(idx+1)
            return self.path, False
        return None, True
    

def main():
    path_lengths = []
    paths = []
    global_minium_path = None
    global tau, next_tau_plus
    for loop_idx in range(config.loop):
        loop_minium_path = None
        loop_minium_path_length = np.inf
        for _ in range(config.ants_num):
            ant_loop = True
            ant = Ant(START)
            while ant_loop:
                path, ant_loop = ant.move()
                if path is not None:
                    path_length = get_path_length(path)
                    if loop_minium_path is None or path_length<loop_minium_path_length:
                        loop_minium_path = path
                        loop_minium_path_length = get_path_length(loop_minium_path)
        # 信息素挥发并增加
        tau = (1-config.Rho)*tau+next_tau_plus
        next_tau_plus = np.zeros_like(tau)
        if loop_minium_path is not None:
            paths.append(loop_minium_path)
            path_lengths.append((loop_idx, loop_minium_path_length))
            if global_minium_path is None or loop_minium_path_length<get_path_length(global_minium_path):
                global_minium_path = loop_minium_path
    
    # 绘制收敛曲线
    loop_idx = [item[0] for item in path_lengths]
    old_steps = [item[1] for item in path_lengths]
    steps = []
    slow_ptr = 0
    for i in range(config.loop):
        steps.append(old_steps[slow_ptr])
        if i>loop_idx[slow_ptr] and slow_ptr<len(loop_idx)-1:
            slow_ptr+=1
    plt.plot(list(range(config.loop)), steps)
    plt.xlabel("loop index")
    plt.ylabel("steps")
    plt.ylim(0, 50)
    plt.savefig("conver.png")
    # 打印路线图
    print(global_minium_path)
    print(f"min length:{get_path_length(global_minium_path)}")
    rst = SPACE.tolist()
    for dot_idx in range(len(global_minium_path)-1):
        old_x, old_y = global_minium_path[dot_idx]
        new_x, new_y = global_minium_path[dot_idx+1]

        if new_x>old_x and new_y>old_y:
            rst[old_x][old_y]="↘"
        elif new_x==old_x and new_y>old_y:
            rst[old_x][old_y]="→"
        elif new_x>old_x and new_y==old_y:
            rst[old_x][old_y]="↓"
        elif new_x<old_x and new_y==old_y:
            rst[old_x][old_y]="↑"
        elif new_x==old_x and new_y<old_y:
            rst[old_x][old_y]="←"
        elif new_x>old_x and new_y<old_y:
            rst[old_x][old_y]="↙"
        elif new_x<old_x and new_y>old_y:
            rst[old_x][old_y]="↗"
        elif new_x<old_x and new_y<old_y:
            rst[old_x][old_y]="↖"
    for item in rst:
        print(" ".join([str(c) for c in item]))



if __name__ == "__main__":
    main()
