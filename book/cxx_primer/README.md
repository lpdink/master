# CXX Primer笔记

本笔记是不常用的CXX基础语法的查漏补缺。

## 第一章 开始

### cerr与clog

cerr不缓冲，用于显示错误信息，以及你不想被> 转发到Log文件的信息。  
clog可以作为输出log。  

### 仅using必须的项目

不使用using namespace xxx而仅仅using其中你需要的，如：

```
using std::cout;
```

### 使用++i而不是i++

++i的效率比i++更高，且当我们使用自增时，往往希望自增先结算。

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

```cpp
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

extern允许我们在一个cc文件中获取另一个cc文件的定义式(包括变量，函数和类定义)，而不必通过.h，只要最后将两个cc文件联合起来编译就可以了。  
> 我总感觉这不太妙，这在破坏封装性。  

```
// file1.cc,对非const的情况，在定义式中可以略去extern.这是默认选项。
// 这也解释了我们为什么一定要命名空间，默认extern太容易造成命名空间污染了！
extern int test=1;
...
// file2.cc
// 这里是声明式,编译器会放过这里,让链接器去找定义式,找不到时,链接器报错.
extern int test;
...
cout<<test<<end;
```

如上所示，这样就能直接在file2中获得file1.cc定义的变量/常量了。  
如果你没有同时编译他们，只编译file2.cc，会报undefined reference的错误。  
> 变量只能被定义一次，但可以被多次声明。

默认extern非常容易造成命名空间污染：

```cpp
// 如果你在两个cc文件中定义了相同签名的函数，就会出现multiple definition的错误！
// file1.cc
int test(int a, int b){return a+b;}
// file2.cc
int test(int a, int b){return a*b;}

// 错误信息：multiple definition of `test(int, int)'
```

> 这个错误也令人怀念...celt_lpc.

在编译库提供给外部语言调用时，如果两个库中不加namespace地提供了同签名函数。外部语言编译器或解释器的行为是难以控制的，是不通过，还是随机调用其中一个？因此，绝对不要这么做，应该尽力通过namespace避免这一情况。

### extern "C"

extern "C"是C++/C混编的方案，在C++中使用extern "C"修饰函数，**并不是**在告诉C++编译器将工作交给C编译器去做，而是使用C++编译器，按照C风格去编译这里。  
什么是C风格？具体来说，就是不按照函数重载规则重命名这里的函数符号。  
C++支持了函数重载，这并不是通过真的保存两个同名符号，而是通过某种规则，根据你的函数签名重命名了同名符号，保证不冲突。这意味着你定义的函数名会被编译器修改。  
C不支持函数重载，所以你写的函数名，就会被编译器直接拿去用，写在库中的，也是你写的函数名，它与头文件写的接口一致。  
外部语言并不一定能理解C++的重名规则(例如JNI)，此时，用extern C能确保外部语言按照你给的.h文件，真的能找到函数定义。  
对于你要暴露给外部语言的接口(.h)文件，添加：

```
#ifdef __cplusplus
extern "C" {
#endif
// ...你的声明式...
#ifdef __cplusplus
}
#endif
```

保证你要暴露的函数声明在extern "C"包裹中即可，至于namespace声明，包含与否都无关痛痒。  
但与此同时，如果使用C++重载去理解声明式(头文件)是外部语言的默认，(例如C++)，但你却贴心地在暴露接口时使用了extern "C"，那么在引用接口时，记得也要：

```
extern "C"{
    #include "your_interface.h"
}
```

注意：**extern "C"仍然是C++编译器在编译，所以你可以在其中尽情地使用C++特性！**

### static

在可见性上，static与extern相对。  
被static修饰的符号，只能在定义的作用域内可见，对外部不可见。
static可能有以下的几种状态：

- 静态局部变量：  
在全局数据区分配内存，要求在声明处c初始化，只被初始化一次，值会保存到下一次函数调用。(因为内存空间在全局数据区，而不是栈上，栈上数据会被回收。)
- 静态全局变量：  
对其他文件完全不可见，避免命名冲突。
- 静态函数：
与静态全局变量一致，对其他文件不可见，避免命名冲突。
- 静态成员变量：
其实就是类变量。
- 静态成员函数：
其实就是类函数。

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

### const

- 可见性
默认情况下，const变量只在文件内部有效。要使得它能被外部cxx取得，需要用extern声明。
- **const与引用**

```
// 你可以这样做，但这没啥用。
const int ci=42;
const int &same_ci=ci;
// 更常见的是，创建一个非const对象的const引用
int ci=42;
const int &you_cant_change_ci=ci;
```

创建一个非const对象的const引用是非常有用的，通常在定义函数时，形参被定义为一个const引用，但是传递进来的实参本身并不是const的。这使得我们能传递引用，但是保证函数不修改我们的对象。

- **const与指针**
**指向常量的指针**

```cpp
// 真正指向常量的指针，很少这样做.
const int val=42;
const int* val_ptr=&val;
// 实际上指向了一个非const的对象的，形式上指向const对象的指针（我要笑死了）
// 然而这很有用，阻止获得val_ptr的人修改val。
int val=42;
const int* val_ptr=&val;
```

与引用一样，你传递一个指向const对象的指针（它实际上指向了一个非const对象），可以阻止获得指针的函数修改这个对象。  
这一做法也常用在函数的形参定义时。  

**常指针/顶层const**
常指针指，指针指向的地址本身不能变化，但是地址内的值可以变化。感觉用的比较少。  
底层const则指，指针指向的对象是常量，指针本身指向的地址则可以变化。  

```cpp
int val=42;
int* const ptr=&val; //ptr将一直指向&val地址，但是不会管里面的值是否变化。

const int* const another_ptr=&val; //another_ptr将一直指向&val地址，并且保证不能通过another_ptr修改&val存储的值。
```

### constexpr常量表达式

C++11特性。  
这是一种在**编译时**由编译器计算结果的表达式，而不是在运行时计算。  
得到计算结果后，该对象与const在运行时的行为一致。  
你可以将一切你认为应该是constexpr的表达式声明成constexpr的，如果不是，编译器会告诉你的。

```cpp
vector<int> res_vec;
// 如果你尝试这样做，编译器会报错。
constexpr int length = res_vec.size();
// error: call to non-‘constexpr’ function ‘std::vector
```

你不能这样做：

```
int val=42;
constexpr int double_val=val+val;
```

但是却可以这么做：

```
int val=42;
const int double_val=val+val;
```

因为constexpr保证会在编译时得到结果并替换，但const没有许下这样的承诺。  
如果追求执行时性能，使用constexpr十分美妙。
**constexpr与指针：**
不要用constexpr修饰指针！  
constexpr修饰指针，不会使得指向的对象成为常量，永远会使你创建的指针是一个常指针！

```cpp
const int *p = nullptr; // 这是指向常量的指针
constexpr int *q = nullptr;// 这是常指针！
```

你可以混用constexpr与const创建一个指向常量的常指针，但是，你可以用两个const完成这一工作，所以别把constexpr与指针放在一起。

```cpp
constexpr int *p=nullptr
// is eq to 
int *const p=nullptr;
//-------
int val=42;
constexpr const int *p=&val;
// is eq to 
const int *const p=&val;
```

> 但话说回来，constexpr const int \*ptr这种写法真的好漂亮哦，比const int* const ptr好看多了...

### typedef

除了typedef，11标准支持了一种新写法：

```
typedef double MyDouble;
using MyInt=int; // 11标准
```

### auto

auto也是c++11新支持的。  

- 与const

```cpp
const int val=42;
auto a=val; //a 不是const的，顶层const被忽略了。
auto p=&val //p是一个指向const的指针，底层const被保留了。
// 如果希望保留顶层const:
const auto another_a=val;
```

### decltype

C++11新支持的。  
可以从表达式或函数的结果取得类型（并不实际执行表达式或函数）。  

```
int i=42;
decltype(i) x=84;
```

> 见了能认识就行了...你不会真想用这个吧，额

### 预处理器：避免多次include

\#系列的命令由预处理器执行，包括include。  
它的工作逻辑非常简单，发现#include，找到include的文件，将内容复制到当前文件。  
这带来一个问题，在层级引用中，有可能会出现多重include:

```cpp
// file1.h
define something
// file2.h
#include "file1.h"
define something
// file3.h
#include "file1.h"
#include "file2.h" //由于file2也引入了file1，这里会导致file1被多次引入
define something

```

解决这个问题的办法就是通过定式：

```
#ifndef YOUR_H_FILE_NAME_H
#define YOUR_H_FILE_NAME_H
// 正文
#endif
```

**这是一个routine，你永远应该这样做，没有例外。**

## 第三章 字符串、向量和数组

### 别在头文件中使用using

因为头文件会被别的文件include，进行替换时引入命名符号绝对不好！

### string

```
#include<string>
using std::string;
```

- 初始化

```cpp
string s1;
string s2=s1; // or string s2(s1);
string s3="aljd";
string s4(3, "c");//"ccc"
```

=执行的是拷贝初始化，()执行的是直接初始化。在C++20中可以用{}初始化，先别那么做吧。  

- 使用getline从流中读取一行：

```
string s;
getline(file_stream, s);// 遇到\n时停止，\n也会被读入。
```

- empty()
- size()
size返回的既不是int，也不是unsigned int，而是string::size_type。（不过它是unsigned的）  
**建议**：如果用了size()，最好别用int，避免int与unsigned混用的问题。  
- sub

```
string s="12345";
s.sub(begin_index, nums);//注意第二个参数是个数。
```

### 处理字符的函数

定义在头文件cctype中

```cpp
isalnum(c) //c为字母或数字
isalpha(c) //c为字母
iscntrl(c) //c为控制字符
isdigit(c) //c为数字
isgraph(c) //c不是空格，但可打印
islower(c) //c是小写字母
isprint(c) //c可打印
ispunct(c) //c是标点符号(不是控制字符，数字，字母，可打印空白中的一种)
isspace(c) //c是空白(包括空格，横纵向制表符，回车，换行，进纸符)
isupper(c) //c是大写字母
isxdigit(c) //c是十六进制数字
tolower(c) //c转小写
toupper(c) //c转大写
```

**建议**：C++兼容了C的标准库头文件，对c的name.h，C++将他们命名为cname。所以，这里cctype与ctype.h头文件的内容是一致的。编写C++时，推荐用C++风格的头文件。

### 范围for

范围for实际上在执行一个拷贝，所以，当你想要修改值时，需要添加引用&.

```
string s="qwerty";

