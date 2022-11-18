#include <iostream>
using namespace std;

int get_bigger(int a, int b) { return a > b ? a : b; }

// 函数指针作为形参
// 如果有已有函数
// using Func = decltype(get_bigger);
// 或
// typedef decltype(get_bigger) Func;
// 如果没有一个已知函数
using Func = int(int, int);
void exec(Func* func) { cout << func(3, 42) << endl; }

// 作为返回值
Func* ret_func_ptr() {
  // 创建一个指向函数的指针
  Func* ptr = get_bigger;
  return ptr;
}

int main() {
  // 作为形参
  exec(get_bigger);
  // 或
  exec(&get_bigger);
}