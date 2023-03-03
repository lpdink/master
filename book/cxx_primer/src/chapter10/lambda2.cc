#include<iostream>
using namespace std;

// int main(){
//     int tmp = 101;
//     auto f = [tmp]{
//         int &p = const_cast<int&>(tmp);
//         ++p;
//         cout<<tmp<<endl;
//         };
//     f();
//     f();
//     cout<<tmp;
// }

int main(){
    // mutable lambda.
    // int tmp = 42;
    // auto f = [=]()mutable{return ++tmp;};
    // cout<<f()<<" "<<f();

    auto f = [](int i)->int {if(i<0)return -i;else return i;};
    cout<<f(1)<<endl;
}