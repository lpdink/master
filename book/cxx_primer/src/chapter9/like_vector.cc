#include<vector>
#include<iostream>
using namespace std;

int main(){
    vector<int> vc{1,2,3};
    vc.emplace_back(12);
    for(auto& e:vc)cout<<e<<" "<<endl;

    // front能作为左值使用吗?
    // 可以.
    vc.front()=42;
    for(auto& e:vc)cout<<e<<" "<<endl;
}