#include <time.h>

#include <fstream>
#include <iostream>
#include <string>
#include <vector>

#include "sm4.h"
using namespace sm4;
using namespace std;

std::vector<int> split(std::string str, std::string pattern) {
  std::string::size_type pos;
  std::vector<int> result;

  str += pattern;  //扩展字符串以方便操作
  int size = str.size();

  for (int i = 0; i < size; i++) {
    pos = str.find(pattern, i);
    if ((int)pos < size) {
      std::string s = str.substr(i, pos - i);
      result.push_back(stoi(s));
      i = pos + pattern.size() - 1;
    }
  }
  return result;
}

int main(int argc, char* argv[]) {
  string key, msg;
  if (argc != 5) {
    cout << "should have 5 arg." << endl;
    return -1;
  }
  if (strcmp(argv[1], "-k") == 0) {
    key = argv[2];
    if (key.size() != 16) {
      cout << "key length should be 16" << endl;
      return -1;
    }
    if (strcmp(argv[3], "-e") == 0) {
      msg = argv[4];
      unsigned char en_rst[msg.size()];
      encrypt(key, msg, en_rst);
      cout << "encrypt result:" << endl;
      for (int i = 0; i < (int)msg.size(); i++) {
        cout << (int)en_rst[i];
        if (i != (int)(msg.size() - 1)) cout << "-";
      }
      cout << endl;
    } else if (strcmp(argv[3], "-d") == 0) {
      msg = argv[4];
      vector<int> nums = split(msg, "-");
      if (nums.size() > 0) {
        unsigned char to_decrypt[nums.size()];
        for (int m = 0; m < (int)nums.size(); m++) {
          to_decrypt[m] = (unsigned char)(nums[m]);
          cout << (int)to_decrypt[m] << "-";
        }
        cout << "decrypt result:" << endl;
        cout << decrypt(key, to_decrypt, nums.size()) << endl;

      } else {
        cout << "input ciphertext error, please check." << endl;
      }

    } else {
      cout << "argv[3] should be -e or -d" << endl;
    }
  } else {
    cout << "need -k and should be first" << endl;
  }
}