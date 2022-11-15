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
```
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
在全局数据区分配内存，要求在声明处化，只被初始化一次，值会保存到下一次函数调用。(因为内存空间在全局数据区，而不是栈上，栈上数据会被回收。)
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
```
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
底层const则指，指针指向的对象是常量。  
```
int val=42;
int* const ptr=&val; //ptr将一直指向&val地址，但是不会管里面的值是否变化。

const int* const another_ptr=&val; //another_ptr将一直指向&val地址，并且保证不能通过another_ptr修改&val存储的值。
```
### constexpr常量表达式
C++11特性。  
这是一种在**编译时**由编译器计算结果的表达式，而不是在运行时计算。  
得到计算结果后，该对象与const在运行时的行为一致。  
你可以将一切你认为应该是constexpr的表达式声明成constexpr的，如果不是，编译器会告诉你的。
```
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
```
const int *p = nullptr; // 这是指向常量的指针
constexpr int *q = nullptr;// 这是常指针！
```
你可以混用constexpr与const创建一个指向常量的常指针，但是，你可以用两个const完成这一工作，所以别把constexpr与指针放在一起。
```
constexpr int *p=nullptr
// is eq to 
int *const p=nullptr;
//-------
int val=42;
constexpr const int *p=&val;
// is eq to 
const int *const p=&val;
```
> 但话说回来，constexpr const int* ptr这种写法真的好漂亮哦，比const int *const ptr好看多了...
### typedef
除了typedef，11标准支持了一种新写法：
```
typedef double MyDouble;
using MyInt=int; // 11标准
```
### auto
auto也是c++11新支持的。  
- 与const
```
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
```
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
```
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
```
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
```
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
```
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
**建议**并不是所有的标准库容器都定义了迭代器的<！因此，总是使用!=来判断迭代器是否走到了末尾。  
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

在栈内，默认初始化会让数组拥有随机值。  
在堆上，被初始化为0。  
- 字符数组

字符数组有一个\0的结尾约定，故存在，你需要\0，你不需要\0两种情况：
```
char a1[]={'c','+','+'}; // 不会添加\0
char a1[]={'c','+','+','\0'}; // 你自己添加了\0
char a3[] = "C++"; // 编译器为你自动添加\0
const char a4[3]="C++"; // 报错，没有空间添加\0
```
- 不允许拷贝和赋值

```
int a[]={1,2,3};
int a2[]=a;// 错误，没有拷贝构造函数
a2 = a; //错误，不允许赋值
```
- 数组支持范围for访问！

因为数组的维度是固定的，算作数组属性的一部分，编译器是知道数组大小的。  
因此这是可以(且推荐)的
```
int array[10];
for(auto& element:array){
    ...;
}
```
- 使用begin与end访问数组的首(尾+1)元素

C++11特性。  
```
int array[]={1,2,3,45};
int *beg = begin(ia); // 指向1
int *last = end(ia); // 指向45的下一位置。不能对last解引用！
```
- 下标和指针

这里同样演示一种等价：  
```
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
```
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
```
string s("12345");
const char *c_s=s; // 错误
const char *c_s=s.c_str(); // 正确
// 对s的修改会反映到c_s上。
```
### TODO：使用数组初始化vector对象。