from numpy import *
from pylab import *
import scipy
from scipy import signal
from scipy.io import wavfile

""" PARTS SHOULD BE RAN ONE BY ONE """

input = scipy.io.wavfile.read('/Users/gregoiretronel/Documents/Eclipse/workspace/DSP_class/src/presentation/Trumpt44.wav')
FS = input[0]
x = input[1]
y = zeros(len(x),int16)


"""_________________________________________________________
SHELVING FILTER
_________________________________________________________"""

""" 1st order LF Shelving"""
G  = -12.0
fc = 1000
Wc = 2.0*fc/FS
V0 = pow(10,G/20.0) 
H0 = V0 - 1.0

if G >= 0:
    c = (tan(pi*Wc/2.0)-1.0) / (tan(pi*Wc/2.0)+1.0)  # boost
else:
    c = (tan(pi*Wc/2.0)-V0) / (tan(pi*Wc/2.0)+V0)  # cut

xh = 0
for n in range(len(x)):
    xh_new = x[n] - c*xh
    ap_y = c * xh_new + xh
    xh  = xh_new
    y[n] = 0.5*H0*(x[n]+ap_y)+x[n] 
    """ change above to minus for HS """

#b = [c, V0]
#a = [-1, c*V0]
#w, h = scipy.signal.freqz(b, a)
#subplot(2,1,1)
#plot(w/max(w), abs(h))
#title('Frequency Response')
#xlabel('Normalized radian frequency')
#subplot(2,1,2)
#plot(w/max(w), angle(h))
#xlabel('Normalized phase')
#show()

""" Plot Signal """ 
subplot(2,2,1)
title('ORIGINAL')
plot(x)
subplot(2,2,2)
title('FILTERED')
plot(y)

""" Plot FFT """
xfft = fft(x,FS)
xfft = xfft[0:int(round(len(xfft)/2))]
yfft = fft(y,FS)
yfft = yfft[0:int(round(len(yfft)/2))]
subplot(2,2,3)
semilogx(abs(xfft))  
subplot(2,2,4)
semilogx(abs(yfft))

show()  

""" write to file """
scipy.io.wavfile.write('/Users/gregoiretronel/Documents/Eclipse/workspace/DSP_class/src/presentation/Trumpt44_shelv.wav',FS,y)


""" __________________
    2nd ORDER SHELVING 
    __________________ """
""" HF Cut example """
G  = -12.0
fc = 700.0
Wc = 2.0*fc/FS
V0 = pow(10,G/20.0) 

K = tan(pi*Wc/2)

b0 = V0*(1 + sqrt(2)*K + pow(K,2))/(1 + sqrt(2*V0)*K + V0*pow(K,2))
b1 = 2*V0*(pow(K,2) - 1)/(1 + sqrt(2*V0)*K + V0*pow(K,2))
b2 = V0*(1 - sqrt(2)*K + pow(K,2))/(1 + sqrt(2*V0)*K + V0*pow(K,2))
a1 = 2*(V0*pow(K,2) - 1)/(1 + sqrt(2*V0)*K + V0*pow(K,2))
a2 = (1 - sqrt(2*V0)*K + V0*pow(K,2))/(1 + sqrt(2*V0)*K + V0*pow(K,2))

b = [b0, b1, b2]
a = [a1, a2]
w, h = scipy.signal.freqz(b, a)
subplot(2,1,1)
plot(w/max(w), abs(h))
xlabel('Normalized Radian Frequency')
subplot(2,1,2)
plot(w/max(w), angle(h))
xlabel('Normalized phase')
show()


""" HF Boost example """
G  = 12.0
fc = 10000.0
Wc = 2.0*fc/FS
V0 = pow(10,G/20.0) 

K = tan(pi*Wc/2)

b0 = (V0 + sqrt(2*V0)*K + pow(K,2))/(1 + sqrt(2)*K + pow(K,2))
b1 = 2*(pow(K,2) - V0)/(1 + sqrt(2)*K + pow(K,2))
b2 = (V0 - sqrt(2*V0)*K + pow(K,2))/(1 + sqrt(2)*K + pow(K,2))
a1 = 2*(pow(K,2) - 1)/(1 + sqrt(2)*K + pow(K,2))
a2 = (1 - sqrt(2)*K + pow(K,2))/(1 + sqrt(2)*K + pow(K,2))

b = [b0, b1, b2]
a = [a1, a2]
w, h = scipy.signal.freqz(b, a)
subplot(2,1,1)
plot(w/max(w), abs(h))
title('Frequency Response')
xlabel('Normalized radian frequency')
subplot(2,1,2)
plot(w/max(w), angle(h))
xlabel('Normalized phase')
show()




"""_________________________________________________________
PEAK FILTER
_________________________________________________________"""
G  = -12
fc = 465.0
Wc = 2.0*fc/FS
fb = 50.0
Wb = 2.0*fb/FS

