#include<queue>
#include<vector>
#include<iostream>
using namespace std;

int main(){
    vector<int> vec{4,3,6,7,8};
    priority_queue<int, vector<int>,greater<int>> pq(vec.begin(), vec.end());
    // priority_queue<int> pq(vec.begin(), vec.end());
    pq.push(1024);
    pq.push(42);
    pq.push(2048);
    while(!pq.empty()){
        cout<<pq.top()<<endl;
        pq.pop();
    }
}