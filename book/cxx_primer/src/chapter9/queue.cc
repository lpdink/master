#include<queue>
#include<deque>
#include<iostream>
using namespace std;

int main(){
    deque<int> deq{1,2,3};
    queue<int> que(deq);
    
    while(!que.empty()){
        cout<<que.front()<<endl;
        que.pop();
    }
}