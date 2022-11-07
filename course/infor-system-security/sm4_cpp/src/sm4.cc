#include "sm4.h"
namespace sm4
{
    
    // void encoder(std::vector<unsigned char> text_bytes){
    //     // TODO
    //     // 强转是必须的，否则为0时好像会core，待测试。
    //     for(int i=0;i<(int)text_bytes.size();i++){

    //     }
    // }

    SM4Key::SM4Key(std::string key_)
    {
        // string to byte
        this->key = new unsigned char[16];
        memcpy(this->key, key_.data(), key_.size());
    }

    SM4Key::~SM4Key()
    {
        delete[] this->key;
        this->key = nullptr;
    }

   std::string SM4Key::encrypt(std::string plain_text, bool padding)
    {
        // padding
        int text_length = plain_text.size();
        int res = text_length%16;
        if(res!=0){
            text_length+=16-res;
        }
        std::vector<unsigned char> text_bytes(text_length);
        memcpy(&text_bytes[0], plain_text.data(), text_length);
        
        for(int i=0;i<32;i++){
            
        }
        
    }
}