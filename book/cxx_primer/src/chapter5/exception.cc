#include <iostream>
#include <stdexcept>
using namespace std;

int main() {
  try {
    try {
      try {
        throw exception();
      } catch (exception err) {
        cout << err.what() << endl;
        throw runtime_error("a runtime error");
      }
    } catch (runtime_error err) {
      cout << err.what() << endl;
      throw logic_error("a logic error");
    }
  } catch (logic_error err) {
    cout << err.what() << endl;
  }
}