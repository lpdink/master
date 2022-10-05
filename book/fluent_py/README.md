# 流畅的python 阅读随笔
## 目录
[create_named_tuple](create_named_tuple.py) : 使用具名元组作为简单数据类  
[function_args](function_args.py)  : 使用*args与**kwargs来传递函数参数，配置了默认值时，允许缺省  
[function_signature](function_signature.py) : 使用inspect.signature获取函数签名  
[reduce](reduce.py) : 使用reduce函数，方便地操作序列中两两元素  
[partial](partial.py) : 使用partial冻结部分函数参数，在提供框架时有用。  
[global](global.py) : 使用globals()函数查看上下文已经定义的对象名，再使用dir方法查看这些对象的属性和方法。在pdb调试中很有用。
[decorate](decorate.py) : 开始使用装饰器，并使用traceback.print_stack追踪运行时代码堆栈。  
[decorate_with_params](decorate_with_params.py) : 使用带有参数的装饰器，如果要封装的函数也有参数，这会需要三层封装。
