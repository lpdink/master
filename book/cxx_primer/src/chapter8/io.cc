#include<iostream>
#include<fstream>
#include<string>
using namespace std;

int main(){
    fstream in("input.txt");
    ofstream out("output.txt", ofstream::app);
    string s;
    while(getline(in, s)){
        out<<s<<endl;
    }
    out.clear();
    out<<"我将出现在第一行"<<endl;
    in.close();
    out.close();
}