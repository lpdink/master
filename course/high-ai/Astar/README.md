# A*算法解决二维迷宫问题
## 问题迷宫：
```
0 0 0 0 1 0 3 0 0 0
0 0 0 0 1 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0
2 0 0 0 1 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
其中0表示可走，1表示不可走，2表示起点，3表示终点。  
实现通用的针对迷宫问题的Astar算法，解决本问题。
## A*算法的执行过程
- 创建open表和closed表
- 将初始节点（迷宫起点节点）计算代价(cost)后，加入open表
- 当open表不为空时，循环：
    - 从open表中选取cost最小的节点，弹出，考察该节点：
        - 如果该节点是终止节点（迷宫终点），说明找到一条路径，算法终止，返回结果。
        - 否则，计算该节点的所有可能转移状态节点，并计算这些转移节点的cost。对所有能转移到的节点，如果不在open表中，则加入open表。
    - 将该节点加入closed表。
- 循环正常结束，表示没有找到可行路径，输出找不到可行解。
## 启发式函数
### 曼哈顿距离
以迷宫的左上角为原点，向下为x轴正方向，向右为y轴正方向，建立坐标系。

设(Xe, Ye)为目标终止位置，则对某一状态(Xi，Yi)，曼哈顿距离定义为：

> <center>mhd(E, I) = |Xe-Xi|+|Ye-Yi|</center>
### 代价函数
要奖励离终止节点更近的选择，要惩罚步数多的选择，且接近终止节点更应该受到奖励。  
故代价函数定义为：  
> <center>cost(E, I) = 2*mhd(E, I)+mhd(O, I)+depth(I)
其中I是第I步的节点坐标，E是目标节点坐标，O是初始节点坐标。  
总是选取cost小的节点作为下一个探索节点。采用优先队列，优化cost排序过程。
## Usage
```
python solution.py
# 这将从同目录下的space.txt读取迷宫。
# 你可以任意修改space.txt中的迷宫（包括维度），确保用0作为可走路径，1作为不可走路径，2作为起点(仅一个），3作为终点（仅一个）即可。
```
## 输出结果
输出相同大小的迷宫阵列，将横向走替换为横向箭头，纵向走替换为纵向箭头,对上述用例，输出结果为：
```
0 0 0 0 1 ↑ → 0 0 0
0 0 0 0 1 ↑ 0 0 0 0
0 0 0 0 1 ↑ 0 0 0 0
0 0 0 0 1 ↑ 0 0 0 0
2 → → → 1 ↑ 0 0 0 0
0 0 0 ↓ 1 ↑ 0 0 0 0
0 0 0 ↓ 1 ↑ 0 0 0 0
0 0 0 ↓ → → 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
## 附录
惩罚depth深的选择是十分重要的，否则会得到这样的解：
```
↑ → → → 1 ↑ → 0 0 0
↑ 0 0 ↓ 1 ↑ 0 0 0 0
↑ 0 0 ↓ 1 ↑ 0 0 0 0
↑ 0 0 ↓ 1 ↑ 0 0 0 0
2 0 0 ↓ 1 ↑ 0 0 0 0
0 0 0 ↓ 1 ↑ 0 0 0 0
0 0 0 ↓ 1 ↑ 0 0 0 0
0 0 0 ↓ → → 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
启发式算法先探索了起始点上方的点，如果不惩罚深度，深度优先搜索的选择将十分诱人。