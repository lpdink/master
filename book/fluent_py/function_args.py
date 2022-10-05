def print_args(a=1,b=2,c=3,d=4):
    print(a,b,c,d)

# 当使用**kwargs或*args时，也可以同时使用默认参数
args={"a":"a", "b":"b"}
print_args(**args)
args = [1,2,3]
print_args(*args)
