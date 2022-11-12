# CXX Primer笔记
本笔记是不常用的CXX基础语法的查漏补缺。
## 第一章 开始
### cerr与clog
cerr不缓冲，用于显示错误信息，以及你不想被> 转发到Log文件的信息。  
clog可以作为输出log。  
### 仅using必须的项目
不使用using namespace xxx而仅仅using其中你需要的，如：   
```
using namespace std::cout;
```
### 使用++i而不是i++
因为当我们使用自增时，往往希望自增先结算。
# 第Ⅰ部分：C++基础
## 第二章 变量和基本类型
### 内置类型与长度
在ubuntu20.04，g++ 9.4.0下:
```
// 整型
bool 1
char 1
wchar_t 4 // 宽字符是内置类型哦
char16_t 2
char32_t 4
short 2
int 4
long 8
long long 8
// 浮点
float 4
double 8
long double 16
```
单位是字节(8位)。  
不要使用long，它的长度可能和int一样，有需求，直接long long。long long是C++11新定义的。    
除bool整型可前置signed/unsigned。  
当char用作数字类型时，明确指示是signed char还是unsigned char，因为单纯char的范围由编译器实现决定。  
### 警惕unsigned
- 警惕unsigned的值经过计算（尝试）到达负值，此时会重回上界。
- 警惕unsigned的值与signed的值的比较。
在实际场景中，冒犯两个警惕的最常见场景是，stl容器的.size()，这个方法的返回值是unsigned的！
```
template <typename T>
void show_except_last_err(const vector<T> &res_v)
{
    // 警惕unsigned尝试变为负数.
    // 很隐晦的是stl容器的size()，这是一个unsigned！

    // 本例是一个错误的示范：
    // vector.size()是unsigned的，如果vector长度为0，<的右式会最大！进入循环后会Segmentation fault!
    for (int i = 0; i < res_v.size() - 1; i++)
    {
        cout << res_v[i] << endl;
    }
}

// 正确的写法是：
template <typename T>
void show_except_last_right(const vector<T> &res_v)
{
    for (unsigned int i = 0; i + 1 < res_v.size(); i++)
    {
        cout << res_v[i] << endl;
    }
}
```
> 真是令人怀念，当时的基础确实太差了...
### 不要依赖隐式转换和错误
不要写这样的代码：
```
double d1=3.14;
int i1=d1;
float f1=i1;
```
当然，编译器理解你要做什么，但为了可读性，更好的写法是：  
```
double d1=3.14;
// many other lines...
int i1=(int)d1;
// many other lines...
float f1=(float)i1;
```
这是在告诫阅读者，d1与t1的类型不同，i1与f1的类型不同。  
不要依赖于错误，常见的是通过超出范围取得最大值：
```
unsigned char char_max=-1;
cout<<(int)char_max<<endl;
```
在“不合常理”时，程序的行为是不确定的，可能错误，可能放过，可能产生随机值，这取决于你的编译器、编译flag，执行平台。  
这是不可移植，或是难再现的，对debug来说很糟糕。
### "比'长一位
'就是单纯的char。"本质上则是常量字符构成的数组，且会在末尾固定添加'\0'。  
在你对char*调用printf或cout时，他们会打印直到第一个'\0'。
### 前缀与后缀
```
// 前置
u"123456" -> char16_t
U"123456" -> char32_t
L"123456" -> wchar_t
u8"123456" -> char
// 后缀
12345u or 12345U -> unsigned
1.23f or 1.23F -> float
1234l or 1234L -> long
1.234l or 1.234L -> long double
1234ll or 1234LL ->  long long
```
### 使用extern
extern允许我们在一个cc文件中获取另一个cc文件的定义式，而不必通过.h，只要最后将两个cc文件联合起来编译就可以了。  
> 我总感觉这不太妙，这在破坏封装性。  
```
// file1.cc
extern const test=1;
...
// file2.cc
extern const test;
...
cout<<test<<end;
```
如上所示，这样就能直接在file2中获得file1.cc定义的变量/常量了。  
如果你没有同时编译他们，只编译file2.cc，会报undefined reference的错误。  
> 变量只能被定义一次，但可以被多次声明。
### 左值引用
引用是对象的别名，因此必须有对象（即引用必须被初始化）。  
与python的引用不同，这是真正的别名。对赋值语句也作用！
```
int val=1024;
int val2=2048;
int &ref_val=val;
ref_val=val2;
std::cout<<val<<" "<<val2<<" "<<ref_val<<" "<<std::endl;
// result:
// 2048 2048 2048
```
不能创建引用的引用(这句话容易令人误解，这不是指，一个引用绑定到某个对象后，不能通过该引用创建到该对象的新引用，而是指不能创建到某个引用本身的引用)。  
你大可以这样做：
```
int &ref_val=val;
int &ref_val2=ref_val;
```
### 使用nullptr，不再使用NULL
这是新标准的现代C++的推荐。
### void*指针
指向任何存放任何对象的地址。  
void*指针的确存放一个地址，但是我们不知道该地址里的对象是什么。  
它看上去作用有限，无法被直接解引用，但是可以作为一个多类型分发的办法：
```
int tmp=114514;
void *ptr=&tmp;
int *int_ptr;
int_ptr=(int* )ptr; // 只要你知道void*指向的是什么类型...就能通过强转拿到值
```
### *属于var，而不是type
```
// p1是int*，p2是int。
int *p1,p2;
// 所以不要这样写，会导致误解。*修饰的是变量。
int* p1, p2;
```
### 高阶指针
```
int val = 1024;
int *p = &val; //一般的一阶指针，左值是指针，右值是地址。
int **pp=&p; //二阶指针
```
### 创建指针的引用
```
int val=42;
int *p=&val;
int *&ref_p=p; //引用的类型是int *， 所以&在*后面。
```
对于更高阶的（为难人的情况），推荐从右向左读，是&就是引用，是*就是指针。  
### TODO:const