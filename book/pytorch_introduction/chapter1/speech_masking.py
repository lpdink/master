import scipy.io.wavfile as wav
import numpy as np
from scipy.fftpack import fft
from scipy.fftpack import ifft
from scipy import signal
import scipy
import librosa
import soundfile


def compute_PSD_matrix(audio, window_size):
    """
	First, perform STFT.
	Then, compute the PSD.
	Last, normalize PSD.
    """
    win = np.sqrt(8.0 / 3.0) * librosa.core.stft(audio, center=False)
    z = abs(win / window_size)
    psd_max = np.max(z * z)
    psd = 10 * np.log10(z * z + 0.0000000000000000001)
    maxk = np.max(psd)
    # breakpoint()
    PSD = 96 - maxk + psd
    return PSD, psd_max, maxk


def Bark(f):
    """returns the bark-scale value for input frequency f (in Hz)"""
    return 13 * np.arctan(0.00076 * f) + 3.5 * np.arctan(pow(f / 7500.0, 2))


def quiet(f):
    """returns threshold in quiet measured in SPL at frequency f with an offset 12(in Hz)"""
    thresh = (
        3.64 * pow(f * 0.001, -0.8)
        - 6.5 * np.exp(-0.6 * pow(0.001 * f - 3.3, 2))
        + 0.001 * pow(0.001 * f, 4)
        - 12
    )
    return thresh


def two_slops(bark_psd, delta_TM, bark_maskee):
    """
	returns the masking threshold for each masker using two slopes as the spread function 
    """
    Ts = []
    for tone_mask in range(bark_psd.shape[0]):
        bark_masker = bark_psd[tone_mask, 0]
        dz = bark_maskee - bark_masker
        zero_index = np.argmax(dz > 0)
        sf = np.zeros(len(dz))
        sf[:zero_index] = 27 * dz[:zero_index]
        sf[zero_index:] = (-27 + 0.37 * max(bark_psd[tone_mask, 1] - 40, 0)) * dz[
            zero_index:
        ]
        T = bark_psd[tone_mask, 1] + delta_TM[tone_mask] + sf
        Ts.append(T)
    return Ts


def compute_th(PSD, barks, ATH, freqs):
    """ returns the global masking threshold
    """
    # Identification of tonal maskers
    # find the index of maskers that are the local maxima
    length = len(PSD)
    # 用于计算极值点，如果是单调的，返回为空数组。
    masker_index = signal.argrelextrema(PSD, np.greater)[0]
    # if masker_index.size == 0:
    #     return None

    # delete the boundary of maskers for smoothing
    if 0 in masker_index:
        masker_index = np.delete(0)
    if length - 1 in masker_index:
        masker_index = np.delete(length - 1)
    num_local_max = len(masker_index)

    # treat all the maskers as tonal (conservative way)
    # smooth the PSD
    p_k = pow(10, PSD[masker_index] / 10.0)
    p_k_prev = pow(10, PSD[masker_index - 1] / 10.0)
    p_k_post = pow(10, PSD[masker_index + 1] / 10.0)
    P_TM = 10 * np.log10(p_k_prev + p_k + p_k_post)

    # bark_psd: the first column bark, the second column: P_TM, the third column: the index of points
    _BARK = 0
    _PSD = 1
    _INDEX = 2
    bark_psd = np.zeros([num_local_max, 3])
    bark_psd[:, _BARK] = barks[masker_index]
    bark_psd[:, _PSD] = P_TM
    bark_psd[:, _INDEX] = masker_index

    # delete the masker that doesn't have the highest PSD within 0.5 Bark around its frequency
    for i in range(num_local_max):
        next = i + 1
        if next >= bark_psd.shape[0]:
            break

        while bark_psd[next, _BARK] - bark_psd[i, _BARK] < 0.5:
            # masker must be higher than quiet threshold
            if quiet(freqs[int(bark_psd[i, _INDEX])]) > bark_psd[i, _PSD]:
                bark_psd = np.delete(bark_psd, (i), axis=0)
            if next == bark_psd.shape[0]:
                break

            if bark_psd[i, _PSD] < bark_psd[next, _PSD]:
                bark_psd = np.delete(bark_psd, (i), axis=0)
            else:
                bark_psd = np.delete(bark_psd, (next), axis=0)
            if next == bark_psd.shape[0]:
                break

    # compute the individual masking threshold
    delta_TM = 1 * (-6.025 - 0.275 * bark_psd[:, 0])
    Ts = two_slops(bark_psd, delta_TM, barks)
    Ts = np.array(Ts)

    # compute the global masking threshold
    theta_x = np.sum(pow(10, Ts / 10.0), axis=0) + pow(10, ATH / 10.0)
    theta_x = 10 * np.log10(theta_x)
    return theta_x


