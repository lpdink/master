#include <iostream>
#include <string>
#include <memory> //使用shared指针的必须
#include "config.h"

int main(int argc, char *argv[]){
    std::shared_ptr<std::string> s=std::make_shared<std::string>("Hello CMake World in CXX11");
    // 当然，你也可以用auto，这就是C++。
    // auto s = std::make_shared<std::string>("Hello CMake World in CXX11.");
    std::cout<<*s<<std::endl;
    std::cout<<"Project Version is "<<HelloWorld_VERSION_MAJOR<<"."<<HelloWorld_VERSION_MINOR<<std::endl;
    return 0;
}