for(auto& c:s){
    ... // c是引用，故可以修改s。
}
```

这里也能看出与python的不同。C++的string是char数组，而不是不可变序列。你可以修改其中的任何一个字符，这个过程没有在创建新字符串。

### vector

```
#include<vector>
using std::vector;
```

- 初始化

```cpp
vecotr<T> v1;
vector<T> v2(v1);
vector<T> v2=v1;//对元素拷贝的
vector<T> v3(n, val);
vector<T> v3(n);//会采用T的默认值
vector<T> v4{a,b,c...};//C++11已经有这种写法了
vector<T> v4={a,b,c};
```

**警告：C++标准要求vector优先对动态增长高效，在初始阶段指定vector的大小甚至会降低效率！(除非所有元素的值相同)。这与python不同。**

### 迭代器

除了下标运算符，还可以利用迭代器访问容器元素。  
所有的标准库容器都可以使用迭代器。  
string不算容器，但也可以使用迭代器。  

```cpp
string s("abcdefg");
// end()返回的迭代器并不实际指向某个元素，只作为\0
if(s.begin()!=s.end()){
    auto it = s.begin(); // 使用auto获得迭代器。
    // 迭代器的行为与指针非常像：
    *it = toupper(*it);
}
```

迭代器的行为与指针类似：

```
*iter 解引用
iterm->mem 解引用并访问mem成员，等价于 (*item).mem
++iter 访问下一个
--iter 访问上一个
iter1 == iter2 判断两个迭代器是否指向相同元素
```

**建议**并不是所有的标准库容器都定义了迭代器的<或！因此，总是使用!=来判断迭代器是否走到了末尾。  

- 迭代器的真实类型
我们总是用auto访问，但迭代器的真实类型是：

```
vector<int>::iterator it;
vector<int>::const_iterator it2;// const 迭代器，只能读不能写
```

- cbegin与cend
使用begin与end时，返回元素是否const由元素本身是否const决定。  
如果一定要获取const，使用cbegin与cend方法。
- 迭代器是支持一次+num或-num的，因此可以方便地用于复杂情况（如二分查找）。  

### 箭头运算符->

是解引用(*)与访问元素(.)运算符的组合。  

```
iterm->mem 解引用并访问mem成员，等价于 (*item).mem
```

### 数组

数组的长度固定，要求在定义时给出，[]内必须至少是一个常量表达式:

```
int num[a_constexpr];
```

- 初始化  

在栈内，默认初始化会让数组拥有随机值, 如果要置零，用={0}。  
在堆上，被初始化为0。  

- 字符数组

字符数组有一个\0的结尾约定，故存在，你需要\0，你不需要\0两种情况：

```cpp
char a1[]={'c','+','+'}; // 不会添加\0
char a1[]={'c','+','+','\0'}; // 你自己添加了\0
char a3[] = "C++"; // 编译器为你自动添加\0
const char a4[3]="C++"; // 报错，没有空间添加\0
```

- 不允许拷贝和赋值

```cpp
int a[]={1,2,3};
int a2[]=a;// 错误，没有拷贝构造函数
a2 = a; //错误，不允许赋值
```

- 数组支持范围for访问！

因为数组的维度是固定的，算作数组属性的一部分，编译器是知道数组大小的。  
因此这是可以(且推荐)的

```cpp
int array[10];
for(auto& element:array){
    ...;
}
```

- 使用begin与end访问数组的首(尾+1)元素

C++11特性。  

```cpp
int array[]={1,2,3,45};
int *beg = begin(ia); // 指向1
int *last = end(ia); // 指向45的下一位置。不能对last解引用！
```

- 下标和指针

这里同样演示一种等价：  

```cpp
int array[]={1,2,3,4,5};
int *p = array;// 等价于int *p = &array[0]
```

注意，数组的[]是取值运算！返回的是数组中的值而不是地址。  
如果要获得数组某个元素的地址：

```
&array[i];
或
array+i;
```

### C风格字符串

c风格字符串即常用的字符串字面值。  
定义在头文件\<cstring\>(c++)或\<string.h\>(c)中的方法用于支持他们。
C标准库的方法是：

```cpp
strlen(p)
strcmp(p1, p2) //p1==p2,ret=0, p1<p2 ret=-num, p1>p2,ret=+num
strcat(p1, p2) //p1+p2
strcpy(p1, p2) //p1=p2
```

strlen方法实际上在尝试找到\0，如果一个const char*没有\0，会产生未定义的情况...  
strcat要求一个新的空间，这个空间足够大，能放下p1+p2。然而这个空间是用户申请的，如果大小计算错误，也将引发严重的内存错误。  

**建议**：因此，除了极少的用于字符串字面量的情况，不使用c风格字符串，能string尽量string。

### 混合使用string与c风格字符串

> 这就是所谓的，C++沉重的历史包袱(的很少一部分)

可以使用string.c_str()获取一个const char*，这是将string降级为c风格字符串的方法。  

```cpp
string s("12345");
const char *c_s=s; // 错误
const char *c_s=s.c_str(); // 正确
// 对s的修改会反映到c_s上。
```

### 使用数组初始化vector对象

使用字面值初始化vector是显然的：

```cpp
vector<int> vec = {1,2,3,4,5};
```

但是下面的做法不行：

```cpp
int nums[]={1,2,3,4,5};
vector<int> vec = nums;
```

应该这样写：

```cpp
int nums[]={1,2,3,4,5};
vector<int> vec(begin(nums), end(nums));
// 这里用cbegin和cend也可以