def generate_th(audio, fs, window_size=2048):
    """
	returns the masking threshold theta_xs and the max psd of the audio
    """
    PSD, psd_max, maxk = compute_PSD_matrix(audio, window_size)
    freqs = librosa.core.fft_frequencies(sr=fs, n_fft=window_size)
    barks = Bark(freqs)

    # compute the quiet threshold
    ATH = np.zeros(len(barks)) - np.inf
    bark_ind = np.argmax(barks > 1)
    ATH[bark_ind:] = quiet(freqs[bark_ind:])

    # compute the global masking threshold theta_xs
    theta_xs = []
    # compute the global masking threshold in each window
    # PSD:[1025, 78],1025由stft产生，78应该是帧数。
    # 本循环遍历所有帧
    for i in range(PSD.shape[1]):
        tmp = compute_th(PSD[:, i], barks, ATH, freqs)
        theta_xs.append(tmp)
    theta_xs = np.array(theta_xs)
    return theta_xs, psd_max, maxk


def get_noise_s(theta_xs, maxk, N):
    # s^2 <=N^2*10^((theta_xs-96+maxk)/10)
    rst = theta_xs - 96 + maxk
    rst = rst / 10
    rst = np.power(10, rst) * N * N
    # rst = np.sqrt(rst)
    return rst


# a*a+b*b=s*s
# s*s*0.6=a*a
# a = sqrt(s^2*t)
def generate_noise(noise_s, a=1):
    rand = np.random.uniform(size=noise_s.shape)
    noise_s = noise_s * a * a
    real = np.sqrt(rand * noise_s)
    unreal = np.sqrt((1 - rand) * noise_s) * 1j
    noise_spec = (real + unreal).T
    rst = librosa.istft(noise_spec, center=False)
    # return noise_spec
    return rst


if __name__ == "__main__":
    sr, audio = wav.read("./resources/waves/test.wav")
    audio = audio.astype(np.float32)
    # librosa的stft会帮你分帧和加窗，故不要自己做。
    # from use_librosa import hamming, framing
    stfted = librosa.stft(audio, center=False)
    # audio = framing(audio)
    # audio = hamming(audio, 2048)
    theta_xs, psd_max, maxk = generate_th(audio, sr)
    noise_s = get_noise_s(theta_xs, maxk, theta_xs.shape[0])
    # noise_spec = generate_noise(noise_s)
    noise = generate_noise(noise_s)
    noise_audio = librosa.istft(stfted, center=False) + noise
    istfted = librosa.istft(stfted, center=False).astype(np.int16)
    noise_audio = noise_audio.astype(np.int16)
    # breakpoint()
    # 叠加
    # noise_audio_spec = stfted+noise_spec
    # 转时域, 记得一定要转int16!!!
    # noise_audio = librosa.istft(noise_audio_spec, center=False).astype(np.int16)
    soundfile.write("noise_audio_handle.wav", noise_audio[512:][:-512], sr)
    soundfile.write("raw_handle.wav", istfted[512:][:-512], sr)
    # breakpoint()

"""
log10(100)=2
添加扰动的范围：
96-maxk+p$ <= theta_xs
p$<=theta_xs-96+maxk
log10S<=(theta_xs-96+maxk)/10
S<=10^((theta_xs-96+maxk)/10)
s^2 <=N^2*10^((theta_xs-96+maxk)/10)



"""
