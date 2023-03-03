#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
  vector<string> vs{"123", "456", "789"};
  string s("123");
  // s.substr()
  auto show_reverse = [](const vector<string> &vs) {
    // 这里用了auto 而不是auto &，以保证遍历到的元素没有被修改.
    for (auto s : vs) {
      // reverse 并不会修改vs中的元素
      reverse(s.begin(), s.end());
      cout << s << endl;
    }
    return 0;
  };
  show_reverse(vs);

  for_each(vs.begin(), vs.end(), [](const string &s) {
    // 这里必须申请4个char空间，额外的一个留给编译器添加的\0
    char tmp[4];
    reverse_copy(s.begin(), s.end(), tmp);
    cout << tmp << endl;
  });
}