// 或者
vector<int> vec(nums, nums+5); // 注意是+5，即使+5访问不到.
```

### 多维数组

```cpp
int a[2][3][4]={0}; // 这会将2*3*4都初始化为0；
```

多维数组是支持范围for的：

```cpp
int a[5][8]={0};
for(auto &row:a){
    for(auto col:a){
        ...
    }
}
```

**注意：** 使用范围for遍历多维数组，只有最内层循环可以不使用引用。
> 如果你尝试在外层循环不使用引用，编译器会报错，auto会将通过外层循环得到的量理解为指针而不是数组。你尝试遍历一个int*指针，当然会报错。  

## 第四章 表达式

### 左值与右值

右值(rvalue)读are-value,左值(lvalue)读ell-value。  
在C中，概念很简单，左值能出现在赋值语句左侧，右值则不能。  
在C++中，比较复杂。当一个对象被用作右值时，用的是对象的值/内容，当对象被用作左值的时候，用的是对象的身份（在内存中的位置）  

### 求值顺序的未定义情况

一个常见的情景：

```cpp
int i=0;
cout<<i<<" "<<++i<<endl;
```

<<运算符与++运算符的顺序是未定义的。  
> 令人吃惊的是，f(x)\*g(x)的顺序也是未定义的，f(x)和g(x)一定会在\*之前调用，但他们的调用顺序是不确定的。  

### 天然的海象表达式

C++天然支持海象表达式：

```cpp
int i;
if((i=get_value())==42){
    cout<<"i is eq to 42"<<endl;
}
```

注意赋值语句的优先级很低，因此必须加括号。

### 一些不清楚的运算顺序

自增运算符与其他运算符混合，运算顺序往往都不清楚：

```cpp
cout<<*iter++<<endl;
// 这里会先对iter解引用，再++。
```

> 虽然primer建议读者写这样的语句，但是笔者不建议你这么写。  

> 在笔者的观点里，除了教学和装x，你永远不应该将自增运算符与双目运算符混用。  

### 条件运算符

C++是支持条件运算符的，享受它吧！

```cpp
bool failed = (score<60)?true:false;
```

> 你不应该嵌套条件运算符，除非你在写算法题。

### 位运算符

```
~ 按位求反
<<  >>左移右移
& 位与
^ 位异或
| 位或
```

### 类型转换: static_cast

C风格的强制类型转换(即前置(type))非常不推荐，应该使用static_cast或reinterpret_cast取代它。  

```cpp
double num=4.2;
void *p=&num;
double *dp = static_cast<double*>(p);
```

### const_cast\<type>(old_num)

const_cast可以去掉底层const。由于const指针可以指向非const对象，因此在**必要条件**下，去掉const指针的const还是可以的（如果它实际上指向了一个非const对象）。  
但是，如果它指向了一个const对象，使用const_cast后的写行为是非常危险的，是未定义而取决于编译器的：

```cpp
const int num=42;
const int *ptr=&num;
int *new_ptr = const_cast<int*>(&num);
*new_ptr=88;
cout<<num<<" "<<*ptr<<" "<<*new_ptr<<endl;
// 执行结果是
// 42 88 88
```

看上去，g++守护了我们最好的const int，但是对指向该const int的指针则不然。我们不禁要问，这里发生了新的内存分配吗？我们在哪里申请了两个int的空间？  

```cpp
const int num[]={1,2,3};
const int *ptr=num;
int *new_ptr = const_cast<int*>(ptr);
*new_ptr=88;
for(auto& n:num){
    cout<<n<<" ";
}
// 结果是88 2 3
```

所以，上面的情况只是编译器变的戏法，它先将const int这样的常量做了全局的替换，就像#define一样。
**num**的值，它的地址存储的值，已经改变了。  
> g++什么也没守护...我哭死...

### 区分static_cast与reinterpret_cast

static_cast用于“存在某种转换协议”时，常见的情况有：

1. 用于类层次结构中基类和派生类之间指针或引用的转换
    - 进行上行转换（把派生类的指针或引用转换成基类表示）是安全的
    - 进行下行转换（把基类的指针或引用转换为派生类表示），由于没有动态类型检查，所以是不安全的
2. 用于基本数据类型之间的转换，如把int转换成char。这种转换的安全也要开发人员来保证
3. 把空指针转换成目标类型的空指针
4. 把任何类型的表达式转换为void类型

reinterpret_cast如其名，用于类型的重新解释，是一种低层次的转换，它并没有直接做什么，只是让编译器重新去理解一个变量。
我们的数值实际上以字节为最小单位存放在申请的空间中，该空间被用“变量类型”(作为协议)来解释。  
reinterpret就是用新的变量类型(新协议)来解释相同的一块内存空间。
这里提供一个较好的，应用了三种转换的实例：

```cpp
string s("0123456789-abcdefgh");
const char *s_c=s.c_str();
char* writable_sc = const_cast<char*>(s_c);
// 重解释为unsigned char
unsigned char *uc_writable_sc=reinterpret_cast<unsigned char*>(writable_sc);
int idx=0;
// \0==0
uc_writable_sc[1]=242; // 修改使超出signed char范围
uc_writable_sc[2]=-42;
while((uc_writable_sc[idx])!='\0'){
    cout<<writable_sc[idx]<<" "<<static_cast<int>(writable_sc[idx])<<" ";
    cout<<uc_writable_sc[idx]<<" "<<static_cast<int>(uc_writable_sc[idx++])<<endl;
}
cout<<uc_writable_sc<<" "<<writable_sc<<" "<<s_c<<" "<<s<<endl;
```

结果是：

```
0 48 0 48
� -14 � 242
� -42 � 214
3 51 3 51
4 52 4 52
5 53 5 53
6 54 6 54
7 55 7 55
8 56 8 56
9 57 9 57
- 45 - 45
a 97 a 97
b 98 b 98
c 99 c 99
d 100 d 100
e 101 e 101
f 102 f 102
g 103 g 103
h 104 h 104
// string被改变了！它本来是一个const char*的。
0��3456789-abcdefgh 0��3456789-abcdefgh 0��3456789-abcdefgh 0��3456789-abcdefgh
```

可以看到，在0-127范围内，char与unsigned char的行为是完全一致的，只有在我们有意的超出两个类型的范围的修改上表现出差异。
static, reinterpret, const三种cast都发生在编译时期。  

### TODO: dynamic_cast

运行时执行的，运行时进行类型检查，需要自定义类型且具备虚函数，不能用于内置类型。  
在后面推进到虚函数时来补充。

## 第五章 语句

### switch

```cpp
int i=0;
switch (i){
    case 0:
        i+=2;
        break; // 如果注释掉本行，会进入case 2;
    case 1:
        i+=2;
        break;
    case 2:
        i=99;
        break;
    default: // 如果没有一个case触发，执行这里
        i=-99;
        break;
}
```

### do-while

```cpp
do{
    ;;;
}while(bool_exp)
```

### 异常处理：try-catch

由于真实系统的边界情况极多，异常处理逻辑复杂。如果与业务逻辑交织在一起，将令维护者难以快速判断哪里是(处理99%情况的)核心代码。
因此，在程序架构上，应该将异常捕获/处理的代码与业务逻辑分离开来，在底层遇到边界情况时抛出异常，在最上层捕获异常，并进行处理。  

- 使用throw抛出异常

> 标准库异常定义在stdexcept头文件中

```cpp
throw runtime_error("a runtime error msg");
```

- 使用try-catch捕获异常

```cpp
try{
    // 可能出现异常的代码
} catch (runtime_error err){
    cout<<err.what();//what 被标准库的所有异常提供
}
```

stdexcept中定义的异常：

```
exception // 最常见的异常，不允许提供任何信息，只能默认初始化。
runtime_error 描述 // 被以下四个继承，本身也可以作为一种异常使用
range_error 边界错误
overflow_error 上溢
underflow_error 下溢
system_error 系统错误

logic_error 描述 // 被以下四个继承，本身也可以作为一种异常使用
domain_error 域错误
invalid_argument 非法参数
length_error 通常是创建对象是给出的尺寸太大
out_of_range 访问超界
future_error 未知错误
```

## 第六章 函数

### 为什么const形参是可行的？

使用实参初始化形参时，会忽略顶层const。  

### 数组作为形参

以下三种写法是等价的，且不会构成函数重载。

```cpp
void print(const int*);
void print(const int[]);
void print(const int[10]);
```

第三种写法暗示着作者期待一个长为10的数组传入，但C++不会为你做这样的检查。必须由作者保证不进行越界访问。  
> 数组传参的本质是传一个int*，因此用int*替代数组传参，这更加清晰。  

传递一个指针，再传递（合法的）长度，不如传递两个指针：

```cpp
void print(const int *beg, const int *end){
    while(beg!=end)
        cout<<*beg++<<endl;
}
```

这是标准库容器的常见初始化方法，这很好。  

### 不要返回局部变量的引用或指针

在局部栈上申请的对象，如果返回对象，其实是在返回对象的拷贝，因为栈上空间会在离开栈时被回收。  
但是编译器的实际实现却不这么做，我们来看这样的示例：
为了方便演示，定义一个类Node，它在被创建时输出new，被销毁时输出delete。

```cpp
class Node
{
public:
    Node()
    {
        cout << "new" << endl;
    }
    ~Node()
    {
        cout << "delete" << endl;
    }
};
```

如果我们在局部变量中在栈上创建一个node，并将它返回，外层的node和里层的node是同一个吗？

```cpp
Node ret_node()
{
    Node node = Node();
    cout <<"node inside addr:"<<&node<<endl;
    return node;
}

int main()
{
    Node node = ret_node();
    cout << "outside node addr:" << &node << endl;
}
```

结果是：

```
new
node inside addr:0x7fff31dbe477
outside node addr:0x7fff31dbe477
delete
```

是同一个！(但是先等等，继续往下看)
这意味着我们可以返回栈上对象的地址或指针吗？

```cpp
Node* ret_node()
{
    Node node = Node();
    cout <<"node inside addr:"<<&node<<endl;
    return &node;
}

int main()
{
    // 对被回收的对象解引用本身就是危险的！
    Node node = *(ret_node());
    cout << "outside node addr:" << &node << endl;
    // node再次被析构也是危险的！
}
```

结果是：

```
new
node inside addr:0x7fff548910a7
delete
outside node addr:0x7fff548910d7
delete
// node只被构造了一次，但析构了两次！
// 如果node具备堆上申请空间的数据成员，执行两次析构函数意味着segmentation fault！
// 然而，对被回收的内存解引用本身就是危险的！
```

答案是绝不。并且在你尝试编译返回栈上对象地址或指针的程序时，g++会警告你：

```
warning: address of local variable ‘node’ returned [-Wreturn-local-addr]
```

> 这不是primer的内容，但是笔者在这里给出解释。

> g++在做某种“偷懒”的行为(或者说是右值引用？)。事实是，你返回了一个在栈上申请的对象，按照标准，它应该在离开作用域后被回收，并重新申请空间，拷贝这个对象，以供外部访问。

> 但是既然它（因为你的返回语句）被外部取得了，g++貌似选择了直接将它的内存空间的管理权限移交给外部(我们的main函数)，这就节省了重新申请内存，并对Node调用拷贝构造函数的开销。

> 这是编译器的优化选择，但你不能依赖于它，因为这不是标准的一部分。标准从来没有承诺，你return的局部栈上变量的地址不会变化。

> 当我们尝试(恶意地)去利用这一特性时，却没有得到预期的结果。在我们返回引用时，局部对象被回收了。我们的小聪明失败了。这很好。
> 但我们还是要多问一句，为什么在返回引用的版本，析构函数被调用了两次呢？  
> 我猜测和(右值引用)的判断有关。之前的优化逻辑只在用户尝试返回一个较大内存占用的对象时作用，但如果用户返回了一个地址，那拷贝与重新申请空间的开销显然不太大。此时，局部的变量离开了作用域，当然会被回收。返回了一个地址，使得没有调用Node构造函数的必要。
> 但在外部看来，我们从一个地址(我们不知道该地址是否有效)解引用(在这里，解引用本身就是危险的！)取得了一个对象，该对象的作用域在我的栈上，当栈结束时，当然应该析构。这样，加起来就调用了两次。

虽然我的编译器做了这样(右值引用)的优化，但是这是聪明的编译器才会做的，笨蛋编译器不会优化，他们会诚实地申请空间，拷贝对象，再析构栈对象，再返回新构造的对象。这样显然效率很低。因此：  
**建议：** 不要返回大对象(数组或自定义对象)，如果编译器没有右值引用，申请空间并拷贝开销很大。请用参数传入指针或数组的方法返回结果。\

### 返回结果可能是左值

```cpp
char &get_val(string &str, string::size_type idx){
    // 返回idx处值的引用
    return str[idx];
}
int main(){
    string s("123456");
    get_val(s, 0)='A';
}
```

### 返回列表初始化

```cpp
vector<string> get_string(){
    return {"abc", "def"};// 这是被允许的
}
```

### 函数重载

只有函数形参列表构成重载，**不能根据返回值重载！**  
const的重载：
**顶层const不能重载(是否为常指针或常量)，底层const(指向的是常量)可以重载.**

```cpp
int ret_val(int num);
int ret_val(const int num); // 不构成重载

