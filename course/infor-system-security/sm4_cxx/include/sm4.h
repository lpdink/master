#include <memory.h>

#include <string>
namespace sm4 {
void encrypt(std::string &key, std::string &msg, unsigned char *rst);

std::string decrypt(std::string &key, unsigned char *rst, int num);
}  // namespace sm4