#include <time.h>
#include <vector>
#include <memory>
#include <string>
#include <iostream>
#include "sm4.h"
using namespace sm4;

int main(){
    // any 16-byte length key.
    std::string key = "mnbvcxzlkjhgfdsa";
    std::string msg = "a msg length 16.";
    auto sm4 = std::make_shared<SM4Key>(key);
    clock_t start, end;
    double duration;
    std::vector<double> durations;
    std::vector<int> sizes;
    //encrypt
    for(int i=16;i<=16e7;i*=2){
        start = clock();
        // encrypt(key, msg);
        sm4->encrypt(msg);
        end = clock();
        msg = msg+msg;
        //duration: ms
        duration=double(end-start)*1e3/CLOCKS_PER_SEC;
        durations.push_back(duration);
        sizes.push_back(msg.size());
    }
    for(int i=0;i<(int)durations.size();i++){
        std::cout<<durations[i]<<" "<<sizes[i]<<std::endl;
    }
    durations.clear();
    sizes.clear();
    std::cout<<std::endl;
    // //decrypt
    // for(int i=16;i<=16e7;i*=2){
    //     // expand basic str to length i.
    //     start = clock();
    //     encrypt(key, msg);
    //     end = clock();
    //     msg = msg+msg;
    //     //duration: ms
    //     duration=double(end-start)*1e3/CLOCKS_PER_SEC;
    //     durations.push_back(duration);
    //     sizes.push_back(msg.size());
    // }
    // for(int i=0;i<durations.size();i++){
    //     std::cout<<durations[i]<<" "<<sizes[i]<<std::endl;
    // }



}