int ret_val(int *num);
int ret_val(const int *num);// 可以重载
```

注意，如果同时定义了引用与常量引用，指针与const指针的两类函数，此时，规则“使用实参初始化形参时，会忽略顶层const。”，不再发挥作用。变量会调用变量版本，const会调用const版本：

```cpp
void show_msg(int &num){
    cout<<"normal show_msg with "<<num<<endl;
}

void show_msg(const int &num){
    cout<<"const int show_msg with "<<num<<endl;
}
int main(){
    int num=42;
    const int val=88;
    show_msg(num);
    show_msg(val);
}
// 结果
// normal show_msg with 42
// const int show_msg with 88
```

如果注释掉常量版本，又回到之前省略形参const的时候了：

```
const int show_msg with 42
const int show_msg with 88
```

### const_cast与重载：格外有用

我们常常需要为参数的const版本和非const版本提供重载，这里提供一个绝佳的实践：让非const版本调用const版本，并通过const_cast增减const。
> 这里也说明了const_cast的作用并不仅仅是减去const，它同样可以追加const。

```cpp
// 比较两个string对象的长度，返回较短的
const string &shorter(const string &s1, const string &s2){
    return s1.size()<=s2.size()? s1:s2;
}

// 非const版本，通过const_cast加减const并调用const版本
string &shorter(string &s1, string &s2){
    // 这里也可以写作 auto &r=...
    const string &r=shorter(const_cast<const string&>(s1), const_cast<const string&>(s2));
    return const_cast<string&>(r);
}
```

> 这是const_cast的绝佳使用，也说明强制类型转换并不总是坏的。  

### 默认实参

只出现在声明式中，多次声明对同一个形参只能配置一次默认实参。  

### 内联函数

inline是对编译器的一个请求，编译器可以选择忽略这个请求。  

### constexpr函数

能用于常量表达式的函数。  
函数的返回值和形参必须是字面值类型（包括算术类型，引用和指针）（不包括自定义类，string等）。  
constexpr函数的返回值不一定是常量表达式，如果将它赋值给constexpr，编译器会为你提供检查。  

### 为什么将inline与constexpr函数定义在头文件中？

- 必要知识

inline与constexpr函数都是编译期函数。  
编译期函数理论上(即按照标准)可以被定义多次，但是多次定义的内容必须完全相同。  
> 实际不行，如果你尝试复制一个肯定会被展开的inline函数(甚至通过__attribute__((always_inline))保证一定展开)，GNU还是会告诉你重定义的，别想钻空子...编译器比你狡猾多了

我们很少将非编译期函数定义在头文件中，因为如果这个头文件被多次包含，就会出现重定义的问题。  

- 正文

现在，我们希望一个函数被多个cpp文件使用，并且希望它被内联展开，此时，在头文件中做该函数的声明，并在某一个cpp文件中进行该函数的实现，这样的做法，能达到我们的目的吗？  
答案是不能。inline是编译期的，如果编译器不能立即知道函数的实现(定义)，而要等到链接器阶段才能链接到函数实现。那假设编译器决定对该函数在定义文件中内联展开，你在别的地方对该inline函数的调用将undefined reference。  
如果它没有被展开，那你定义inline也就没啥用...
> 按照标准，应该是这样解释的。但是在GNU中，即使它最终没有被展开（例如通过inline \_\_attribute\_\_((noinline))阻止）或者使用O2以下的优化(不含)，你依然会得到undefined reference。  

> 因此，extern地利用inline函数，实际上是被GNU阻止的。即使加extern都没用。  

为什么会这样？  
**分开编译，一起链接。** 编译器总是分别编译各个cpp文件，让链接器将他们链接起来。现在，你在func.cc中定义了一个inline函数（而不是头文件），并在main.cc中include func.h，并调用inline函数。  

```cpp
// func.h
inline void a_inline_func();
// func.cc
#include "func.h"
inline void a_inline_func(){
    std::cout<<"a inline func msg"<<std::endl;
}
// main.cc
#include "func.h"
int main(){
    a_inline_func();
}
```

预处理器为main.cc引入了inline函数的声明，编译器编译了main.cc，它发现inline函数的声明，并期待链接器能找到一个函数实现。  
编译器编译了func.cc函数，发现有函数是inline的，决定对它做inline展开，它在它当前能获取的范围内（即本cpp文件内）展开了该函数，**并不保存该函数的实现体**。  
链接器开始链接两个cc文件的实现，main.cc要求inline函数的实现，但是链接器已经不能在func.cc中找到实现了。（因为被展开了。）
这就会导致链接器抛出undefined reference。  
如果你希望定义的函数只在本cpp文件中使用，像一般函数一样，写在本cpp文件中，声明static即可。  
对同为编译期作用的constexpr，情况是一样的。

### 为什么最好不要单独使用inline，而要static inline？

> 本节只是给出一种可能性的说明，以说明为何static inline是最佳实践。GNU在实现时做了更复杂的策略，使得本节的理论无法进行实验。

> 我们只能说，static inline增加了inline被展开的可能。（因为杜绝了extern调用）。事实上，如上节所述，GNU本来就是阻止extern地调用inline的。你加上static，不会有任何损失。

> 不要小看编译器。

> 本节是笔者写的，不一定是对的。

看了上一节，我们决定将inline函数的实现体放在.h文件中，这样，它被内联展开了吗？  
答案是有可能没有，但等等，这不是因为它可能太复杂，不便inline，而是因为它可能是extern的。  

inline是对编译器的建议，编译器可以不接受它。如果一个inline函数不是static的，意味着用户可能在extern作用域引用它，假如我(编译器)选择将这个函数inline了，那可能的extern还怎么获取这个函数的定义？我(编译器)当然不能背这个锅！所以，对于一切不是static的inline，对编译器而言的最简单策略是，都不进行inline。  

> 参考GNU文件6.39 [An Inline Function is As Fast As a Macro](https://web.mit.edu/rhel-doc/3/rhel-gcc-en-3/inline.html)

> When an inline function is not static, then the compiler must assume that there may be calls from other source files; since a global symbol can be defined only once in any program, the function must not be defined in the other source files, so the calls therein cannot be integrated. Therefore, a non-static inline function is always compiled on its own in the usual fashion.

> 如果参考这个文档里的说明，单独的inline将永远不会被展开，但这是违反事实的，GNU并没有那么笨，(如果它很笨就好了，方便我们的实验)。笔者做了实验，单纯的inline是可能被展开的。

> 我们来考虑一下，什么情况下，inline关键字可以被单独使用，以说明为什么你应该永远使用static inline。

> 如果实现体在头文件中（多文件使用），你写下inline，说明你希望被内联展开，此时加static将增加它被内联的概率（如果编译器决定为了extern考虑，不展开所有非static的inline得话）  

> 如果实现体在cc文件中（只有本文件使用），你可以单独使用inline了，此时编译器可能展开，或者不展开该inline函数。  
此时有个不懂inline的程序员看到了你的代码，他发现你的inline函数不是static的，他决定在他新增的代码文件中直接使用该函数。(因为他没有被static声明，是extern的！)。假如编译器展开了你的inline函数，这个可怜的人将会发现undefined reference！但他不明白，这不是extern的吗？  
> 如果编译器没有展开，并允许extern调用了，那更糟糕，他会认为inline的函数都是可以extern使用的，假设有一天公司换了编译器，新编译器决定对你的函数进行inline展开了（或者不允许inline的extern调用了），将会出现undefined reference...
而如果你一开始就写下static inline，暗示该程序员，别xjb用我的内部函数，也许就不会出现这这样的问题了。

综上所述，你亘古不变地应该使用static inline，没有例外！  
> 有一个例外，你在声明一个类的成员函数，且希望它被内联。你不能将它声明为static的，这将使它成为类函数而失去this指针。  

> 或者你可以在函数附近写下注释：

```cpp
// 别在外部使用这个函数！
inline void My_inline_func(){
    ...;
}
```

> 这样也能满足你单独使用inline保留字的(奇怪)欲望...

- 附带

如果你想确定一个函数是否被内联展开了，添加编译参数-save-temps=obj，这将保留预处理器结果.ii，编译器结果.s，链接结果.o。
**注意：** 只有使用-O2以上的优化(含)时，才会进行内联展开。  

### assert与调试

assert定义在头文件cassert中，是一种预处理宏，它在debug中被开启，用于检测用户定义的程序执行情况是否符合预期。  
assert依赖于NDEBUG预处理变量，如果定义了NDEBUG，assert将什么也不做。  
当开启release时，就开启了NDEBUG。  
借助这个预处理变量，你也可以写一些只在debug时执行的代码。  

```cpp
#ifndef NDEBUG
// __func__是编译器定义的局部静态变量，用于保存当前函数的名字
cerr<<__func__<<endl;
// __FILE__ 保存文件名
// __LINE__ 保存当前行号
// __TIME__ 保存文件编译时间
// __DATE__ 保存文件编译日期
```

### 选择哪个重载函数

由于重载和函数默认值的提供，匹配调用与函数重载的逻辑是比较复杂的，大体上是匹配最优的或最接近的。  
但有时候还是会出现重载二义性，即编译器无法决定使用哪个函数。

### 函数指针

函数指针指向的是函数而非对象。  
函数指针具备某种类型，类型由函数的返回值和形参类型共同决定，与函数名无关。  
示例：

```cpp
// 函数
bool length_compare(const string&, const string&);

