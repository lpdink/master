// 内置类型
// 只有整型和浮点类型两种
// C强大在其内存操作上，故应该始终从字节级别(本质)理解数据类型。
#include <iostream>
using namespace std;

int main()
{
    // 整型
    // 整型可以前置signed/unsigned，除了char外，全部都是默认signed的。
    // char究竟是signed的，还是unsigned的，由编译器决定。
    // 因此，对于数字，建议不要声明char类型，而应该明确指出是signed的还是unsigned的。
    cout << "bool " << sizeof(bool) << endl;
    cout << "char " << sizeof(char) << endl;
    cout << "wchar_t " << sizeof(wchar_t) << endl;
    cout << "char16_t " << sizeof(char16_t) << endl;
    cout << "char32_t " << sizeof(char32_t) << endl;
    cout << "short " << sizeof(short) << endl;
    cout << "int " << sizeof(int) << endl;
    cout << "long " << sizeof(long) << endl; // 避免使用Long.有可能长度等于int。
    cout << "long long " << sizeof(long long) << endl;
    // 浮点类型
    cout << "float " << sizeof(float) << endl;
    cout << "double " << sizeof(double) << endl;
    cout << "long double " << sizeof(long double) << endl;
    // Ubuntu下：
    // bool 1
    // char 1
    // wchar_t 4
    // char16_t 2
    // char32_t 4
    // short 2
    // int 4
    // long 8
    // long long 8

    // float 4
    // double 8
    // long double 16
    

    // 使用int *p而不是int* p
    // 因为 int* p, np，其中p是int*，而np是int

    // extern允许cc文件获取另一个cc文件的变量，无需通过.h，只需要将两个cc一起编译，在定义处和声明处都extern。
    // 一个extern表示这个变量提供给外面，另一个表示这个变量由外部提供。

    // &除了取地址，还是引用：
    int n=1;
    int &nn=n;
    // nn是对n的别名。
    decltype(nn) nnn=n;

    // const引用
    // const引用的对象可以不是const的，这就是我们常常传递的：
    // void test(const Student &student)
    // 的秘密。


}