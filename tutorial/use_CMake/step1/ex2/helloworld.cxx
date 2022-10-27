#include <iostream>
#include <string>
#include <memory> //使用shared指针的必须

int main(int argc, char *argv[]){
    const double inputValue = std::stod(argv[1]);
    std::shared_ptr<std::string> s=std::make_shared<std::string>("Hello CMake World in CXX11");
    // 当然，你也可以用auto，这就是C++。
    // auto s = std::make_shared<std::string>("Hello CMake World in CXX11.");
    std::cout<<*s<<inputValue<<std::endl;
    return 0;
}