// 指针
bool (*pf)(const string&, const string&); 
// 这样就能声明一个函数指针
// pf两端的括号必不可少，否则它将成为函数定义。
```

- 使用

```cpp
// 可以直接将函数名赋给指针
pf = length_compare;
// 或者取函数地址
pf = &length_compare;
// 或者nullptr/0;

// 调用
// 可以直接使用函数指针调用
bool b1 = pf("hello", "helloworld");
// 或者解引用调用
bool b2 = (*pf)("hello", "helloworld");
```

**你可以将函数指针作为函数参数使用，这就是C++将函数视为对象的方法**  

```cpp
// 与数组类似，直接传入一个函数是可以的，它会被视为指针
void exec(bool pf(const string&, const string&));
// 或者传入一个指针
void exec(bool (*pf)(const string&, const string&));
```

写这样冗长的声明太糟糕了，可以替换为：

```cpp
// 注意decltype返回的是函数，*必不可少
typedef decltype(length_compare) *Func; 
// 将exec重定义为：
void exec(Func fucn);

// 或者直接写成：
void exec(decltype(length_compare) func){}
// 或
void exec(decltype(length_compare) *func){}

// 调用
exec(length_compare);
```

- 作为返回值（返回一个函数指针）
定义

```cpp
using F = int(int*, int);  //F是函数类型，不是函数指针类型
using PF = int(*)(int *, int); //PF是函数指针类型

PF ret_ptr(){}
// 或:(不推荐这一写法)
int (*ret_ptr())(int*, int){}
```

根据定义方法的不同，调用方法也有不同

```cpp
PF f1(int);
// 或
F *f1(int);
// 或者不使用using：
int (*f1(int))(int*, int);
// 更清晰的写法是
auto f1(int) -> int(*)(int*, int);
```

**函数指针的最佳实践**  
> 这是笔者本人提供的。

同时有typedef和using，可以起别名或者不使用别名，函数指针的语法规范是难解的。  
为了更好的可读性，这里提供一种最佳实践：  
使用using定义函数别名，并始终使用该函数别名。  

```cpp
// 一个接受两个int，返回一个int的函数
int get_bigger(int a, int b){
    return a>b?a:b;
}
// 定义别名
// 如果存在已有函数
using Func=decltype(get_bigger);
// 如果不存在一个已有函数
using Func=int(int, int);

// 存在对Func别名的三种使用：
// 作为函数形参
void exec(Func* func){}
// 作为函数返回值
Func* get_func_ptr(){}
// 构造实参, &可加可不加.
Func* func_ptr=&get_bigger;
```

## 第七章 类

### this

与python的self一样，this是指向当前对象的指针，可以在C++类定义内部使用。  

```cpp
class Counter {
 public:
  Counter() {}
  void add() { this->nums += 1; }
  int nums = 0;
};
// 调用
// 在栈上创建对象的方法与python一样，只是多一个类型
Counter counter = Counter();
// new创建
Counter *counter_ptr = new Counter();
delete counter_ptr;
counter_ptr=nullptr;// 这样回收指针指向的空间，不是delete *counter_ptr;
// delete后面是地址。
```

### const成员函数

const成员函数禁止修改类的数据成员，通过后置const声明。  
如果一个成员函数不进行对数据成员的修改，你就应该将它声明为const成员函数。例如一些打印信息的方法。  

```cpp
class Counter {
 public:
  Counter() {}
  // 加在函数参数列表之后
  // 此时修改this->nums是非法的
  // 注意是const后置而不是前置，前置将是成员函数返回值的一部分。
  void add()const { this->nums += 1; }
  int nums = 0;
};
```

将add声明为一个const成员函数非我们所愿，优化为:

```cpp
class Counter {
 public:
  Counter() {}
  void add(){ this->nums += 1; }
  int get_nums()const{return this->nums;}
 private:
  int nums = 0;
};
```

常量对象，常量对象的引用，指向常量对象的指针，都只能调用const成员函数。  
const成员函数，或者不是const的成员函数，可以以此进行函数重载。  

### 在类的外部定义函数

成员函数的声明一定要在类体内，但可以在外部定义。  
规范是：  

```cpp
// 类型 类名::方法名(方法参数列表) [const]{}
int Counter::get_nums()const{
    return this->nums;
}
```

### 返回this

可以让add方法返回this:

```cpp
Counter& Counter::add(){
    this->nums+=1;
    return *this;
}
```

这方便于连续调用方法：

```cpp
counter.add().add().add();
```

返回引用对于连续调用方法是必须的，如果返回值是Counter，相当于：

```cpp
// 这将创建对counter的浅拷贝
Counter tmp = counter.add();
```

### 构造函数

构造函数不能是const的。  
如果定义了一个构造函数，编译器就不会生成默认构造函数。最佳实践是，总是显式地定义构造函数，即使什么也不做。  
> 如果一个类在某种情况下需要控制对象初始化，那么该类很可能在所有情况下都需要控制。  

```cpp
// 快捷显式定义构造函数
class Node{
    public:
        Node() = default;
}
```

- 使用初始化列表

初始化参数列表是被effective推荐的最佳实践，这将只有初始化一个开销。  
如果你使用赋值的方法，需要先进行初始化，再进行赋值，开销比较大。  
对const数据成员，只能通过初始化参数列表进行初始化，而不能通过在构造函数中赋值。  

```cpp
class Student
{
public:
    // 语法：
    // 类名(形参列表):属性1(形参1), 属性2(形参2)...{}
    // 形参可以与实参的名字相同或不同，编译器能正确区分他们.
    Student(const std::string name, const unsigned int age, const unsigned int id, float score) : name(name), age(age), number(id), score(score) {}
private:
    const std::string name;
    const unsigned int age;
    const unsigned int number;
    float score;
};
```

### 拷贝、幅值与析构

编译器会生成默认的拷贝赋值与析构函数，但默认的函数并不总是有效的，尤其在类内存在动态内存分配时，要保证正确地回收对象的内存，必须自行定义析构函数。  
在需要深拷贝的情况下，默认的拷贝构造函数也不能作用。  
TODO：等待后续补充。

### struct

除了语法,struct与class唯一的区别在于struct的默认权限是public的,class则是private的。  
> 在C++中，不需要使用struct。

### 友元函数

我们希望我们定义的一些函数能否访问类的私有成员或函数，可以将这些外部函数声明为友元函数。  
> 不要这么做，这在破坏封装性.  

```cpp
class Student
{
public:
    friend void show_info(const Student* ptr);
private:
    const std::string name;
    const unsigned int age;
    const unsigned int number;
    float score;
};
void show_info(const Student* ptr)
    {
        std::cout << __func__ << "\n name:" << ptr->name << " age:" << ptr->age << " number:" << ptr->number << std::endl;
    }
```

### 友元类

与友元函数类似，这将允许友元类访问本类的私有成员。

```cpp
class Teacher{
    public:
        void show_info(const Student* ptr)
        {
            std::cout << __func__ << "\n name:" << ptr->name << " age:" << ptr->age << " number:" << ptr->number << std::endl;
        }
};
class Student
{
public:
    friend class Teacher;
    // 可以只赋予teacher的show_info方法友元权限，但这要求方法必须先声明。
    // friend void Teacher::show_info(const Student*);
    // 如果要赋予友元的函数进行了重载

private:
    const std::string name;
    const unsigned int age;
    const unsigned int number;
    float score;
};
```

### 内联的成员函数

如果一个成员函数不是类成员函数，那应该使用inline而不是static inline，static声明将使得函数失去this指针。

```cpp
class Node{
    public:
        Node(int number, string name):number(number),name(name){}
        // it's ok
        inline void show_info(){
            cout<<"number:"<<this->number<<" name:"<<this->name<<endl;
        }
        // illegal:class function don't have this ptr;
        // static inline void show_info(){
        //     cout<<"number:"<<this->number<<" name:"<<this->name<<endl;
        // }
    private:
        int number;
        string name;
};
```

### mutable

当你希望一个数据成员可以被const成员函数修改时，将它声明为mutable的。  

```cpp
class Node{
    public:
        Node(int number, string name):number(number),name(name){}
        void set_name(std::string new_name)const{
            this->name=new_name;
        }
    private:
        int number;
        mutable string name;
};
```

### 类成员初始值

希望为类的数据成员提供初始值时，必须使用=或花括号{}。  
这是说，你不能使用()。

```cpp
class Node{
    public:
        // error:
        // string name("Node");
        string name{"name"};
};
```

### 委托构造函数

构造函数将部分构造功能委托给另一个构造函数，这就是委托构造函数。  
用在提供多种构造函数时，存在部分数据成员的初始化方法相同。  

```cpp
class Node{
    public:
        Node(string name, int num):name(name), num(num){}
        Node(string name):Node(name, 0){}
        // 但是，这可以通过给上一个构造函数默认值来完成...
    private:
        string name;
        int num;
};
```

### 转换构造函数与隐式的类类型转换

如果一个构造函数只定义了一个参数，那它实际上是一个转换构造函数。  
这十分有用，在函数要求类型时，可以将那个参数的类型给进去。  
> 这也帮助我们理解隐式转换的实质，只不过是构造函数而已，编译器帮你顺手做了一下构造。  

> 这也解释了为何有时不能进行隐式转换，必须进行显示转换：要转换到的类，没有提供对应的单参数构造函数（转换构造函数。）

```cpp
class Node{
    public:
        Node(string name):name(name){}
        string name;
};

void show_name(const Node &node){
    cout<<node.name<<endl;
}

