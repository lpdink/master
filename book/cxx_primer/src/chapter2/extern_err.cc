// 函数也是默认extern的，不使用命名空间，就可能导致污染！
int test(int a, int b){
    return a+b;
}
// #include<iostream>
// using namespace std;

// extern int test(int, int);

// int main(){
//     int a=5, b=4;
//     cout<<test(a, b)<<endl;
// }