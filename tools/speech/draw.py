import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt


def draw_wav(file_path):
    """绘制wav的时域波形

    Args:
        file_path (str): wav文件路径
    """
    audio, sr = librosa.load(file_path, sr=None, mono=True)
    librosa.display.waveshow(audio, sr=sr)
    plt.savefig("tmp.png")


def draw_spec(file_path):
    audio, sr = librosa.load(file_path, sr=None, mono=True)
    plt.figure()
    # 在音乐处理中，n_fft推荐为2048,在speech中，推荐为512。hop_length推荐为其1/4.
    stfted = librosa.stft(audio, n_fft=2048, hop_length=512)
    # 频域幅值, 也可以通过librosa.magphase取得，第一项。
    S = np.abs(stfted)
    # 将幅度谱转换为dB单位
    D = librosa.amplitude_to_db(S, ref=np.max)
    plt.subplot(2, 1, 1)
    # 线性谱，y轴线性增加
    librosa.display.specshow(D, y_axis="linear")
    # 本行在右侧添加dB颜色图例
    plt.colorbar(format="%+2.0f dB")
    plt.title("Linear-frequency power spectrogram")

    plt.subplot(2, 1, 2)
    # 对数谱，y轴指数增加
    librosa.display.specshow(D, y_axis="log")
    plt.colorbar(format="%+2.0f dB")
    plt.title("Log-frequency power spectrogram")
    plt.savefig("spec.png")


if __name__ == "__main__":
    file_path = "../../book/pytorch_introduction/chapter1/resources/waves/test.wav"
    # draw_wav(file_path)
    draw_spec(file_path)
