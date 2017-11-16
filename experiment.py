from matplotlib import pyplot as plt
import numpy as np
from scipy.signal import fftconvolve
from scipy import fftpack

if __name__ == '__main__':
    t = np.arange(0.0, 10.0, 0.01)
    w1 = 25.0
    w2 = 12.0
    w3 = 12.5

    signal = np.sin(t * w1) + np.cos(t * w2)
    conv_targ = np.cos(t * w3)

    fftconv2 = fftconvolve(signal, conv_targ, 'full')
    normal_conv = np.convolve(signal, conv_targ, 'same')

    # plt.plot(t, signal)
    n = len(signal) + len(conv_targ) - 1
    fslice = len(signal)

    sig_fft = fftpack.rfft(signal, n=n)
    targ_fft = fftpack.rfft(conv_targ, n=n)
    fftconv = fftpack.irfft(sig_fft * targ_fft, n=n)[0:n].copy()

    print signal.shape
    print sig_fft.shape
    print fftconv.shape
    print normal_conv.shape

    plt.plot(fftconv, label='fftconv')
    plt.plot(fftconv2, label='fftconv2')
    # plt.plot(sig_fft * targ_fft)
    # plt.plot(normal_conv, label='normal_conv')
    plt.legend()

    plt.show()
