#include<string>
#include<iostream>

#include "config.h"
#ifdef USE_LIBRARY
#include "add.h"
#else
int myadd(int a, int b){
    return int((a+b)*100);
}
#endif

int main(int argc, char *argv[]){
    int a = std::stoi(argv[1]);
    int b = std::stoi(argv[2]);
    int c = myadd(a, b);
    std::cout<<"a "<<a<<" +b "<<b<<" = "<<c<<std::endl;

}