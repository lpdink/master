#include <iostream>
using namespace std;

void bad_way()
{
    double d1 = 3.14;
    int t1 = d1;
    float f1 = t1;
    cout << d1 << " " << t1 << " " << f1 << endl;
}

void better_way()
{
    double d1 = 3.14;
    int t1 = (int)d1;
    float f1 = (float)t1;
    cout << d1 << " " << t1 << " " << f1 << endl;
}

int main()
{
    bad_way();
    cout << "---------------" << endl;
    better_way();

    unsigned char char_max = -1;
    cout << (int)char_max << endl;
}