import os
import librosa
import soundfile
import numpy as np
from tqdm import tqdm
from multiprocessing import Pool
from functools import partial
from scipy import spatial
import h5py

"""
mel频谱：
对于人耳：
1kHz以下，与频率成线性关系
1kHz以上，与频率成对数关系
因此人耳对低频信号比对高频信号更加敏感
由大量心理声学实验得到了一个类似耳蜗作用的滤波器组，用于模拟人耳对不同频段信号的感知能力。

求mel频谱，本质上是对语音幅度谱的一个矩阵乘法变换。
"""
RAW_DIR_PATH = "change here"
RST_DIR_PATH = "change here"


def get_melspec(file_path, rst_file_path=None):
    audio, sr = librosa.load(file_path, sr=None, mono=True)
    mel_spec = librosa.feature.melspectrogram(y=audio, sr=sr, n_fft=256, n_mels=80)
    return audio, mel_spec


if __name__ == "__main__":
    raw_audio, raw = get_melspec(
        "/mnt/data/xiaozeyu/master/book/pytorch_introduction/chapter1/raw_handle.wav"
    )
    noise_audio, noise = get_melspec(
        "/mnt/data/xiaozeyu/master/book/pytorch_introduction/chapter1/noise_audio_handle.wav"
    )
    print(f"mel sim:{1-spatial.distance.cosine(raw.reshape(-1), noise.reshape(-1))}")
    print(
        f"wav sim:{1-spatial.distance.cosine(raw_audio.reshape(-1), noise_audio.reshape(-1))}"
    )
    # breakpoint()
    # h5_file = h5py.File("/mnt/data/xiaozeyu/github/ParallelWaveGAN/resources/dump/sample/raw/raw_new.h5", "w")
    # h5_file["feats"]=raw.T
    # h5_file["wave"]=raw_audio
    # breakpoint()
    # h5_file.close()
    # data_set = h5_file.create_dataset("feats",raw.T.shape,np.float32)
    # breakpoint()
