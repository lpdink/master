#include<iostream>

template <typename T>
void multiply(T *a, T *b, int n, T *rst)
{
    for (int i = 0; i < n; i++)
    {
        rst[i] = a[i] * b[i];
    }
    std::cout << "multiply done." << std::endl;
}

void show_vector(int* vec, int n);