#ifndef sm4_h
#define sm4_h
#include <string.h>
#include <iostream>
#include <vector>

namespace sm4
{
    class SM4Key
    {
    public:
        SM4Key(std::string key_);
        ~SM4Key();

        std::string encrypt(std::string plain_text, bool padding = true);

        std::string decrypt(std::string cipher_text, bool padding = true);

    private:
        unsigned char* key;
    };
}
#endif // sm4_h