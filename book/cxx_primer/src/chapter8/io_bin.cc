#include<iostream>
#include<fstream>
using namespace std;

struct Student
{
    char name[30];
    int age;
    int number;
};


// int main(){
//     ofstream out("out_bin.bin", ofstream::binary);
//     Student ns={"大BOSS", 18, 1001};
//     out.write(reinterpret_cast<char*>(&ns), sizeof(ns));
//     out.close();
// }

int main(){
    // 读
    ifstream in("out_bin.bin", ifstream::binary);
    Student ns;
    in.read(reinterpret_cast<char*>(&ns), sizeof(ns));
    cout<<ns.name<<" "<<ns.age<<" "<<ns.number<<endl;
    // 这会core，可能是因为没有给string分配内存空间，但尝试向其中写了。
}