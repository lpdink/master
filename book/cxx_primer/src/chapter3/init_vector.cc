#include<iostream>
#include<vector>
using namespace std;

int main(){
    const int nums[]={1,2,3,4,5};
    // nums[1]=88;
    vector<int> vec(nums, nums+5);
    for(auto &item:vec){
        cout<<item<<endl;
    }
}