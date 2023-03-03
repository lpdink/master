#include<algorithm>
#include<vector>
#include<iostream>
using namespace std;

int main(){
    vector<int> vec{1,2,3,43,5,6,6, 6, 7, 8, 9, 1, 2, 3, 5, 5, 3, 4, 3, 2, 3, 5};
    auto end_unique = unique(vec.begin(), vec.end());
    for(auto &e:vec){
        cout<<e<<" ";
    }
    cout<<endl;
    cout<<*end_unique<<" "<<*(end_unique-1);

}