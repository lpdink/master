// 尝试在extern C声明中使用C++特性
#include<vector>
#include<iostream>
using namespace std;
extern "C" void show_vector(const vector<int> &res_vector){
    for(auto item:res_vector){
        cout<<item<<endl;
    }
}


int main(){
    vector<int> my_vector={1,2,3,4,5};
    show_vector(my_vector);
}