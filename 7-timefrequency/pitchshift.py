from scipy import *
from pylab import *
from scipy.io import wavfile
import numpy
import pyaudio
import wave
import sys


execfile('rec.py')

n1 = 512
pit_ratio = 1.2
N = 2048

(fs,signalin) = wavfile.read('query.wav')
win = hanning(N)
L = signalin.size
a = zeros(N)
b = zeros(N - numpy.mod(L, n1))
DAFx_in = numpy.concatenate([a, signalin, b])
DAFx_in = DAFx_in *1.0/ max(abs(signalin))
DAFx_out = zeros(DAFx_in.size)

grain = zeros(N)
hs_win = N/2
omega = 2*pi*n1*arange(0,hs_win)/N
phi0 = zeros(hs_win)
r0 = zeros(hs_win)
psi = phi0
res = zeros(n1)

pin = 0
pout = 0
pend = DAFx_in.size - N

while pin < pend:
	grain =  DAFx_in[pin:pin+N]*win
	fc = fft(numpy.fft.fftshift(grain))
	f = fc[0:hs_win]
	r = abs(f)
	phi = angle(f)
	delta_phi = omega + mod(phi-phi0-omega+pi, -2*pi) + pi
	delta_r = (r-r0)/n1
	delta_psi = pit_ratio*delta_phi/n1
	for k in range(n1):
		r0 = r0 + delta_r
		psi = psi + delta_psi
		res[k] = r0.dot(cos(psi))
	phi0 = phi
	r0 = r
	psi = mod(psi+pi, -2*pi)+pi
	DAFx_out[pout:pout+n1] += res
	pin += n1
	pout += n1

DAFx_out = DAFx_out[hs_win+n1:hs_win+n1+L]*1.0/max(abs(DAFx_out))

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
