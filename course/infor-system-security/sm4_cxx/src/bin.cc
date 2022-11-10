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

static unsigned char encrypt_msg[655350];

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
      encrypt(key, msg, encrypt_msg);
      cout << "encrypt result:" << endl;
      int padding_num = msg.size();
      if (padding_num % 16 != 0) padding_num += 16 - padding_num % 16;
      for (int i = 0; i < padding_num; i++) {
        cout << (int)encrypt_msg[i];
        if (i != padding_num - 1) cout << "-";
      }
      cout << endl;
    } else if (strcmp(argv[3], "-d") == 0) {
      msg = argv[4];
      vector<int> nums = split(msg, "-");
      if (nums.size() > 0) {
        if (nums.size() % 16 != 0) {
          cout << "decrypt text should be 16x" << endl;
          return -1;
        }
        for (int m = 0; m < (int)nums.size(); m++) {
          encrypt_msg[m] = (unsigned char)(nums[m]);
        }
        cout << "decrypt result:" << endl;
        cout << decrypt(key, encrypt_msg, nums.size()) << endl;

      } else {
        cout << "input ciphertext error, please check." << endl;
      }

    } else {
      cout << "argv[3] should be -e or -d" << endl;
    }
  } else {
    cout << "need -k and should be first" << endl;
    }
  return 0;
}