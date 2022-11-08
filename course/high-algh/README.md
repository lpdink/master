# 在线算法
## 问题定义
存在长宽高为length(l), width(w), height(h)的3维空间，将连续给出的一组货物存入空间，求使得空间利用率最高的算法。  
- 第i个货物的长宽高为i_l, i_w, i_h。
- 第i个货物放入后，空间利用率为Σ(i_v)/(l\*w\*h)
## 思路
### 如何描述状态空间
算法的关键在于描述三维空间在某一时间断面的状态，即放入货物i后的空间占用及空闲状态。  
可以使用二维数组+一维高度的形式描述状态空间。  
即将对于长宽高均为5的状态空间，在起始时表示为：
```
{
    5, 5, 5, 5, 5,
    5, 5, 5, 5, 5,
    5, 5, 5, 5, 5,
    5, 5, 5, 5, 5,
    5, 5, 5, 5, 5,
}
```
以数组原点作为空间原点，优先在靠近坐标原点处放置货物，则在放入货物(2, 3, 4)后，空间可以表示为：
```
{
    1, 1, 1, 5, 5,
    1, 1, 1, 5, 5,
    5, 5, 5, 5, 5,
    5, 5, 5, 5, 5,
    5, 5, 5, 5, 5,
}
```
### 如何进行状态转移
对于第i个货物(i_l, i_w, i_h)，要找到空间中的一片位置可以放置它，即在space中找到(i_l, i_w)大小的矩阵，矩阵内部的所有元素均大于i_h。  
由于货物是在线给出的，故使得算法具备更高的利用率，即提高空间在装入当前货物后，装入更多货物的潜力。  
故在当前货物i可放置的所有位置中，选择放置i后，空间潜力最大的位置。  
假定货物可以旋转，不妨令i_h>=i_w>=i_l，此时，优先选择内部元素和最小的矩阵(高度潜力最低的矩阵)，留下高度潜力高的矩阵，以便后续货物最高的边i_h可能能装入。
## Requirements
```
python>=3.8
numpy
scipy
```
## Usage
```
# 随机生成货物输入
python tool/static.py

# 测试
python solution/3d-map.py
```
## 性能
对空间100\*100\*100，生成100个货物，每个货物的长宽高随机，均服从[1, 40]的均匀分布。100个货物的体积期望为800000，空间占用期望80%。  
进行了10次测试，每次测试结果及算法耗时如下：
```
space usage:730301 in 1000000  0.730301%
in all_v:0.7714460764895713%
main cost 7899.402618408203 ms

space usage:625695 in 1000000  0.625695%
in all_v:0.8988075657304073%
main cost 6263.985872268677 ms

space usage:626654 in 1000000  0.626654%
in all_v:0.6764794148190849%
main cost 6800.952434539795 ms

space usage:701574 in 1000000  0.701574%
in all_v:0.7515973106045998%
main cost 7175.0078201293945 ms

space usage:561286 in 1000000  0.561286%
in all_v:0.6681156953373575%
main cost 6564.270973205566 ms

space usage:612695 in 1000000  0.612695%
in all_v:0.9324128338307155%
main cost 6016.13712310791 ms

space usage:728558 in 1000000  0.728558%
in all_v:0.6547764770167936%
main cost 7842.029571533203 ms

space usage:636145 in 1000000  0.636145%
in all_v:0.6935781236882532%
main cost 6843.368053436279 ms

space usage:624322 in 1000000  0.624322%
in all_v:0.7486530595603692%
main cost 6256.461143493652 ms

space usage:675056 in 1000000  0.675056%
in all_v:0.8121033054073172%
main cost 7554.092884063721 ms

```
可见，在这一设置下，放入100个货物需要约6~9秒，空间利用率56%~73%(期望80%)，放入的体积占总货物体积的65%~93%(期望100%)