#include<iostream>
using namespace std;

int get_value(){
    return 42;
}

int main(){
    int i;
    if((i=get_value())==42){
        cout<<"i is eq to 42"<<endl;
    }
}