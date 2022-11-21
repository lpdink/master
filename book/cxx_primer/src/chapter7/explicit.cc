#include<iostream>
#include<string>
using namespace std;

class Node{
    public:
        explicit Node(string name):name(name){}
        string name;
};

void show_name(const Node &node){
    cout<<node.name<<endl;
}

int main(){
    string s{"我下午要玩戴森球计划"};
    // show_name(s);
    Node node = Node(s);
    show_name(node);
    show_name(Node(s));
    // 但是允许显式的强制类型转换
    show_name(static_cast<Node>(s));
}