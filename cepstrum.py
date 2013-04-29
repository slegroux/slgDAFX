from numpy import*
from pylab import*
from scipy import signal
import scipy.io
from scipy.io import wavfile

fs,y = wavfile.read("/Users/ShuoLiu/Desktop/la.wav")
offset = 1000
# N1: cut quefrency
WLen = 2048
w = hanning(WLen)
buf = y[offset:offset+WLen]*w
f = fft(buf)/(WLen/2)
freq = arange(0,WLen,2)
freq = freq*44100/2048
freq1 = freq[1:WLen/2]
flog = 20*log10(0.00001+abs(f))
#----- plotting the Magnitude -----
subplot(2,1,1);
#plot(freq,flog)
plot(freq1, flog[1:WLen/2]);
ylabel('X(f)/dB');
xlabel('f/Hz'); 
axis([0,8000,-20,80]);
title('Short-time spectrum and spectral shape');

N1=input('cut value for cepstrum (e.g. 150): ');
cep=ifft(flog);
cep[2:N1] = 2*cep[2:N1]
cep[N1+2:WLen]=0
##list2 = 2*cep[2:N1]
##list3 = cep[1]
##list4 = cep[N1]
##cep_cut=list2.insert(0,list3);
##cep_cut=cep_cut.append(list4);
##cep_cut=concatenate([cep_cut,list1]);
flog_cut=real(fft(cep));
#----- plotting the spectral shape -----
subplot(2,1,2); 
plot(freq1, flog_cut[1:WLen/2]);
ylabel('Shape(f)/dB');
xlabel('f/Hz'); 
axis([0,8000,-20,80]);
show()
