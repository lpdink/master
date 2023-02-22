#include<string>
#include<iostream>
using namespace std;

int main(){
    string s1="123456";
    s1.push_back('A');
    s1.append("abcdefg");
    s1.replace(0, 3, "789");
    cout<<s1<<endl;
    cout<<"------"<<endl;

    string::size_type pos=0;
    string s2="ab12cd34ef56ppos";
    while((pos=s2.find_first_of("0123456789", pos))!=string::npos){
        cout<<pos<<" "<<s2[pos]<<endl;
        ++pos;
    }
}