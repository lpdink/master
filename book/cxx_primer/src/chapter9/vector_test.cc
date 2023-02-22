// 用vector测试几乎所有容器的泛用操作
#include<iostream>
#include<vector>
using namespace std;

class Node{
    public:
        int inside[3];
        vector<int> vec;
        int age;
};

int main(){
    // 泛用操作

    // 构造函数
    vector<int> v1;
    vector<int> v2{1,2,3};
    vector<int> v3(v2);
    vector<int> v4=v2;
    vector<int> v5={1,2,3};

    // 相等性:发现v2~v5都相等.
    cout<<(v1==v2)<<endl<<(v2==v3)<<endl<<(v2==v4)<<endl<<(v2==v5)<<endl;
    cout<<"-----"<<endl;

    // 地址: v2与v2[0]的地址不相等.v2[0]与v3[0]的地址不相等，说明是深拷贝。
    cout<<&v1<<endl<<&v2<<endl<<&(v2[0])<<endl<<&v3<<endl<<&(v3[0])<<endl<<&v4<<endl<<&v5<<endl;
    cout<<"-----"<<endl;

    // 再探深拷贝
    // 01. 二维vector的赋值是深拷贝吗？
    // 是深拷贝！
    vector<int> tmp_v{1,2,3};
    vector<vector<int>> vv1;
    vv1.push_back(tmp_v);
    vector<vector<int>> vv2(vv1);
    vv1[0][0]=42;
    vv2[0][0]=88;
    cout<<tmp_v[0]<<endl<<vv1[0][0]<<endl<<vv2[0][0]<<endl;

    // 02. 自定义类型可以被深拷贝吗？
    // 可以.
    Node node=Node();
    node.age=42;
    node.inside[0]=99;node.inside[1]=98;node.inside[2]=97;
    node.vec={1,2,3};
    vector<Node> vn1;
    vn1.push_back(node);
    vector<Node> vn2=vn1;
    vn2[0].age=1001;
    vn2[0].inside[0]=8888;
    vn2[0].vec[0]=98765;
    cout<<"vn1:"<<vn1[0].age<<" "<<vn1[0].inside[0]<<" "<<vn1[0].vec[0]<<endl;
    cout<<"vn2:"<<vn2[0].age<<" "<<vn2[0].inside[0]<<" "<<vn2[0].vec[0]<<endl;
    // cout<<"vn1==vn2?"<<(vn1==vn2);
    cout<<"-----"<<endl;
    // swap
    vector<int> tmp_v1{1,2,3}, tmp_v2{4,5,6};
    // swap(tmp_v1, tmp_v2);
    tmp_v1.swap(tmp_v2);
    for(auto& e:tmp_v1){
        cout<<e<<endl;
    }
    for(auto& e:tmp_v2){
        cout<<e<<endl;
    }
    cout<<"------"<<endl;

    // 增删元素
    tmp_v1={4,5,6,4};
    tmp_v1.insert(tmp_v1.begin(),77);
    // cout<<&tmp_v1.begin()<<" "<<&tmp_v1<<" "<<&(tmp_v1[0])<<endl;
    tmp_v1.erase(tmp_v1.begin());
    for(auto e:tmp_v1)cout<<e<<endl;
}