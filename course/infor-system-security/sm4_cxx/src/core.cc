#include "core.h"

#include <stdio.h>
#include <string.h>

namespace sm4 {
static inline uint32 load_uint32_be(byte *bytes, uint32 i) {
  uint32 rst = ((uint32)bytes[4 * i] << 24) | ((uint32)bytes[4 * i + 1] << 16) |
               ((uint32)bytes[4 * i + 2] << 8) | ((uint32)bytes[4 * i + 3]);
  return rst;
}

static inline void store_uint32_be(uint32 res, byte *rst) {
  rst[0] = (byte)(res >> 24);
  rst[1] = (byte)(res >> 16);
  rst[2] = (byte)(res >> 8);
  rst[3] = (byte)(res);
}

static inline uint32 rotl(uint32 &x, uint32 n) {
  return (x << n) | (x >> (32 - n));
}

static inline void swap(uint32 &a, uint32 &b) {
  uint32 c(a);
  a = b;
  b = c;
}

// sbox变换
static byte sm4_sbox_transfer(byte inch) {
  byte *pTable = (byte *)sm4_sbox;
  byte retVal = (byte)(pTable[inch]);
  return retVal;
}

// 合成变换T，进行非线性t变换和线性L变换
static uint32 sm4_lt(uint32 ka) {
  uint32 bb = 0;
  uint32 c = 0;
  byte a[4];
  byte b[4];
  store_uint32_be(ka, a);
  b[0] = sm4_sbox_transfer(a[0]);
  b[1] = sm4_sbox_transfer(a[1]);
  b[2] = sm4_sbox_transfer(a[2]);
  b[3] = sm4_sbox_transfer(a[3]);
  bb = load_uint32_be(b, 0);
  c = bb ^ (rotl(bb, 2)) ^ (rotl(bb, 10)) ^ (rotl(bb, 18)) ^ (rotl(bb, 24));
  return c;
}

// 轮函数F
static inline uint32 sm4_f(uint32 x0, uint32 x1, uint32 x2, uint32 x3,
                           uint32 rk) {
  return (x0 ^ sm4_lt(x1 ^ x2 ^ x3 ^ rk));
}

// 计算轮密钥
static uint32 sm4_get_rk(uint32 ka) {
  uint32 bb = 0;
  uint32 rk = 0;
  byte a[4];
  byte b[4];
  store_uint32_be(ka, a);
  b[0] = sm4_sbox_transfer(a[0]);
  b[1] = sm4_sbox_transfer(a[1]);
  b[2] = sm4_sbox_transfer(a[2]);
  b[3] = sm4_sbox_transfer(a[3]);
  bb = load_uint32_be(b, 0);
  rk = bb ^ (rotl(bb, 13)) ^ (rotl(bb, 23));
  return rk;
}
// byte to uint32 key.
void sm4_get_key(int mode, uint32 rst_key[32], byte key[16]) {
  uint32 MK[4];
  uint32 k[36];
  uint32 i = 0;

  MK[0] = load_uint32_be(key, 0);
  MK[1] = load_uint32_be(key, 1);
  MK[2] = load_uint32_be(key, 2);
  MK[3] = load_uint32_be(key, 3);
  k[0] = MK[0] ^ sm4_fk[0];
  k[1] = MK[1] ^ sm4_fk[1];
  k[2] = MK[2] ^ sm4_fk[2];
  k[3] = MK[3] ^ sm4_fk[3];
  for (; i < 32; i++) {
    k[i + 4] = k[i] ^ (sm4_get_rk(k[i + 1] ^ k[i + 2] ^ k[i + 3] ^ sm4_ck[i]));
    rst_key[i] = k[i + 4];
  }
  // 解密时交换密钥顺序
  if (mode == sm4_decrypt) {
    for (i = 0; i < 16; i++) {
      swap(rst_key[i], rst_key[31 - i]);
    }
  }
}

void sm4_crypt(uint32 sk[32], byte input[16], byte output[16]) {
  uint32 i = 0;
  uint32 ulbuf[36];

  memset(ulbuf, 0, sizeof(ulbuf));
  ulbuf[0] = load_uint32_be(input, 0);
  ulbuf[1] = load_uint32_be(input, 1);
  ulbuf[2] = load_uint32_be(input, 2);
  ulbuf[3] = load_uint32_be(input, 3);

  while (i < 32) {
    ulbuf[i + 4] =
        sm4_f(ulbuf[i], ulbuf[i + 1], ulbuf[i + 2], ulbuf[i + 3], sk[i]);
    i++;
  }
  store_uint32_be(ulbuf[35], &output[0]);
  store_uint32_be(ulbuf[34], &output[4]);
  store_uint32_be(ulbuf[33], &output[8]);
  store_uint32_be(ulbuf[32], &output[12]);
}
}  // namespace sm4