int main(){
    string s{"我下午要玩戴森球计划"};
    show_name(s);
}
```

### 使用explicit阻止隐式的类型转换

很多时候我们不想单参数的构造函数用作转换构造函数，即，我们不希望隐式地创建对象。要阻止编译器为你做这样的转换工作，在**声明**单参数构造函数时，添加explicit声明。  
Note：

- explicit只对单参数构造函数有用。
- 只能放在函数声明处，不能放在定义处。
- 如果在声明处定义，也ok。
- explicit不会阻止显式的构造或强制类型转换

```cpp

class Node{
    public:
        explicit Node(string name):name(name){}
        string name;
};

void show_name(const Node &node){
    cout<<node.name<<endl;
}

int main(){
    string s{"我下午要玩戴森球计划"};
    // error:
    // show_name(s);
    Node node = Node(s);
    show_name(node);
    show_name(Node(s));
    // 但是允许显式的强制类型转换
    show_name(static_cast<Node>(s));
}
```

转换构造函数允许一步转换，但是不会允许多步转换。假设有一个函数需要std::string，你可以用字面值const char\*来作为实参。  
我们上面例子的show_name接受Node类型，如果没有explicit声明，它可以接受一个std::string，但是不能接受一个const char* 字面量。那就是两步转换了。  

### 聚合类

允许用户直接访问其成员，且具备特殊的初始化语法。满足以下特点：

- 所有成员都是public的
- 没有定义任何构造函数
- 没有类内初始值
- 没有基类，也没有virtual函数。

> 不必记忆它不是什么，最好记忆它是什么。聚合类表现为一组数据成员的组合，可以通过花括号{}进行初始化。  

```cpp
class Data{
    public:
        string name;
        long long id;
};
// 或者使用struct,好处很明显，你不用打public了。
// 这可能是struct唯一在c++的作用。
Data data = {"pudding", 114514};
```

### constexpr构造函数

构造函数可以用constexpr修饰，随后，它必须初始化所有数据成员。  
> 弄不懂何时使用。

TODO:constexpr构造函数

### 类的静态成员

类的静态成员函数不能获取this指针，也不能被声明为const的。
可以通过对象或类来访问静态成员。  
静态成员在类内是直接可见的，不用通过this等访问。  

可以在类的内外定义静态成员函数，但在外部定义时，不能重复static关键词。（就像你不能重复explicit关键词一样）  
你不能在类内直接为一个static数据成员初始化，除非它是const的。

```cpp
class Node{
    public:
        const static int num=1;
        static int id;
};

int Node::id=1;
```

静态成员可以作为默认实参，但对象的成员不可以，因为对象的成员属于对象。  

# 第Ⅱ部分：C++标准库

## 第八章：IO库

### 三种IO流类型

- iostream IO流
- fstream 文件流
- sstream 字符串流

宽字符(wchar_t)使用的是wcin, wcout和wcerr。

### 文件输入输出

读写文本文件：

```cpp
#include<iostream>
#include<fstream>
#include<string>
using namespace std;

int main(){
    fstream in("input.txt");// ifstream也可以
    ofstream out("output.txt"); // ofstream打开，覆盖写,如果是fstream打开，则不清空，光标从0号位置开始写。
    string s;
    while(getline(in, s)){
        out<<s<<endl;
    }
    in.close();
    out.close();
}
```

由于ofstream打开文件时一定会清空文件，因此追加写需要显式指定：

```cpp
#include<iostream>
#include<fstream>
#include<string>
using namespace std;

int main(){
    fstream in("input.txt");
    ofstream out("output.txt", ofstream::app);
    string s;
    while(getline(in, s)){
        out<<s<<endl;
    }
    in.close();
    out.close();
}
```

文件流常用三个方法：

- fstream.open("filename.txt")
- fstream.good() 或fstream.is_open()
- fstream.close()

### 读写二进制文件

如果希望将自定义结构的数据保存到外存的二进制文件中，那么自定义结构不能包含可变长度类型，例如各种stl容器。  

下面的例子就要求结构体Student的char数组是固定长度的。

```cpp
// 写
ofstream out("out_bin.bin", ofstream::binary);
Student ns={"大BOSS", 18, 1001};
out.write(reinterpret_cast<char*>(&ns), sizeof(ns));
out.close();

// 读
ifstream in("out_bin.bin", ifstream::binary);
Student ns;
in.read(reinterpret_cast<char*>(&ns), sizeof(ns));

struct Student
{
    char name[30];
    int age;
    int number;
};// ok

struct Student
{
    string name;
    int age;
    int number;
};// core.
```

### 使用字符串流sstream

sstream有好处：由于流的特点，可以简单地用空格分割，并将他们赋予不同的变量，以下是一个例子。

```cpp
#include<iostream>
#include<sstream>
#include<string>

using namespace std;

int main(){
    stringstream ss("BigBoss 22 2022");
    string name, year;
    int age;
    ss>>name>>age>>year;
    cout<<name<<" "<<age<<" "<<year;
}
```

stringstream相当于fstream，也可以用istringstream或ostringstream。  
sstream的方法：

- strm.str(); 返回sstream返回中的字符串。
- strm.str("some string"); 将string绑定给流，返回void;

## 第九章：顺序容器

### 顺序容器类型与特点

|名称|特点|
|---|---|
|vector|可变大小；随机访问；尾部操作快|
|deque|双向队列;随机访问；头尾操作快|
|list|双向链表;双向顺序访问；任何位置操作都快|
|forward_list|单项列表；单向顺序访问；任何位置都快|
|array|固定大小；随机访问；不能增减元素；|
|string|与vector类似，专注于保存字符；尾部操作快|

**使用建议**:

- 一般情况下，vector一把梭。
- 链表(list/forward_list)的空间占用较大，避免在空间敏感时使用。
- deque也很常用。

### 所有容器都支持的操作

- 容器都定义在与它的名字一样的头文件中，如deque定义在deque头文件中。
- 容器都是模板类，在声明时需要给出d_type；box\<d_type\>

**构造函数**

```cpp
Box box; //空容器
B b1(b2); //拷贝构造，深拷贝
B b1=b2; //初始化，深拷贝
B b3(s, e); //将迭代器s和e范围内的元素拷贝到b3中
B b4{a,b,c...}; // 列表初始化
```

> 令人吃惊的是，容器类的()与=构造都是深拷贝，且是完全的深拷贝。即对于d_type为自定义类型，且类型内包含传统数组的情况，也会支持深拷贝。非常可靠。

**常用方法**

```cpp
a.swap(b); //交换a,b容器的元素
// or swap(a, b)
a.size();
a.empty();

// 增删元素
c.insert(args); // 拷贝args进c里。
// 对于vector: v.insert(v.begin(), 12345); 第一个参数是const迭代器
c.erase(args); // 删除指定元素
// 常见两个重载，v.erase(v.begin()+i) or v.erase(v.begin(), v.end());
c.clear(); // 清空

c.front();// 返回首元素的引用。除了array都有
c.back();//返回尾元素的引用，除了forward_list都有。
// 因为是引用，所以front和back都可以作为左值使用.
// 两个方法对空都是不安全的，属于未定义行为。
```

### 容器的迭代器

```cpp
auto it1=a.begin();
auto it2 = a.rbegin(); // 反向迭代器，从最后一个元素开始，使用++访问上一个元素
auto it3 = a.cbegin(); // const迭代器，不允许修改元素;
auto it4 = a.crbegin(); // 反向const迭代器
```

### 顺序容器支持的操作

```cpp
// array不支持这些操作
// forward_list 有自己专属版本的insert和emplace;
// forward_list 不支持push_back和emplace_back;
// vector和string 不支持 push_front和emplace_front

c.push_back(t); // 除了array和forward_list外，每个顺序容器都支持push_back；包括string。

c.pop_back();
c.pop_front();

// C++11新支持了emplace系方法. push_back在添加元素前会先创建这个元素，再将元素移动到容器中，而emplace_back添加元素时，是直接在尾部创建这个元素，相对来说效率更高。
c.emplace_back(t);

c.insert(p, t);// insert方法返回指向p位置的迭代器.
//因此可以放在循环里，不断向特定位置插值
c.emplace(p, t);

c.push_front(t)// list, forward_list, deque支持front追加。forward_list顾头不顾尾.
// vector充当了栈，deque则两头.
```

### emplace与push的性能讨论

emplace 比 push省去了拷贝这一步，但如果对象是已经创建好的，则效率是一致的。  
只有在触发转换构造函数，或者C++内置类型时，会有较大的收益。  

```cpp
#include<iostream>
#include<vector>
using namespace std;

class Node{
    public:
        Node(int n):num(n){
            cout<<"构造函数"<<endl;
        }
        Node(const Node &other):num(other.num){
            cout<<"拷贝构造函数"<<endl;
        }
        Node(Node&& old):num(old.num){
            cout<<"移动构造函数"<<endl;
        }
        int num;
};

