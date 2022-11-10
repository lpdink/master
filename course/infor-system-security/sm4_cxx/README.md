# SM4对称加密算法的C++实现
[English](README_en.md) | 中文
> 参考 [pypi库 sm4](https://pypi.org/project/sm4/) 实现
## 环境需要
```
linux
cmake
```
## 编译
```
bash build.sh
```
## 二进制使用
```
# 在编译产物.sm4_build目录下
# 加密
sm4 -k key -e plaintext
# 解密
sm4 -k key -d ciphertext
```
注意：
- SM4算法要求密钥是16字节(128位)。
- 待加密明文需要是16字节的倍数，如果不是，会用0填充。  
- 待解密密文需要是16字节的倍数。
## 库使用
拷贝安装目录.sm4_install到您的项目，引用include下的头文件，链接lib下的静态库或动态库。  
## 测试
二进制benchmark可以在.sm4_build下找到，它进行两项测试：
- 读取上层目录的acc.txt，以每行的前16个字符作为key，后面的字符作为text进行加解密，验证加解密结果与text的一致性。如果acc.txt不存在，跳过测试。
- 生成16，32，64...65536长度的文本，对每个文本，重复1000次加解密，测试时间。
## 性能
![img](tools/speed.png)  
64  Intel(R) Xeon(R) Gold 6138 CPU @ 2.00GHz