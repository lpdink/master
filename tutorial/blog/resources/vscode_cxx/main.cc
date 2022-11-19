#include "function.h"

int main(){
    int a[10]={1,2,3,4,5,6,7,8,9,10};
    int b[10]={10,10,10,10,10,10,10,10,10,10};
    int c[10];
    multiply(a, b, 10, c);
    multiply(c, b, 10, c);
    multiply(c, b, 10, c);
    show_vector(c, 10);
}