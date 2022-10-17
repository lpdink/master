import os
import librosa
import soundfile
from tqdm import tqdm
from multiprocessing import Pool
from functools import partial

RAW_DIR_PATH="change here"
RST_DIR_PATH="change here"

TARGET_SR=16000
PROCESS_NUM=32

def resample(file_path, rst_file_path, target_sr):
    """对wav音频重采样

    Args:
        file_path(str): 原文件路径
        rst_file_path(str): 重采样后文件路径
        target_sr (int): 目标采样率
    """
    audio, sr = librosa.load(file_path, sr=None, mono=True)
    # fix:调整重采样信号的长度，使得时长不变
    # scale：缩放重采样信号，使得能量不变
    audio_hat = librosa.resample(audio, orig_sr=sr, target_sr=target_sr, fix=True, scale=False)
    soundfile.write(rst_file_path, audio_hat, target_sr)

def _resample(args, target_sr):
    """对wav音频重采样

    Args:
        target_sr (int): 目标采样率
        args[0](str): 原文件路径
        args[1](str): 重采样后文件路径
    """
    file_path, rst_file_path = args
    audio, sr = librosa.load(file_path, sr=None, mono=True)
    # fix:调整重采样信号的长度，使得时长不变
    # scale：缩放重采样信号，使得能量不变
    audio_hat = librosa.resample(audio, orig_sr=sr, target_sr=target_sr, fix=True, scale=False)
    soundfile.write(rst_file_path, audio_hat, target_sr)


if __name__=="__main__":
    wav_filenames = [file_name for file_name in os.listdir(RAW_DIR_PATH) if file_name.endswith(".wav")]

    raw_paths = [os.path.join(RAW_DIR_PATH, file_name) for file_name in wav_filenames]

    dst_paths = [os.path.join(RST_DIR_PATH, file_name) for file_name in wav_filenames]

    with Pool(processes=PROCESS_NUM) as pool:
        result = list(tqdm(pool.imap(partial(_resample, target_sr=TARGET_SR),list(zip(raw_paths, dst_paths))), total=len(raw_paths)))
