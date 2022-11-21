#include<iostream>
#include<string>
using namespace std;

class Node{
    public:
        Node(int number, string name):number(number),name(name){}
        void set_name(std::string new_name)const{
            this->name=new_name;
        }
        inline void show_info(){
            cout<<"number:"<<this->number<<" name:"<<this->name<<endl;
        }
    private:
        int number;
        mutable string name;
};

int main(){
    Node node = Node(114514, "ATRI");
    node.show_info();
    node.set_name("nanami");
    node.show_info();
}