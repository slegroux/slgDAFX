from scipy import *
from pylab import *
from scipy.io import wavfile
import numpy
import pyaudio
import wave
import sys


execfile('rec.py')

n1 = 256
n2 = n1
N = 1024

(fs,signalin1) = wavfile.read('query.wav')
(fs,signalin2) = wavfile.read('v1.wav')

win = hanning(N)
L = min(signalin1.size, signalin2.size)
a = zeros(N)
b = zeros(N - numpy.mod(L, n1))
DAFx_in1 = numpy.concatenate([a, signalin1, b])
DAFx_in1 = DAFx_in1 *1.0/ max(abs(signalin1))
DAFx_in2 = numpy.concatenate([a, signalin2, b])
DAFx_in2 = DAFx_in2 *1.0/ max(abs(signalin2))
DAFx_out = zeros(DAFx_in1.size)
ft = zeros(N, dtype = complex)

pin = 0
pout = 0
pend = min(DAFx_in1.size, DAFx_in2.size) - N

while pin < pend:
	grain1 = DAFx_in1[pin:pin+N]*win
	grain2 = DAFx_in2[pin:pin+N]*win
	f1 = fft(numpy.fft.fftshift(grain1))
	r1 = abs(f1)
	theta1 = angle(f1)
	f2 = fft(numpy.fft.fftshift(grain2))
	r2 = abs(f2)
	theta2 = angle(f2)
	# r and theta can be changed according to the expected effect
	r = r1
	theta = theta2
	ft.real, ft.imag = r*cos(theta), r*sin(theta)
	grain = numpy.fft.fftshift(real(ifft(ft)))*win
	DAFx_out[pout:pout+N] += grain
	pin += n1
	pout += n2

DAFx_out = DAFx_out[N:N+L]*1.0/max(abs(DAFx_out))

wavfile.write('out.wav',fs,array(DAFx_out*signalin1.max(), dtype = 'int16'))

chunk = 1024
wf = wave.open('out.wav', 'rb')
p = pyaudio.PyAudio()
stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)
data = wf.readframes(chunk)
while data != '':
    stream.write(data)
    data = wf.readframes(chunk)

stream.close()
p.terminate()
