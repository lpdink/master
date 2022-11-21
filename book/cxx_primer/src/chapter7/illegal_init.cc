#include<iostream>
#include<string>
using namespace std;

class Node{
    public:
        // string name("Node");
        string name{"name"};
};

int main(){
    Node node = Node();
    cout<<node.name<<endl;
}