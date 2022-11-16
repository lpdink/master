#include<iostream>
#include<string>
#include<vector>
using namespace std;

int main(){
    string s("0123456789-abcdefgh");
    const char *s_c=s.c_str();
    char* writable_sc = const_cast<char*>(s_c);
    // 重解释为unsigned char
    unsigned char *uc_writable_sc=reinterpret_cast<unsigned char*>(writable_sc);
    int idx=0;
    // \0==0
    uc_writable_sc[1]=242;
    uc_writable_sc[2]=-42;
    while((uc_writable_sc[idx])!='\0'){
        cout<<writable_sc[idx]<<" "<<static_cast<int>(writable_sc[idx])<<" ";
        cout<<uc_writable_sc[idx]<<" "<<static_cast<int>(uc_writable_sc[idx++])<<endl;
        // ++idx;
    }
    cout<<uc_writable_sc<<" "<<writable_sc<<" "<<s_c<<" "<<s<<endl;
}