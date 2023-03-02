#include<algorithm>
#include<vector>
#include<string>
#include<iostream>

using namespace std;

int main(){
    string s1="1234567abcdefg";
    vector<string> vs{"123", "abc","456","def"};
    auto ptr = find(vs.begin(), vs.end(), "abc");
    // auto ptr = s1.find("abc");
    // 最好不要直接这么做，find找不到会指向end()，对end()解引用是危险的.
    cout<<*ptr<<endl;
}