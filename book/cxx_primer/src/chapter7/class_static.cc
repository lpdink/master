#include<iostream>
#include<string>
using namespace std;

class Node{
    public:
        Node(int number, string name):number(number),name(name){}
        // it's ok
        inline void show_info(){
            cout<<"number:"<<this->number<<" name:"<<this->name<<endl;
        }
        // illegal:class function don't have this ptr;
        // static inline void show_info(){
        //     cout<<"number:"<<this->number<<" name:"<<this->name<<endl;
        // }
    private:
        int number;
        string name;
};

int main(){
    Node node = Node(114514, "ATRI");
    node.show_info();
}