#include<iostream>
#include<vector>
using namespace std;

void test(){
    int val=42;
    // 虽然val被显示声明了，但是它并非const的，地址不确定，因此不能为constexpr提供支持。
    const int val2=val+val;
    cout<<val2<<endl;
}

int main(){
    // vector<int> res_vec;
    // // 如果你尝试这样做，编译器会报错。
    // constexpr int length = res_vec.size();
    // cout<<length<<endl;
    test();
    constexpr int num=423;
    cout<<num<<endl;
    return 0;

}