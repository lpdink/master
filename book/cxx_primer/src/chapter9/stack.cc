#include<stack>
#include<deque>
#include<vector>
using namespace std;

int main(){
    deque<int> deq{12,3};
    vector<int> vec{4,5,6};
    stack<int> sk(deq); // 适配器可以用基本容器类型初始化
    sk.push(123);
    int top=sk.top();//返回栈顶元素
    sk.pop(); //pop没有返回值
}