#include "sm4.h"

#include "core.h"
namespace sm4 {

void encrypt(std::string &key, std::string &msg, unsigned char *rst) {
  uint32 rst_key[32];
  std::string padding_text = msg, rst_msg, tmp;
  sm4_get_key(sm4_encrypt, rst_key, (byte *)key.data());
  if (msg.size() % 16 != 0)
    padding_text = msg + std::string(16 - msg.size() % 16, '0');
  int block_nums = padding_text.size() / 16;
  // slice to 16x
  for (int i = 0; i < block_nums; i++) {
    sm4_crypt(rst_key, (byte *)padding_text.substr(i * 16, 16).data(),
              rst + i * 16);
  }
}
byte decrypt_mem[655360];
std::string decrypt(std::string &key, unsigned char *encrypt, int num) {
  uint32 rst_key[32];
  int padding_num = num;
  if (padding_num % 16 != 0) padding_num += 16 - padding_num % 16;
  memcpy(decrypt_mem, encrypt, padding_num);

  sm4_get_key(sm4_decrypt, rst_key, (byte *)key.data());
  for (int i = 0; i < (int)(padding_num / 16); i++) {
    sm4_crypt(rst_key, encrypt + i * 16, decrypt_mem + i * 16);
  }
  std::string rst = (char *)decrypt_mem;
  return rst.substr(0, num);
}

}  // namespace sm4