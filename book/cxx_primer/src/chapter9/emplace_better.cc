#include<iostream>
#include<vector>
using namespace std;

class Node{
    public:
        Node(int n):num(n){
            cout<<"构造函数"<<endl;
        }
        Node(const Node &other):num(other.num){
            cout<<"拷贝构造函数"<<endl;
        }
        Node(Node&& old):num(old.num){
            cout<<"移动构造函数"<<endl;
        }
        int num;
};

int main(){
    vector<Node> vns;
    cout<<"效率相等的情况：先创建对象，再放入容器"<<endl;
    cout<<"push_back:"<<endl;
    vns.push_back(Node(12));
    cout<<"------\n"<<"emplace_back:"<<endl;
    vns.emplace_back(Node(42));

    cout<<"---------\nemplace_back效率高的情况：\n";
    cout<<"push_back:"<<endl;
    vns.push_back(12);
    cout<<"emplace_back:"<<endl;
    vns.emplace_back(42);
    cout<<"------"<<endl;
    vns.emplace_back(move(Node(42)));
}