# Effective VScode

本文将介绍VScode中极好用的操作，提高你的生产效率！  
本文的阅读诀窍是：**试试看比听我说要快得多！**  

## 使用shift+alt进列选取

有下面一张表，现在，要求分离name列和number列。  

```
name    number
xiao    114514
red     223243
plus    159853
...
```

如果在以前，我会通过写一个python脚本的方式，通过空格进行split，写出到两个文件中，但在vscode中，你可以按下**shift+alt+鼠标点击**或**shift+上下左右键**，分离地进行列选择。  
分离结果：

```
number
114514
223243
159853

name
xiao
red 
plus
```

## 使用alt进行多行编辑

有以下代码：

```python
print(text.replace("\n", "")) # 打印没有换行符的text
print(text.replace("\t", "")) # 打印没有制表符的text
```

现在，你被要求删除两行代码的注释，并去除print，改为对text的赋值，你可以一行一行地编辑，但更快的方法是使用**alt+鼠标点击**进行多行编辑：

```python
text = text.replace("\n", "")
text = text.replace("\t", "")
```

你也可以通过**alt+ctrl+上下左右箭头**进行无鼠标的选择。

## 使用alt+上下箭头快速移动一行

代码：

```
dog.sleep()
dog.eat()
dog.play_with_me()
dog.play_with_cat()
```

现在，将狗与我玩的时间放在它睡觉以前。古老的做法是cv+删除+增加，但你可以通过**alt+上下箭头**完成快速移动：

```
dog.play_with_me()
dog.sleep()
dog.eat()
dog.play_with_cat()
```

## 使用alt+shift快速复制一行

```
ant.move_once()
```

现在，让蚂蚁移动两次。古老的做法是复制，回车，粘贴。但你可以通过alt+shift快速完成。  

```
ant.move_once()
ant.move_once()
// 本次任务是通过alt+shift,再利用alt+箭头，再进行alt+shift完成的，没有进行cv.
// 享受vscode吧！
```

## 翻页、换行、快速选取

使用**上下箭头**进行换行。  
使用**ctrl+上下箭头**代替鼠标滚轮（光标不移动）。  
使用**alt+左右箭头**进行翻页（光标移动）（如果到达文件末尾或开头，会切换到相邻的其他文件）。  
使用**shift+箭头**进行无鼠标的选取。  
使用**ctrl+左右箭头**进行光标的块跳转。  
结合上两点，使用**shift+ctrl+左右箭头**选取块方法。
这样，你可以方便地复制或删除某个方法的调用：
你被要求将方法find_another_node_with_name复制给new_node：

```py
node.find_another_node_with_name(name)
new_node
```

```py
node.find_another_node_with_name(name)
new_node.find_another_node_with_name(name)
```

## 不太常用的

用ctrl+shift选择一个方法名，用ctrl+shift+L对他进行全局重命名

```
moon.turn_on()
sum.turn_on()
person.turn_on()
```

```
moon.trun_off()
sum.trun_off()
person.trun_off()
```
