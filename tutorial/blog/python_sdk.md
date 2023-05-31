# Python SDK开发入门

> 因为最近要把PDL封装成SDK的形式，所以需要学习一下setuptools的用法，有一个神奇的，叫做入口点的配置，可以方便地提供命令行工具。

> 之前以为是打成可执行文件，后来发现也不过是python文件的封装，依然是解释器的调用方法罢了，缺少解释器还是无法调用的.

> 参考：[官方文档](https://setuptools.pypa.io/en/latest/userguide/quickstart.html) 

使用setuptools进行打包，提供了三种标准，pyproject.toml，setup.cfg和setup.py，标准逐渐变老，但也变得更复杂，不过也更灵活。拥抱新标准，我们选择使用pyproject.toml。

pyproject.toml需要的基本配置是：

```toml
[project]
name = "mpkg"
version = "0.0.1"
dependencies = [] # 这里填写setup时需要依赖的第三方库(版本)

[project.scripts]
command-hello = "mpkg:hello" # 入口点，允许将某个python函数暴露为可执行文件，前面是命令名，后面是引用方法。考虑安装完毕后该函数如何被import到即可
command-goodbye = "mpkg:goodbye"

# 一般不需要手动指定find的配置，但是如果项目同级别包括test/tools等不需要被打包的目录，还是手动指定一下src在哪比较好
# 这也仅仅需要where即可
[tool.setuptools.packages.find]
# All the following settings are optional:
where = ["src"]  # ["."] by default
include = ["mypackage*"]  # ["*"] by default
exclude = ["mypackage.tests*"]  # empty by default
# namespaces = false  # true by default，没搞明白这个命名空间是做什么的
```

目录结构是：
```
- src
    - __init__.py
    - main.py
    - ...
- pyproject.toml

```

这样，在pyproject.toml同级别目录，执行python -m build，就可以打包出dist目录，其中将包含whl和tar.gz两种现行的python库标准文件。任何一个都可以被pip install。

此时，我们没有指定本库可执行的操作系统，一般情况下，都不会有不同。不过windows和linux的差异还是不小的，等用到的时候再做特化考虑吧。