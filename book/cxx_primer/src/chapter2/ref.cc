#include<iostream>

int main(){
    int val=1024;
    int val2=2048;
    int &ref_val=val;
    int &ref_val2=ref_val;
    ref_val=val2;
    std::cout<<val<<" "<<val2<<" "<<ref_val<<" "<<ref_val2<<std::endl;

    return 0;
}