V0 = pow(10,G/20.0)
H0 = V0 - 1.0 

if G >= 0:
    c = (tan(pi*Wb/2)-1) / (tan(pi*Wb/2)+1) # boost
else:
    c = (tan(pi*Wb/2)-V0) / (tan(pi*Wb/2)+V0) # cut
    
d = -cos(pi*Wc)
xh = [0, 0]
for n in range(len(x)):
    xh_new = x[n] - d*(1-c)*xh[0] + c*xh[1]
    ap_y = -c * xh_new + d*(1-c)*xh[0] + xh[1]
    xh = [xh_new, xh[0]]
    y[n] = 0.5 * H0 * (x[n] - ap_y) + x[n]


""" Plot """ 
subplot(3,2,3)
plot(x)
subplot(3,2,4)
plot(y)

""" Plot fft """
xfft = fft(x,FS)
xfft = xfft[0:int(round(len(xfft)/2))]
yfft = fft(y,FS)
yfft = yfft[0:int(round(len(yfft)/2))]
subplot(3,2,1)
title('ORIGINAL')
semilogx(abs(xfft))
subplot(3,2,2)
title('FILTERED')
semilogx(abs(yfft))  

show()   

""" WRITE to file """
scipy.io.wavfile.write('/Users/gregoiretronel/Documents/Eclipse/workspace/DSP_class/src/presentation/Trumpt44_peak.wav',FS,y)

""" Coefficients """
G  = 0
fc = 1000.0
fb = 500.0
Wc = 2.0*fc/FS
K  = tan(pi*Wc/2)
V0 = pow(10,G/20)
Q  = fb/fc
# BOOST:
b0 = (1+V0*K/Q+pow(K,2))/(1+K/Q+pow(K,2))
b1 = 2*(pow(K,2)-1)/(1+K/Q+pow(K,2))
b2 = (1-V0*K/Q+pow(K,2))/(1+K/Q+pow(K,2))
a1 = 2*(pow(K,2)-1)/(1+K/Q+pow(K,2))
a2 = (1-K/Q+pow(K,2))/(1+K/Q+pow(K,2))
# Cut:
b0 = (1+K/Q+pow(K,2))/(1+K/(V0*Q)+pow(K,2))
b1 = 2*(pow(K,2)-1)/(1+K/(V0*Q)+pow(K,2))
b2 = (1-K/Q+pow(K,2))/(1+K/(V0*Q)+pow(K,2))
a1 = 2*(pow(K,2)-1)/(1+K/(V0*Q)+pow(K,2))
a2 = (1-K/(V0*Q)+pow(K,2))/(1+K/(V0*Q)+pow(K,2))

b = [b0, b1, b2]
a = [a1, a2]
w, h = scipy.signal.freqz(b, a)
plot(w/max(w), abs(h))
xlabel('Normalized frequency')
show()

"""_________________________________________________________
VIBRATO
_________________________________________________________"""

# function y = vibrato(x, fs, Modfreq, Width)

Modfreq = 7.0 # modulation frequency in Hz
Width   = .01  #modulation width (delay time) in sec

Delay=Width

DELAY=round(Delay*FS)
WIDTH=round(Width*FS)

MODFreq=Modfreq/FS
LEN=len(x)
L=int(2+DELAY+WIDTH*2)
Delayline=zeros(L)
y=zeros(len(x),int16)

for n in range(LEN-1):
    print n
    MOD=sin(MODFreq*2*pi*n)
    TAP=1+DELAY+WIDTH*MOD
    i=int(floor(TAP))-1
    frac=TAP-i
    Delayline = concatenate(([x[n]],Delayline[0:L-1]),axis=0)
    #---Linear Interpolation-----------------------------
    y[n] = Delayline[i+1]*frac+Delayline[i]*(1-frac)

""" WRITE to file """
scipy.io.wavfile.write('/Users/gregoiretronel/Documents/Eclipse/workspace/DSP_class/src/presentation/Trumpt44_vibrato_7hz_.01s.wav',FS,y)

""" Plot """ 
subplot(3,2,1)
title('ORIGINAL')
plot(x)
subplot(3,2,2)
title('FILTERED')
plot(y)

xfft = fft(x,FS)
xfft = xfft[0:int(round(len(xfft)/2))]
yfft = fft(y,FS)
yfft = yfft[0:int(round(len(yfft)/2))]
subplot(3,2,3)
title('ORIGINAL')
semilogx(abs(xfft))  
subplot(3,2,4)
title('FILTERED')
semilogx(abs(yfft))  

""" Plot spectrogram """
subplot(3,2,5)
sgramX = specgram(x)
subplot(3,2,6)
sgramY = specgram(y)

show()   