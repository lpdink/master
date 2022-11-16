// 不能返回任何在栈上申请的对象或其引用或其指针！
#include <iostream>
#include <string>
#include <vector>
using namespace std;

class Node
{
public:
    Node()
    {
        cout << "new" << endl;
    }
    ~Node()
    {
        cout << "delete" << endl;
    }
};

Node ret_node()
{
    Node node = Node();
    cout <<"node inside addr:"<<&node<<endl;
    return node;
}

int main()
{
    Node node = ret_node();
    cout << "outside node addr:" << &node << endl;
}