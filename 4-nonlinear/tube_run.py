
from pylab import *
import numpy as np
import scikits.audiolab
import tube
import scipy.io.wavfile


#x = arange(0, 1, 0.01)
ret = scikits.audiolab.wavread("/Users/shaoduo/Desktop/dsp_presentation/eg.wav")
#ret = scipy.io.wavfile.read("/Users/shaoduo/Desktop/dsp_presentation/eg.wav")
x = ret[1]

subplot(3, 1, 1)
plot(x)
for i in range(0, len(x)):
	x[i] = x[i] / 2**15
y = tube.tube(x, 3.0, 1.0, 150.0, 0.8, 0.8, 0.6)
#y = tube.symclip(x)
#y = tube.expdist(x, 10.0, 0.8)

scikits.audiolab.wavwrite(y, "/Users/shaoduo/Desktop/dsp_presentation/eg-d.wav", fs=44100, enc='pcm16')
#scipy.io.wavfile.write("/Users/shaoduo/Desktop/dsp_presentation/eg-d.wav", 44100, y)
subplot(3, 1, 2)
plot(y)

xy = abs(x) - abs(y)
subplot(3, 1, 3)
plot(xy)
show()