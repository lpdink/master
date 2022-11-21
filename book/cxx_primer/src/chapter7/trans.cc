#include<iostream>
#include<string>
using namespace std;

class Node{
    public:
        Node(string name):name(name){}
        string name;
};

void show_name(const Node &node){
    cout<<node.name<<endl;
}

int main(){
    string s{"我下午要玩戴森球计划"};
    show_name(s);
}