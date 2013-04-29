from scipy import *
from pylab import *
from scipy.io import wavfile
import numpy
import pyaudio
import wave
import sys


execfile('rec.py')

n1 = 400
n2 = n1
N = 1024

(fs,signalin) = wavfile.read('query.wav')
win = arange(0,N)*1.0/N
L = signalin.size
a = zeros(N)
b = zeros(N - numpy.mod(L, n1))
DAFx_in = numpy.concatenate([a, signalin, b])
DAFx_in = DAFx_in *1.0/ max(abs(signalin))
DAFx_out = zeros(DAFx_in.size)

pin = 0
pout = 0
pend = DAFx_in.size - N

while pin < pend:
	grain =  DAFx_in[pin:pin+N]*win
	f = fft(grain)
	r = abs(f)
	grain = numpy.fft.fftshift(real(ifft(r)))*win
	DAFx_out[pout:pout+N] += grain
	pin += n1
	pout += n2

DAFx_out = DAFx_out[N:N+L]*1.0/max(abs(DAFx_out))

wavfile.write('out.wav',fs,array(DAFx_out*signalin.max(), dtype = 'int16'))

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
