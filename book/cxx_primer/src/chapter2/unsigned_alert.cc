#include <iostream>
#include <vector>
using namespace std;

template <typename T>
void show_except_last_err(const vector<T> &res_v)
{
    // 警惕unsigned尝试变为负数.
    // 很隐晦的是stl容器的size()，这是一个unsigned！

    // 本例是一个错误的示范：
    // vector.size()是unsigned的，如果vector长度为0，<的右式会最大！进入循环后会Segmentation fault!
    for (int i = 0; i < res_v.size() - 1; i++)
    {
        cout << res_v[i] << endl;
    }
}

template <typename T>
void show_except_last_right(const vector<T> &res_v)
{
    // 正确的写法是：
    for (unsigned int i = 0; i + 1 < res_v.size(); i++)
    {
        cout << res_v[i] << endl;
    }
}

int main()
{
    vector<int> test_vector_0;
    vector<int> test_vector_5={1,2,3,4,5};
    // show_except_last_err(test_vector_0);
    show_except_last_err(test_vector_5);
    cout<<"--------"<<endl;
    show_except_last_right(test_vector_0);
    show_except_last_right(test_vector_5);
}