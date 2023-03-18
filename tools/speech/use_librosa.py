import librosa
import numpy as np
from copy import deepcopy
from collections.abc import Container

"""
预加重，分帧，加窗，
"""


def read_wav(file_name):
    """用librosa读取wav文件，返回数据，采样率和duration

    Args:
        file_name (str): wav文件路径

    Returns:
        data: numpy.ndarray, 音频数据
        duration: float, 音频时长
        sr：int, 采样率
    """
    # get_duration方法的默认调用不是对path的，故显式指定filename参数
    duration = librosa.get_duration(filename=file_name)
    # 要获取原音频采样率，sr需要指定为None.mono=True使转换为单声道
    data, sr = librosa.load(file_name, sr=None, mono=True)
    return data, duration, sr


def preemphasis(data, a=0.98):
    """预加重，公式:s`(n)=s(n)-a*s(n-1)  a≈0.98
    进行预加重的原因是：语音经发声者的口唇辐射发出，会受到唇端辐射抑制，高频能量被明显降低，
    语音信号的频率提高2倍时，功率谱的幅度下降6dB.即语音信号的高频部分受到的抑制较大。
    预加重就是为了补偿语音信号高频部分的振幅。

    Args:
        data (List[int]): 待加重的语音数据，一维数组
        a (float, optional): 预加重系数. Defaults to 0.98.

    Returns:
        rst: List[float] 加重结果，使用了deepcopy，不会修改输入的data.
    """
    # 要求输入的是一维数组(即元素不是容器类型)
    assert all(not isinstance(item, Container) for item in data)
    length = len(data)
    rst = deepcopy(data)
    for i in range(1, length):
        rst[i] = rst[i] - a * rst[i - 1]
    return rst


def framing(data, frame_length=2048, hop_size=512):
    """分帧，将data分为多个frame_length长度的二维数组，
        帧与帧之间存在重叠，故指定跳数hop_size，一般要求hop_size<frame_length/2
    语音信号是一个短时平稳信号，浊音是有规律的声带振动，即基音频率在短时范围内相对稳定。
    可以认为，10~30ms内的语音片段是一个准稳态的，分为一帧。
    一帧常规定为20ms~25ms，在采样率16Khz下，25ms意味着400个采样点。
    两帧之间的基音可能变化，故重叠取帧，帧移10ms，重叠50%~60%。

    Args:
        data (List[float]): 预加重的音频数据
        frame_length (int, optional): 每帧长. Defaults to 2048.
        hop_size (int, optional): 步长. Defaults to 512.

    Returns:
        rst: List[List[float]] 分帧结果
    """
    # 要求输入的是一维数组
    assert all(not isinstance(item, Container) for item in data)
    singal_length = len(data)
    # 计算帧数
    # 假设100个点，帧长20，每次移动10，求分几帧？
    # 1-20, 10-30, 20-40...80-100 显然是8帧，计算方法是(采样点数-帧长)/step
    fn = (singal_length - frame_length) / hop_size
    # 向上取整，以保留所有帧
    fn = int(np.ceil(fn))
    # 如果有105个点,求补充0的数量? 多走一帧的开始:fn*step，+frame_length成为结尾，减去原采样点的数量得解。
    # 80-100, 90-110，补充5个0. 计算方法是(fn*step+frame_length)-singal_length
    zero_nums = (fn * hop_size + frame_length) - singal_length
    zero_array = np.zeros(zero_nums)
    # 拼接
    tmp_data = np.array(deepcopy(data))
    zero_array = zero_array.astype(tmp_data.dtype)
    tmp_data = np.concatenate((tmp_data, zero_array))
    # np.tile(A, times) 把数字A重复times次，times可以是高维的,本方法很好用.
    rst = np.array(
        [tmp_data[index : index + frame_length] for index in range(fn)]
    ).astype(tmp_data.dtype)
    return rst


def hamming(data, M):
    """对data加hanmming窗
    分帧相当于对信号加了矩形窗，会发生过强的频谱泄露

    Args:
        data (List[List[float]]): 分帧后的音频数据
        M (int): 窗口大小，一般等于帧长

    Returns:
        List[float]: 加窗结果
    """
    # data.shape=(78, 2048),
    hanwindow = np.hamming(M)
    return data * hanwindow


def _stft(audio, n_fft=2048, hop_length=512, window="hann"):
    # 短时傅里叶变换
    # zz = librosa.stft(y, n_fft=2048, hop_length=None, win_length=None, window='hann', center=True, pad_mode='reflect')
    # librosa的stft是自带加窗的
    # stfted.shape==(1025, 82) 这里因为填充信号，所以帧数多一些，shape=((1+n_fft/2), t)
    # 每帧有1025个值，每个值都是一个复数,如:0.0103363 +0.00675756j，这代表该点的频率值。
    # 使用复数表示频率，需要参考极坐标
    return librosa.stft(audio, n_fft=n_fft, hop_length=hop_length, window=window)


def _magphase(stfted, power):
    """取得stft的幅值和相位矩阵

    Args:
        stfted (List[List[complex]]): stft结果
        power (int): 幅度谱的指数，1代表能量，2代表功率...

    Returns:
        D_mag: 幅值矩阵
        D_phase: 相位矩阵
        两个矩阵的shape与stfted一致，但并非简单的6.2708445e-05-5.29952449e-05j的实数和虚数部分分离
        D_mag其实是复数的模矩阵，phase = np.exp(1j * np.angle(D(F, T)))
    """
    D_mag, D_phase = librosa.magphase(stfted, power=power)
    return D_mag, D_phase


def _istft(stfted, hop_length=512, win_length=2048, window="hann", center=True):
    """逆stft变换，一般不需要额外指定参数，librosa可以从stfted中计算出hop和win_length.
        先进行stft，再做istft，会丢失一些信息，采样点数量也会变化，但十分小。
    Args:
        stfted (List[List[complex]]): 经过stft变换后的矩阵
        hop_length (int, optional): 帧移. Defaults to 512.
        win_length (int, optional): 窗口大小. Defaults to 2048.
        window (str, optional): 窗口类型. Defaults to 'hann'.
        center (bool, optional): 与进行stft变换时保持一致. Defaults to True.

    Returns:
        audio: 时域信号
    """
    return librosa.istft(
        stfted,
        hop_length=hop_length,
        win_length=win_length,
        window=window,
        center=center,
    )


if __name__ == "__main__":
    data, duration, sr = read_wav(
        "../../book/pytorch_introduction/chapter1/resources/waves/test.wav"
    )
    # data:<class 'numpy.ndarray'>, (41885,) duration=1.899546485260771(float), sr=22050(float)
    # data = preemphasis(data)
    # frame_length, hop_size = 2048, 512
    # frames = framing(data, frame_length, hop_size)
    # windowed = hamming(frames, frame_length)

    stfted = librosa.stft(data, n_fft=2048, hop_length=512, window="hann")
    D_mag, D_phase = librosa.magphase(stfted, power=1)
    istfted = librosa.istft(stfted)
    breakpoint()
