from numpy import*
from pylab import*
from scipy import signal
import scipy.io
from scipy.io import wavfile

fs,y = wavfile.read("/Users/ShuoLiu/Desktop/la.wav")
offset = 1000

WLen = 2048
w = hanning(WLen)
buf = y[offset:offset+WLen]*w
f = fft(buf)/(WLen/2)
freq = arange(0,WLen,1)
freq = freq*44100/2048
flog = 20*log10(0.00001+abs(f))
# Frequency window
nob = input('length of bins (must be even, e.g. 20) = ');
w1 = hanning(nob)
w1 = w1/sum(w1)
list1 = zeros((WLen-nob)/2)
f_channel = concatenate([list1,w1])
f_channel = concatenate([f_channel,list1])
# FFT of frequency window
fft_channel = fft(fftshift(f_channel))
f2 = f*conj(f)
# Circ. Convolution by FFT-Multiplication-IFFT
energy=real(ifft(fft(f2)*fft_channel));
flog_rms=10*log10(abs(energy));
#10 indicates a combination with sqrt operation
subplot(1,1,1);
#plot(flog)
plot(freq,flog,freq,flog_rms);
ylabel('X(f)/dB');
xlabel('f/Hz ');
axis([0,8000,-40,80]);
title('Short-time spectrum and spectral envelope')
show()

