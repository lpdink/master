#include <iostream>
using namespace std;

// class Counter {
//  public:
//   Counter() {}
//   void add(){ this->nums += 1; }
//   int nums = 0;
// };
class Counter {
 public:
  Counter() {}
  void add() { this->nums += 1; }
  int get_nums() const { return this->nums; }

 private:
  int nums = 0;
};
int main() {
  // Counter* counter = new Counter();
  Counter counter = Counter();
  for (int i = 0; i < 10; i++) {
    counter.add();
  }
  cout << counter.get_nums() << endl;
}