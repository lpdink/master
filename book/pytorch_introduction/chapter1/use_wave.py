import wave

"""
本P是标准库wave的所有api的使用示范，
使用标准库wave对基本wav协议文件的读取与写入。
是对speech.py的简化。
"""


def read_wav(file_path):
    """从路径中读取wav文件，显示通道数，采样率，帧数，时长(s)，每帧字节数。返回int列表的content

    Args:
        file_path (str): wav文件路径

    Returns:
        List[int]: wav数值信息
    """
    wav_file = wave.open(file_path, "rb")  # 写：wb, 标准库不支持同时读写文件。
    channels = wav_file.getnchannels()
    assert channels == 1
    sampwidth = wav_file.getsampwidth()
    framerate = wav_file.getframerate()
    frames = wav_file.getnframes()
    params = wav_file.getparams()
    print(
        f"channels:{channels}, sampwidth:{sampwidth}, framerate:{framerate}, frames:{frames}, durations:{frames/framerate}(s)"
    )
    # channels:1, sampwidth:2, framerate:22050, frames:41885, durations:1.899546485260771(s)
    print(f"params:{params}")
    # 这里返回的是bytes类型的。根据sampwidth，我们可以将每帧转换为具体的int值。
    data = wav_file.readframes(frames)
    # 需要注意的是，这里是有符号的。
    # 这里有个问题，我怎么知道这个wav是大端还是小端呢？
    int_data = [
        int.from_bytes(data[index : index + 2], "little", signed=True)
        for index in range(0, len(data), 2)
    ]
    assert len(int_data) == frames  # 转换得到的list长度应该与frames相等。
    wav_file.close()
    return int_data


def draw_waveform(data):
    """绘制一维数据波形图，写出到外存

    Args:
        data (None): None
    """
    import matplotlib.pyplot as plt

    plt.plot(range(len(data)), data)
    plt.savefig("waveform2.png")


def write_wav(file_name="sin.wav", framerate=16000, f=1000, E=10000):
    """手写wav波，可以说，在png里能看到的听不到，看不到的听得到。

    Args:
        file_name (str, optional): 写出wav文件名. Defaults to "sin.wav".
        framerate (int, optional): 采样率. Defaults to 16000.
        f (int, optional): 正弦波频率. Defaults to 1000.
        E (int, optional): 音高. Defaults to 10000.
    """
    wav_file = wave.open(file_name, "wb")
    # 这里设置1通道，每帧2字节，采样率16k，可以指定帧数，但这里不指定，让wave自己去算。
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(framerate)
    # 在2*pi范围内，生成一秒(16k个点)的sin，注意，写出的内容应该是int16的，
    # 这里不用numpy有点困难...
    import numpy as np

    # 固定生成1s
    x = np.linspace(0, 1, framerate)
    data = (np.sin(2 * np.pi * x * f) * E).astype(np.int16)
    draw_waveform(data)
    wav_file.writeframes(data)
    wav_file.close()


if __name__ == "__main__":
    file_path = "./resources/waves/test.wav"
    data = read_wav(file_path)
    # 可以将data通过matplotlib画出来，就得到了波形图
    # draw_waveform(data)
    # 生成sin函数，写出为wav文件
    write_wav(f=1)
