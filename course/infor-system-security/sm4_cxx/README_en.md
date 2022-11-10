# C++ implementation of SM4 symmetric encryption algorithm
English | [中文](README.md)
> reference to  [pypi sm4](https://pypi.org/project/sm4/)
## Environment
```
linux
cmake
```
## Compile
```
bash build.sh
```
## Usage
### Binary Usage
```
# under .sm4_build folder.
# encrypt
sm4 -k key -e plaintext
# decrypt
sm4 -k key -d ciphertext
```
Note：
- SM4 requires 16-byte length(128-bit length) key.
- plaintext should be a multiple of 16, otherwise padding with zero.
- ciphertext should be a multiple of 16.
### Lib Usage
copy folder .sm4_install to your project, reference header file in folder include, linking to static or shared library under lib folder.
## Performance
![img](tools/speed.png)  
64  Intel(R) Xeon(R) Gold 6138 CPU @ 2.00GHz