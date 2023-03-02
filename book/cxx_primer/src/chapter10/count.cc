#include<algorithm>
#include<iostream>
#include<vector>
using namespace std;

int main(){
    vector<int> vec{1,2,3,4,5,5,6,6,5,5,5};
    int rst = count(vec.begin(), vec.end(), 5);
    cout<<rst<<endl;
}