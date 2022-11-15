#include<iostream>
using namespace std;

int main(){
    // const int num=42;
    // const int *ptr=&num;
    // // int *new_ptr = const_cast<int*>(ptr);
    // int *new_ptr = const_cast<int*>(&num);
    // *new_ptr=88;
    // cout<<num<<" "<<*ptr<<" "<<*new_ptr<<endl;
    const int num[]={1,2,3};
    const int *ptr=num;
    int *new_ptr = const_cast<int*>(ptr);
    *new_ptr=88;
    for(auto& n:num){
        cout<<n<<" ";
    }
    cout<<endl;
}