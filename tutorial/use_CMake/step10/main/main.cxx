#include<iostream>
#include "own_math.h"

int main(int argc, char* argv[]){
    // int a = argv[1];
    // int b = argv[2];
    // float c = argv[3];
    // float d = argv[4];
    int a=2;int b=98;
    float c=1.414;float d=2.828;
    std::cout<<"a+b="<<add(a, b)<<"a*b="<<mul(a,b)<<std::endl;
    std::cout<<"c+d="<<add(c, d)<<"c*d="<<mul(c,d)<<std::endl;
    return 0;
}