int main(){
    vector<Node> vns;
    cout<<"效率相等的情况：先创建对象，再放入容器"<<endl;
    cout<<"push_back:"<<endl;
    vns.push_back(Node(12));
    cout<<"------\n"<<"emplace_back:"<<endl;
    vns.emplace_back(Node(42));

    cout<<"---------\nemplace_back效率高的情况：\n";
    cout<<"push_back:"<<endl;
    vns.push_back(12);
    cout<<"emplace_back:"<<endl;
    vns.emplace_back(42);
}
```

执行结果是：

```
效率相等的情况：先创建对象，再放入容器
push_back:
构造函数
移动构造函数
------
emplace_back:
构造函数
移动构造函数
拷贝构造函数
---------
emplace_back效率高的情况：
push_back:
构造函数
移动构造函数
拷贝构造函数
拷贝构造函数
emplace_back:
构造函数
```

> 第一种情况让人感到费解，emplace_back多调用了一次拷贝构造函数。它的效率比push_back更低了。  

> 第二种情况当然是符合期望的，也是emplace_back能大幅取得收益的地方。  

> 因此，不能说emplace_back总比push_back好。事实上，除非你能通过定义转换的形式(单参数ok，多参数也ok)，保证emplace_back更好，否则还是push_back一把梭吧。

### 使用resize

可以使用resize调整容器的大小，向其中加入指定元素来填充，或删除部分元素。

```cpp
c.resize(n) //将c的大小调整为n，超过则删除后面的，不足则用0补齐。
c.resize(n, num)// 不足用num补齐。
```

> resize是有些危险的，如果缩小容器，可能导致指向被删除元素的迭代器，引用和指针失效。

使用指向容器类型的指针是危险的，如果容器增加或删除了元素，引起了存储空间的重新分配，指针可能会失效。
> 这么说，为什么我们当时使用的vector都使用了shared_ptr呢？

> **警告**：不要保存end返回的迭代器。对容器的任何添加或删除操作都会使得end迭代器失效。希望通过begin!=end来遍历容器时需要在每次循环时都调用end()，而不是先保存它。

### 管理vector的扩张

vector总是申请比它当前需要的元素多一些的空间，以应对随时可能到来的push_back。  
可以使用一定的方法告知vector准备多少空间，以改善程序性能：

```cpp
// 将capacity()减少到size()大小，相当于避免占用多余的空间.
// 对于d_type很大，且空间敏感时，在程序的最后调用一下这个方法很好.
// 但这依然是一个请求，请求编译器在这里退回多余的容器空间。因为是请求，所以不一定会被执行.
c.shrink_to_fit();

c.capacity();// 当前不引起重新内存分配的最大容量.
c.reserve(n);// 分配n个元素的内存空间
// reserve会至少分配n个元素的内存空间，不过有可能更大.
```

### 额外的string操作

```cpp
// 构造函数
string s(cp, n);// cp数组中前n个元素的拷贝
string s(s2, pos2);// 对s2的，从pos2开始的元素拷贝
stirng s(s2, pos2, len); //对s2的，从pos2开始的，len个元素的拷贝
```

```cpp
// sub_str
s.substr(pos, len) // 注意第二个参数是len，不是pos，与切片不同！

//insert-erase
s.insert(s.size(), 5, '!'); //末位加入5个!
s.erase(s.size()-5, 5); // 删除末尾的5个元素

const char *str="Hello World";
s.assign(str, 5);// s=Hello；

// append与replace
s.append("abcde"); //append在末尾追加字符串,push_back只能放入一个字符.
s.replace(0, 3, "abcdes");// 从0号位置开始删除3个元素，替换为abcdes。
```

```cpp
// 搜索
// 如果搜索失败，返回string::npos
string s1="abcdes";
s1.find("abc") // rst=0, 注意，这是一个unsigned!最好不要用int这样的有符号类型保存它.
// 推荐用auto？

// 寻找与任何字符匹配的第一个位置
string res="abcdefg123890";
res.find_first_of("0123456789");// 相当于返回第一个数字所在的索引.

// 寻找与给定字符不匹配的第一个位置
res.find_first_not_of("0123456789");

// 其他
s.rfind() // 最后一次出现
s.find_last_of(); //倒着找
s.find_last_not_of(); 

// 一个示例：每步循环查找字符串中的下一个数字
string::size_type pos=0;
string s2="ab12cd34ef56ppos";
while((pos=s2.find_first_of("0123456789", pos))!=string::npos){
    cout<<pos<<" "<<s2[pos]<<endl;
    ++pos;
}
```

```cpp
// 字符串的数值转换
int i=42;
string s=to_string(i);
double d=stod(s);

to_string(val);// 几乎所有的内置数据类型都有
stoi(); // int
stol(); // long
stoul(); //unsigned long
stoll(); // long long
stoull(); // unsigned long long
stof(); // float 
stod(); //double 
stold(); // long double
```

### 容器适配器

C++有三种容器适配器。所谓容器适配器，是指可以由容器伪装的一种类型，表现出适配器类型的特点。  

- stack
- queue
- priority_queue

> 适配器只有空构造函数，和从基础容器的构造函数。这是说，你不能通过{}来初始化他们。

> 不能使用auto迭代，没有begin和end方法。

> 从功能上，适配器是带有限制的基础容器。

**stack**

```cpp
// 不太理解什么场景会用stack。
// 因为vector可以完全替代它的作用.
#include<stack>
#include<deque>
#include<vector>
using namespace std;

int main(){
    deque<int> deq{12,3};
    vector<int> vec{4,5,6};
    // 适配器可以用一些基本容器类型初始化
    // 奇怪的是，stack不能用vector初始化...
    stack<int> sk(deq); 
    sk.push(123);
    int top=sk.top();//返回栈顶元素
    sk.pop(); //pop没有返回值
}
```

**queue与priority_queue**

本节在cxx_primer中的叙述很奇怪，可能是有所错误。  
书330页底部关于队列适配器的叙述，说q.pop()不删除元素，且有返回值，但这是不正确的。测试代码如下：

```cpp
#include<queue>
#include<deque>
#include<iostream>
using namespace std;

int main(){
    deque<int> deq{1,2,3};
    queue<int> que(deq);
    
    while(!que.empty()){
        cout<<que.front()<<endl;
        que.pop();// 返回值是void的！
    }
}
```

以下给出优先队列的常见使用：

```cpp
#include<queue>
#include<vector>
#include<iostream>
using namespace std;

int main(){
    vector<int> vec{4,3,6,7,8};
    priority_queue<int> pq(vec.begin(), vec.end());
    pq.push(1024);
    pq.push(42);
    pq.push(2048);
    while(!pq.empty()){
        cout<<pq.top()<<endl;
        pq.pop();
    }
}
// output:
// 2048
// 1024
// 42
// 8
// 7
// 6
// 4
// 3
```

优先队列默认是从大到小的（大根堆）。  
要声明一个小根堆，需要：

```cpp
priority_queue<int, vector<int>,greater<int>> pq(vec.begin(), vec.end());
```

这是priority的完整声明，第一个参数是d_type，第二个是实现优先队列的底层容器类型，这里用了vector，第三个是比较两个元素之间的函数。一般有std::less和std::greater。greater代表从前到后，依次greater。

## 第十章：泛型算法

本章的重点在算法，而不是对用户如何定义泛型的讲解。主要介绍定义在头文件algorithm中，以及一些数值泛型操作，定义在numeric中。  

但泛型算法的“泛型”也十分重要，它意味着算法并不作用于特定容器之上，在下面可以看到，泛型算法总是作用在容器的迭代器上。  
因此，泛型算法一定不会改变容器的大小。尽管它有可能改变元素的值。  

> 因为你知道，在使用迭代器遍历容器时，增删元素是危险的。

### 一个好的例子：find与count

algorithm中的find可以作用在标准库容器或C数组上，返回一个迭代器。

```cpp
#include<algorithm>

int val = 42;
// result 是一个迭代器，使用autou最好
auto result = find(vec.begin(), vec.end(), val);
// count则返回出现的次数.
int rst = count(vec.begin(), vec.end(), 5);
// 如果找不到result == vec.end()
```

### 只读算法

上面的count和find就是只读算法。同使用类型的包括：

- count: 统计范围内特定元素的个数.
- find: 查找特定范围内的第一个元素.
- accumulate: 对特定范围求和。（第三个参数是求和初始量，也决定了使用哪种加法，以及返回值类型）

> 如果你对string类型调用accumulate，那么就会造成拼接。

> 你不能这样写：string sum = accumulate(v.begin(), v.end(), "")，因为const char*上没有定义加法运算符。

> 你需要把它修改为string("").

- equal: 比较两个容器的元素值是否完全相等。参数分别为：第一个容器的begin，第一个容器的end，第二个容器的begin。

> equal可以从第一个容器的begin和end推测出应该遍历多少次第二个容器。因此，你需要保证第二个容器至少含有那么多元素。  

### 写容器元素

- fill: fill(vec.begin(), vec.end(), 0); 用第三个元素给各位置赋值。
- fill_n: fill_n(vec.begin(), n, 0); n标志了移动多少次.

fill_n要求程序员确保n位空间已申请且可访问。如果没有，那么结果是未定义的。  

### back_inserter

back_inserter定义在interator头文件中。它接受一个容器的引用，返回一个与该容器绑定的插入迭代器。  
之后，给该迭代器赋值，会隐含地调用push_back()，以添加元素：

```cpp
#include<iterator>

vector<int> vec;
auto it = back_inserter(vec)
*it = 42;// is equal to vec.push_back(42);
```

配合使用back_inserter和fill_n，我们就可以给已经创建好的容器批量添加元素了。  

```cpp
#include<iterator>
#include<algorithm>

vector<int> vec;
fill_n(back_inserter(vec), 10, 0) // 加入10个0给vec。
```

### 拷贝copy

```cpp
#include<algorithm>
auto ret = copy(a1.begin(), a1.end(), a2.begin());
// 需要用户确保a2有足够的空间
// 返回的ret指向a2尾元素之后的位置。
```

### replace与copy

许多算法有copy版本，即不修改原先的容器，而是将结果放入第三个容器中。  

```cpp
// 一般replace:
replace(a.begin(), a.end(), 0, 42);// 0替换为42;

// copy版本
replace_copy(a1.cbegin(), a1.cend(), back_inserter(new_vec), 0, 42);
// 结果将会放到new_vec中
```

### sort与unique

```cpp
// 以下是一个任务：删除string数组的重复元素

