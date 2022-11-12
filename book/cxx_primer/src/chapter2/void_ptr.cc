#include<iostream>
using namespace std;

int main(){
	int tmp=114514;
	void *ptr=&tmp;
	int *int_ptr;
	int_ptr=(int* )ptr;
	cout<<*int_ptr<<endl;
}
