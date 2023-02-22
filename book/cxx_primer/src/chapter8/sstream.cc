#include<iostream>
#include<sstream>
#include<string>

using namespace std;

int main(){
    stringstream ss("BigBoss 22 2022");
    string name, year;
    int age;
    ss>>name>>age>>year;
    cout<<name<<" "<<age<<" "<<year;
}