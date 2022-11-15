#include<string>
#include<iostream>
using namespace std;

int main(){
    string s("123456 abcde");
    // 这里不是拷贝，而是真实的地址返回.
    const char *s_ptr = s.c_str();
    s[1]='A';
    cout<<s<<endl;
    cout<<s_ptr<<endl;
}