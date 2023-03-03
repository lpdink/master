#include<iostream>
#include<vector>
#include<string>
#include<algorithm>
using namespace std;


int main(){
    auto shorter = [](const string &s1, const string &s2)->bool{return s1.size()<s2.size();};

    vector<string> vec{"123dd", "4567","qw","e"};
    sort(vec.begin(), vec.end(), shorter);
    for(auto& e: vec){
        cout<<e<<" ";
    }
}