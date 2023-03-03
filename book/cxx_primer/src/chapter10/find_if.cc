#include<algorithm>
#include<vector>
#include<string>
#include<iostream>

using namespace std;

int main(){
    string s1="1234567abcdefg";
    vector<string> vs{"123", "abc","45z6","def"};
    int min_size = 4;

    auto ptr = find_if(vs.begin(), vs.end(), [min_size](const string &s){return s.size()>=min_size;});
    if(ptr!=vs.end())
    cout<<*ptr<<endl;
}