#include<iostream>
using namespace std;

int ret_bigger(int a, int b){
    return a>b?a:b;
}
using PF=int(*)(int, int);

PF ret_ptr(){

    return *ret_bigger;
}

int main(){
    cout<<ret_ptr()(2,3)<<endl;
}