// 排序，寻找重复单词
sort(words.begin(), words.end());

// unique得配合sort使用才行.将不重复的元素放到容器的前面，返回第一个重复元素的位置的迭代器。
auto end_unique = unique(words.begin(), words.end());

// 删除
words.erase(end_unique, words.end());
```

> unique的作用是去除容器或者数组中相邻元素的重复出现的元素，只保留其中一个。其函数原型为：iterator unique (iterator it_1,iterator it_2)。其中，it_1和it_2表示容器的起始和结束迭代器，函数会返回去重之后的尾地址。需要注意的是，这里的去除并非真正意义的erase，而是将重复的元素放到容器的末尾。对于顺序顺序错乱的数组成员或者容器成员，需要先进行排序，可以调用std::sort()函数。

### 定制行为：向算法传递函数

标准库中的算法的行为常常是确定的，但用户也可以进行一些定制操作。

我们自定义一个函数，让标准库算法使用我们定义的函数工作：

```cpp
#include<algorithm>
#include<string>

bool isShorter(const string &s1, const string &s2){
    return s1.size()<s2.size();
}

// 将函数传递给泛型算法以定制操作
// sort在底层执行的是一个二元运算符，因此第三个函数被要求定义为二元的。
// 这个函数将words按照元素长度，从小到大排列.
// 即对二元的 s1和s2，如果s1 ? s2==True，则s1排在s2之前.
sort(words.begin(), words.end(), isShorter);
```

容易理解，标准库提供的泛型算法作用在一个地址区间上的每个元素或每组元素上，本质上是元素操作。因此，一定存在运算符。  
理解算法使用的是哪种运算符，是几元的，我们就能定制算法行为。  

### lambda表达式

语法：

```cpp
[capture list](parameter list) -> return type {function body}
// capture list指lambda函数体内会使用的“局部标识符”。
// 不在捕获列表内，lambda函数无法使用.
// 全局变量不是。lambda函数内可以使用任何全局声明的，包括函数与类定义，或者static变量。
```

在实现时，可以忽略参数列表和返回值类型，但永远必须包含捕获列表和函数体：

```cpp

auto f = []{return 42;};
// 建议记忆：
auto f = [](){return 42;};
// lambda函数不允许默认参数。
// labmda函数要求在定义体最后的;
```

lambda函数的调用与一般函数一致。由于短小，方便调用，常用在传递给函数，以定制行为上。

之前的例子可以用lambda函数实现为：

```cpp
#include<iostream>
#include<vector>
#include<string>
#include<algorithm>

auto shorter = [](const string &s1, const string &s2)->bool{return s1.size()<s2.size();};

vector<string> vec{"123dd", "4567","qw","e"};
sort(vec.begin(), vec.end(), shorter);
// or
// sort(vec.begin(), vec.end(), [](const string &s1, const string &s2){return s1.size()<s2.size();});
// ...，这种代码在大型工程中会不会有点不负责任？
```

lambda做的实际工作比看上去更多。编译器实际上先定义了一个lambda对应的，未命名的class类型。我们调用声明的lambda函数时(包括auto的赋值调用和字面量传入函数调用)，实际上在构造这个未命名的class的对象。  

### find_if

find_if是对find的定制行为支持。  
find只能使用==完成查找操作，find_if则在第三项接受一个返回bool的函数，单目运算符，作用在每个遍历到的元素上，直到第三个参数的函数返回True为止。  

配合lambda表达式，实现一个找到列表中第一个达到指定长度的字符串。

```cpp
vector<string> vs{"123", "abc","45z6","def"};
int min_size = 4;

// 这里也演示了lambda表达式关于局部变量捕获的使用方法
auto ptr = find_if(vs.begin(), vs.end(), [min_size](const string &s){return s.size()>=min_size;});
```

容易理解，如果先根据元素长度对列表排序，再find_if取得第一个达到期望长度的元素的迭代器，根据vs.end()-ptr，我们就能知道列表中有多少个元素达到了指定长度。  

> 当然，这样做在时间上是亏很多的。

### for_each算法

for_each算法接受一个可调用对象（lambda/函数），对范围内的所有元素调用该对象。（所以，可调用对象必须是单目的）

下段代码打印vector\<string\>中所有字符串的反转，但不修改字符串。  
用了两种方法，for(:)和for_each。  
由于范围for不加&时会创建元素的拷贝，因此无需额外考虑，调用reverse就能反转一个备份，然后打印。  
for_each更像是一般的循环，自行申请了新的空间，并用reverse_copy完成了工作。  

```cpp
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
  vector<string> vs{"123", "456", "789"};
  string s("123");
  // s.substr()
  auto show_reverse = [](const vector<string> &vs) {
    // 这里用了auto 而不是auto &，以保证遍历到的元素没有被修改.
    for (auto s : vs) {
      // reverse 并不会修改vs中的元素
      reverse(s.begin(), s.end());
      cout << s << endl;
    }
    return 0;
  };
  show_reverse(vs);

  for_each(vs.begin(), vs.end(), [](const string &s) {
    // 这里必须申请4个char空间，额外的一个留给编译器添加的\0
    char tmp[4];
    reverse_copy(s.begin(), s.end(), tmp);
    cout << tmp << endl;
  });
}

```

> 颇有一种，茴字的四种写法的味道...

但for_each还是比较有用的，如果你要对列表中的每个元素都执行特定的单一操作的话。  

> 我们来复习一下python的lambda表达式，下例生成1-100的奇数和偶数，并将两者相加:
```py
odd = list(range(1, 100, 2))
even = list(map(lambda x:x+1, odd))
rst = list(map(lambda x,y:x+y, odd, even))
```

### lambda的值捕获与引用捕获

在lambda表达式的捕获列表中，除了值传递，也可以通过&完成引用传递。  
对于值传递，lambda会在自己被定义时就完成拷贝，因此，后续对该值的更改不会影响到lambda。  
值传递是const的，你无法修改，也不应该修改它的值。  

> 当然，它可以被解const，以下是一个实例，同时也说明了lambda的值传递在定义时完成，而不是调用时。  
> 也暗示了，lambda在创建一个自定义类型，而不是简单的函数调用的实质：它需要一块内存，保存值捕获的结果。  
```cpp
int tmp = 101;
auto f = [tmp]{
    int &p = const_cast<int&>(tmp);
    ++p;
    cout<<tmp<<endl;
    };
f();
f();
cout<<tmp;
// 结果是：
// 102 
// 103
// 101
// 由于我们恶意地用const_cast解除了值捕获的read-only，因此，多次对lambda调用打印的捕获值有所不同。这暗示了lambda定义了一个类型，并将捕获到的值作为其const数据成员，在调用时产生对象。
```

引用捕获：

```cpp
int size = 42;
auto f2 = [&size]{return size;};
```
引用捕获的行为与一般引用一致。  
在返回引用的对象上，lambda的规则与一般函数一致，不要返回局部对象的引用。离开作用域范围，会被回收。  
引用捕获不进行值传递，如果引用的对象在lambda调用时已经被回收，那么调用就是危险的。  
所以说，以引用方式捕获一个变量时，需要确保lambda执行时值依然存在。  

### lambda的隐式捕获

> 如果说有什么是最讨厌的，就是这一大堆令人费解，毫无可读性，让人摸不着头脑的省略写法。  

隐式捕获指让编译器根据lambda中函数体的代码，推断需要捕获哪些变量。  
在推断列表中写一个=或&，分别代表值捕获和引用捕获。  

```cpp
wc = find_if(words.begin(), words.end(), [=](const string &s){return s.size()>=sz;})
// 由于写了=，sz会被推导，隐式捕获。
```

> 不过你问我会不会写？我肯定会写！挺方便的呀。

可以混合使用隐式捕获和显式捕获，不过，若隐式捕获&，则显式的只能是=，相反亦然。  

### 可变lambda:使得值捕获可变

像之前说的，lambda的值捕获都会是const的，我们可以声明mutable，来使得它可变。  
注意区分两种情况，mutable声明与引用捕获是截然不同的。mutable声明的值引用依然是值传递，使得捕获的参数可以改变，但是不会改变该参数的源对象，就像我们上面强制解const时的情况一样。  

```cpp
int tmp = 42;
auto f = [=]()mutable{return ++tmp;};// 这种情况下不能省略参数的()，即使没有。
// 这有点让人在意，mutable不应该是作用在[]上的吗？
cout<<f()<<" "<<f();

// result:
// 43 44
```

### lambda：无法推断返回值类型的情况

有时候，lambda无法推断返回值的类型，此时需要显式指出：

例如：
```cpp
auto f = [](int i){if(i<0)return -i;else return i;};
```
需要修改为：

```cpp
auto f = [](int i)->int {if(i<0)return -i;else return i;};
```
> 这是primer说的，我在g++上，第一种情况也通过了。

### 使用bind生成新的可调用对象

> 与python的functools.partial装饰器行为相似。  

语法是auto new_callable = bind(callable, arg_list)。arg_list中使用占位符，绑定部分参数。  

```cpp
#include <iostream>
#include <functional>

using namespace std;
using namespace std::placeholders;

int add(int a, int b, int c) {
    return a + b + c;
}

int main() {
    auto newAdd = bind(add, _1, _2, 0); // 将第三个参数绑定为0
    cout << newAdd(1, 2) << endl; // 输出3
    return 0;
}
```
TODO:
- 10.4 再探迭代器
- 10.5 泛型算法结构
- 10.6 特定容器算法

三节，感觉意义有限，暂时跳过。

## 第十一章 关联容器
