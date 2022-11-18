#include<iostream>
using namespace std;

int ret_bigger(int a, int b){
    return a>b?a:b;
}
void exec(decltype(ret_bigger) *func){
    cout<<func(5, 6)<<endl;
}
// 或者写作：
// typedef decltype(ret_bigger) Func;
// void exec(Func func){
//     func(5, 10);
// }

int main(){
    exec(ret_bigger);
}