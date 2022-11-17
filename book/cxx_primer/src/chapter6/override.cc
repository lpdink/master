#include<iostream>
using namespace std;

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