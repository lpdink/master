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
- SM4 requires 16-byte length(128-bit length) key, auto-padding for key less than 16-byte with zero, auto-cut prior 16-byte for key more than 16-byte.
- plaintext should be a multiple of 16, otherwise padding with zero.
- ciphertext should be a multiple of 8, otherwise padding with zero. After decryption, program will throw the padding characters away.
### Lib Usage
copy folder .sm4_install to your project, reference header file in folder include, linking to static or shared library under lib folder.
## Performance
64  Intel(R) Xeon(R) Gold 6138 CPU @ 2.00GHz