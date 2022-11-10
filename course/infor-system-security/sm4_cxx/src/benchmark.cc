#include <time.h>

#include <fstream>
#include <iostream>
#include <string>

#include "sm4.h"
using namespace sm4;
using namespace std;

static string ACC_PATH = "../acc.txt";
static const int SPEED_TEST_TIMES = 1000;
static unsigned char encrypt_msg[655360];
void test_acc() {
  ifstream infile(ACC_PATH);
  if (infile.is_open() == false) {
    cout << "need file named acc.txt in ../ to test acc." << endl;
    return;
  }
  string line;
  string key, msg, decrypt_msg;
  int err = 0, line_nums = 0;
  while (getline(infile, line)) {
    key = line.substr(0, 16);
    msg = line.substr(17);
    encrypt(key, msg, encrypt_msg);
    decrypt_msg = decrypt(key, encrypt_msg, msg.size());
    if (decrypt_msg != msg) err++;
    line_nums++;
  }
  infile.close();
  cout << "acc test done, failed: " << err << " in " << line_nums << endl;
}

void test_speed() {
  string key, msg, decrypt_msg;
  key = "1234567890123456";
  msg = "a msg length 16.";
  clock_t start, end;
  double duration;
  for (int i = 0; i <= 12; i++) {
    duration = 0;
    for (int j = 0; j < SPEED_TEST_TIMES; j++) {
      start = clock();
      encrypt(key, msg, encrypt_msg);
      end = clock();
      duration += (double)(end - start) / CLOCKS_PER_SEC;
    }
    cout << "encrypt msg length " << msg.size() << ", " << SPEED_TEST_TIMES
         << " times use: " << duration << "s" << endl;
    duration = 0;
    for (int j = 0; j < SPEED_TEST_TIMES; j++) {
      start = clock();
      decrypt_msg = decrypt(key, encrypt_msg, msg.size());
      end = clock();
      duration += (double)(end - start) / CLOCKS_PER_SEC;
    }
    cout << "decrypt msg length " << msg.size() << ", " << SPEED_TEST_TIMES
         << " times use: " << duration << "s" << endl;
    msg += msg;
  }
}

int main() {
  test_acc();
  test_speed();
}