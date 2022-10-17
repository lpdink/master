"""
在VScode中，我们能看到准备好的test.wav文件的格式是：
encoding	pcm_s16le 
# PCM:脉冲编码调制，Pulse-code Modulation, PCM，
# s16：有符号16位范围，即-32768~32767. 振幅越大，声音的强度越大
# le:小端编码，一个字节8位，该语音是16位的，故一个采样点需要用两个字节去表示，所以需要表明大小端，小端意味着先存低字节，再存高字节。
format	s16
number_of_channel	1 (mono) # 单声道
sample_rate	22050 # 采样率，22050，这是一个常见标定，因为人耳的识别范围是20-20kHz.
file_size	83814 byte # 文件大小
duration	1.899546485260771s
"""


def read_waves(file_path):
    with open(file_path, "rb") as file:
        head = bin_file.read(44)
    RIFF = head[:4]  # RIFF 固定的
    assert RIFF.decode() == "RIFF"
    length = int.from_bytes(
        head[4:8], "little"
    )  # 文件长度 unit32 int.from_bytes(length, 'little') 2**32B为4GB，故wav文件不能超过4G。
    WAVE = head[8:12]  # 固定为WAVE
    assert WAVE.decode() == "WAVE"
    fmt = head[12:16]  # 固定为 "fmt "
    assert fmt.decode() == "fmt "
    h16_20 = head[16:20]  # 固定为10 00 00 00，表示是PCM
    assert h16_20.decode() == "\x10\x00\x00\x00"
    h21_22 = head[20:22]  # 固定为01 00，表示是PCM
    assert h21_22.decode() == "\x01\x00"
    channel = int.from_bytes(head[22:24], "little")  # 通道数
    sample_rate = int.from_bytes(head[24:28], "little")  # 采样率
    code_rate = int.from_bytes(
        head[28:32], "little"
    )  # 码率 采样率x位深度x通道数/8 比如双通道的44.1K 16位采样的码率为176400
    h33_34 = int.from_bytes(head[32:34], "little")  # 采样一次，占内存大小 ： 位深度x通道数/8
    depth = int.from_bytes(head[34:36], "little")  # 采样深度
    data = head[36:40]  # 固定为data
    assert data.decode() == "data"
    data_length = int.from_bytes(head[40:44], "little")  # 数据部分的长度，与文件长度的差值应该等于36
    assert length - data_length == 36
    return sample_rate, channel, depth


if __name__ == "__main__":
    with open("./resources/waves/test.wav", "rb") as bin_file:
        head = bin_file.read(44)
