# 流畅的python 阅读随笔
## 目录
[create_named_tuple](py/create_named_tuple.py) : 使用具名元组作为简单数据类  
[function_args](py/function_args.py)  : 使用*args与**kwargs来传递函数参数，配置了默认值时，允许缺省  
[function_signature](py/function_signature.py) : 使用inspect.signature获取函数签名  
[reduce](py/reduce.py) : 使用reduce函数，方便地操作序列中两两元素  
[partial](py/partial.py) : 使用partial冻结部分函数参数，在提供框架时有用。  
[global](py/global.py) : 使用globals()函数查看上下文已经定义的对象名，再使用dir方法查看这些对象的属性和方法。在pdb调试中很有用。
[decorate](py/decorate.py) : 开始使用装饰器，并使用traceback.print_stack追踪运行时代码堆栈。  
[decorate_with_params](py/decorate_with_params.py) : 使用带有参数的装饰器，如果要封装的函数也有参数，这会需要三层封装。  
[local_variable](py/local_variable.py) : python变量的作用域，global保留字的使用，说明了python作为脚本语言，编译的那一面。
[dis_example](py/dis_example.py) : 使用dis.dis查看python函数的字节码，说明了python作为脚本语言，编译的那一面。  
[closure](py/closure.py) : 说明了闭包、自由变量、nonlocal、global的概念及使用。闭包是python函数式编程的关键，使得函数拥有类似类的数据成员。  
[clock](py/clock.py) : 提供了一个较全面的函数时间统计装饰器，同时说明了@functools.wraps(func)的使用。  
[lru_cache](py/lru_cache.py) : 提供了functools.lru_cache的使用范例，和它多级缓存的说明。
[singledispatch](py/singledispatch_example.py) : 说明了functools.singledispatch的使用。这一内置装饰器在解耦if/else组时格外有用。

## 为什么不使用ipynb
fluent-py本身是基础书，故不希望有任何环境需要。

## 额外资源
对于装饰器，[Graham的博客](https://github.com/GrahamDumpleton/wrapt/blob/develop/blog/README.md)十分重要。
## 版本
目前截至至第七章