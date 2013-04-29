import pyaudio
import os, wave
import numpy as np
import math
import line
import mlpy
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import scipy.signal

execfile('rec.py')

chunk = 2048
fs=4000
freqref = 7.943049790954413
fftsize = 4096

index0=48
index1=95
i = index0
interval = []
while 1:
	freqrange=[]
	freqrange.append(int((2**(1.0/12))**(i-0.5)*freqref/fs*fftsize))
	freqrange.append(int((2**(1.0/12))**(i+0.5)*freqref/fs*fftsize))
	interval.append(freqrange)
	i=i+1
	if i>index1:
		break

def smooth(a):
        for i in range(len(a)-2):
                if (a[i]-a[i+1])>2 and (a[i+2]-a[i+1])>2:
                        a[i+1] = a[i]
                if (a[i+1]-a[i])>2 and (a[i+1]-a[i+2])>2:
                        a[i+1] = a[i]
        return a


def buildstate(fftdata):
	ob = []
	for i in range(len(interval)):
		s = interval[i][0]
		end = interval[i][1]
		window1 = np.hamming(end-s+1)
		v = 0
		for j in range(len(window1)):
			v = v+ window1[j]*fftdata[s+j]
		ob.append(v)
	return ob


def argmax(l):
	if max(l) == min(l):
		return -1
	for i in range(len(l)):
		if l[i] == max(l):
			return i


# target
wf = wave.open('query.wav', 'rb')
swidth = wf.getsampwidth()
RATE = wf.getframerate()
p = pyaudio.PyAudio()
stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
               	channels = wf.getnchannels(),
               	rate = wf.getframerate(),
               	output = True)

window = np.blackman(38)
alldata = wf.readframes(wf.getnframes())
allindata = np.convolve(np.array(wave.struct.unpack("%dh"%(len(alldata)/swidth),alldata)), window)
newdata = scipy.signal.resample(allindata, len(allindata)*fs/44100)

b = []
movesize = 512
ksize = (len(newdata)-chunk)/movesize+1
window = np.hamming(chunk)
for k in range(ksize):
	indata = newdata[k*movesize:(k*movesize+chunk)]*window
	fftData=abs(np.fft.rfft(indata,n=fftsize))**2
	ob = buildstate(fftData)
	b.append(ob)
window = np.hamming(len(newdata)-(k+1)*movesize)
indata = newdata[(k+1)*movesize:len(newdata)]*window
fftData=abs(np.fft.rfft(indata,n=fftsize))
ob = buildstate(fftData)
b.append(ob)

stream.close()
p.terminate()

c = [[] for index in range(len(b))]
tempc = 0
for i in range(len(b)):
	for j in range(12):
		tempc = tempc + b[i][j] + b[i][j+12] + b[i][j+24] + b[i][j+36]
		c[i].append(tempc)
		tempc = 0
	csum = sum(c[i])
	for j in range(12):
		c[i][j] = c[i][j]/csum

for i in range(len(c)):
	if numpy.std(c[i]) < 0.1:
		c[i] = [1.0/12]*12

hist = []
for j in range(12):
	sumh = 0
	for i in range(len(c)):
		sumh = sumh + c[i][j]
	hist.append(sumh)

#keymajor = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]

#keym = []
#for i in range(12):
#	keym.append(numpy.dot(hist,keymajor))
#	keymajor.insert(0,keymajor[11])
#	q = keymajor.pop()

#chromakey = argmax(keym)

#for i in range(chromakey):
#	for j in range(len(c)):
#		c[j].append(c[j][0])
#		c[j].remove(c[j][0])

imshow(c)

# fill out the blank & eliminate the beginning blank part
p=[]
for i in range(len(c)):
	if argmax(c[i]) > -1:
		p.append(argmax(c[i]))
		break

for i in range(len(c)):
	if argmax(c[i]) == -1:
		p.append(p[len(p)-1])
		continue
	p.append(argmax(c[i]))

p = smooth(p)

print p

punique=[]
punique.append(p[0])
time = []
time.append(0)
for i in range(len(p)-1):
	if p[i+1]!=p[i]:
		punique.append(p[i+1])
		time.append(i+1)
f = open("qchroma.txt",'w')
f.writelines(["%s\n" % item for item in p])
f.close()
	
