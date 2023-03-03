#include<iostream>
#include<string>
using namespace std;

// static int standard = 3;

bool shorter(const string &s1, const string &s2){
    return s1.size()<s2.size();
}

int main(){
    int standard = 3;
    auto f = [](const string &s1, const string &s2){
        cout<<"s1.size<standard? "<<(s1.size()<standard)<<endl;
        cout<<"s2.size<standard? "<<(s2.size()<standard)<<endl;
        return "done!";
    };
    string s1("123456"), s2("1");
    cout<<f(s2, s1)<<endl;
    cout<<f(s1, s2)<<endl;
}