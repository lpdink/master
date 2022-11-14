#ifndef SM4_H
#define SM4_H
#include <memory.h>

#include <string>
namespace sm4 {
#ifdef __cplusplus
extern "C" {
#endif
void encrypt(std::string &key, std::string &msg, unsigned char *rst);

std::string decrypt(std::string &key, unsigned char *rst, int num);
#ifdef __cplusplus
}
#endif
}  // namespace sm4
#endif