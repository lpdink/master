import librosa
import numpy as np
from copy import deepcopy
from collections.abc import Container

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
    # 要获取原音频采样率，sr需要指定为None.
    data, sr = librosa.load(file_name, sr=None)
    return data, duration, sr

def preemphasis(data, a=0.98):
    """预加重，公式:s`(n)=s(n)-a*s(n-1)  a≈0.98

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
        rst[i]=rst[i]-a*rst[i-1]
    return rst

def framing(data, frame_length=2048, hop_size=512):
    """分帧，将data分为多个frame_length长度的二维数组，
        帧与帧之间存在重叠，故指定跳数hop_size，一般要求hop_size<frame_length/2

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
    fn = (singal_length-frame_length)/hop_size
    # 向上取整，以保留所有帧
    fn = int(np.ceil(fn))
    # 如果有105个点,求补充0的数量? 多走一帧的开始:fn*step，+frame_length成为结尾，减去原采样点的数量得解。
    # 80-100, 90-110，补充5个0. 计算方法是(fn*step+frame_length)-singal_length
    zero_nums = (fn*hop_size+frame_length)-singal_length
    zero_array = np.zeros(zero_nums)
    # 拼接
    tmp_data = np.array(deepcopy(data))
    zero_array = zero_array.astype(tmp_data.dtype)
    tmp_data = np.concatenate((tmp_data, zero_array))
    # np.tile(A, times) 把数字A重复times次，times可以是高维的,本方法很好用.
    rst = np.array([tmp_data[index:index+frame_length] for index in range(fn)]).astype(tmp_data.dtype)
    return rst

def hamming(data, M):
    """对data加hanmming窗

    Args:
        data (List[List[float]]): 分帧后的音频数据
        M (int): 窗口大小，一般等于帧长

    Returns:
        List[float]: 加窗结果
    """
    # data.shape=(78.2048), 
    hanwindow = np.hamming(M)
    return data*hanwindow

if __name__=="__main__":
    data, duration, sr = read_wav("./resources/waves/test.wav")
    # data:<class 'numpy.ndarray'>, (41885,) duration=1.899546485260771(float), sr=22050(float)
    data = preemphasis(data)
    frame_length, hop_size = 2048, 512
    frames = framing(data, frame_length, hop_size)
    windowed = hamming(frames, frame_length)
    breakpoint()