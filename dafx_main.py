#!/usr/bin/env python
#
#

from pylab import *
from scikits.audiolab import wavread, wavwrite
from dafx_filter import *
from numpy import *
from scipy import stats

fs = 44100.


def pinknoise(n, rvs=stats.norm.rvs):
    k = min(int(floor(log(n) / log(2))), 6)
    pink = zeros((n, ), float64)
    m = 1
    for i in range(k):
        p = int(ceil(float(n) / m))
        pink += repeat(rvs(size=p), m, axis=0)[:n]
        m <<= 1

    return pink / k


def low_demo(snd, start, stop):
    # lowpass at starting at 100 and ending at 1000

    freq = linspace(start, stop, len(snd))
    normal_freq = 2 * freq / fs
    lowpass_y = aplowpass(snd, normal_freq)

    wavwrite(lowpass_y, "aplow_demo.wav", fs)


def high_demo(snd, start, stop):

    freq = linspace(start, stop, len(snd))
    normal_freq = 2 * freq / fs
    highpass_y = aphighpass(snd, normal_freq)

    wavwrite(highpass_y, "aphigh_demo.wav", fs)


def allpass_demo(snd, amt, blend, feedback, feedforward):

    y = allpass(snd, amt, blend, feedback, feedforward)
    wavwrite(y, "allpass_demo.wav", fs)


def iir_comb_demo(snd, amt, blend, feedback):

    y = iir_comb(snd, amt, blend, feedback)
    wavwrite(y, "iir_comb_demo.wav", fs)


def var_allpass_demo(snd, amt, width, blend, feedback, feedforward, breakPoint):

    y = universal_comb_variable(snd, amt / 1000., width / 1000., blend, feedforward, feedback, breakPoint)
    wavwrite(y, "var_allpass_demo.wav", fs)


def main():

    # import soundfile
    snd = wavread('trumpet.wav')[0]
    kick = wavread('kick.wav')[0]
    amb = wavread('amb.wav')[0]
    amb = amb * 0.8                 # reduce gain of this soundfile a little bit
    
    print len(amb)
    #low_demo(snd, 10., 500.)
    #high_demo(snd, 10000., 10.)
    #allpass_demo(snd, 1000, -find_c(1000., fs), find_c(1000., fs), 1.0)
    #iir_comb_demo(kick, 100, 0.5, -0.5)

    t = len(amb) / fs
    period = 1.0 / fs
    t_v = arange(0.0, t, period)
    delayTime = 2.0
    width = 1.0
    freq = 1
    breakPoint = (sin(2. * pi * freq * t_v))
    #breakPoint = linspace(1, -1, len(amb))

    #var_allpass_demo(snd, delayTime / 1000., width / 1000., -find_c(8000, fs), find_c(8000, fs), 1.0, breakPoint)
    #var_allpass_demo(amb, delayTime / 1000., width / 1000., 0.5, -0.5, 0.0, breakPoint)

    # flanger
    var_allpass_demo(amb, delayTime, width, 0.7, 0.7, 0.7, breakPoint)

    # chorus
    #breakPoint = pinknoise(len(snd))
    #breakPoint = breakPoint / max(breakPoint)

    #var_allpass_demo(snd, 20., 2., 0.7, -0.7, 1.0, breakPoint)


if __name__ == '__main__':
    main()





