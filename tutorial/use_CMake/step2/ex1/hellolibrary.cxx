#include<string>
#include<iostream>

#include "add.h"

int main(int argc, char *argv[]){
    int a = std::stoi(argv[1]);
    int b = std::stoi(argv[2]);
    int c = myadd(a, b);
    std::cout<<"a "<<a<<" +b "<<b<<" = "<<c<<std::endl;

}