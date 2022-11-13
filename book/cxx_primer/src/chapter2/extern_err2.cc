// 函数也是默认extern的，不使用命名空间，就可能导致污染！
int test(int a, int b){
    return a*b;
}