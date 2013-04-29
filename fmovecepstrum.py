
# UX_fmove_cepstrum.m

import numpy
from pylab import *
from scipy.io import wavfile
#----- USER DATA -----
SR,DAFx_in = wavfile.read("/Users/fanziwen/Desktop/dafxchapnine/moore_guitar.wav") #sound file
warping_coef  = 2
n1            = 512            # analysis hop size
n2            = n1             # synthesis hop size
WindowLength  = 2048           # window length
w1            = hanning(WindowLength) # analysis window
w2            = w1             # syhnthesis window
ordre1         = 50             # cut quefrency

#----- initialisations -----
WindowLength2 = WindowLength/2;
L             = len(DAFx_in);
DAFx_in       = numpy.concatenate([zeros(WindowLength), DAFx_in, zeros(WindowLength-mod(L,n1))])
append(DAFx_in,1)
DAFx_in = DAFx_in/max(abs(DAFx_in))      
DAFx_out      = zeros(L)
t             = 1 + floor(arange(0,WindowLength)*warping_coef) # apply the warping
lmax          = max(WindowLength,t[WindowLength-1])


#UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU
pin  = 0
pout = 0
pend = L - WindowLength;
while pin<pend:
   grain  = DAFx_in[pin:pin+WindowLength]* w1
#===========================================
   f      = fft(grain)/WindowLength2     # spectrum of grain
   flogs  = 20*log10(0.00001+abs(f))     # log|X(k)|

   grain1 = DAFx_in[arange(0,WindowLength*warping_coef,warping_coef)]* w1           # linear interpolation of grain
   f1     = fft(grain1)/WindowLength2    # spectrum of interpolated grain
   flogs1 = 20*log10(0.00001 + abs(f1))  # log|X1(k)|
   flog   = log(0.00001+abs(f1)) - log(0.00001+abs(f))
   cep    = ifft(flog)                   # cepstrum
   cep[1] = cep[1]/2
   cep_coupe  = numpy.concatenate([cep[0:ordre1],zeros(WindowLength-ordre1)])
   append(cep_coupe,1)  

   corr   = exp(2*real(fft(cep_coupe)))  # spectral shape
   grain  = (real(ifft(f*corr)))*w2

   fout   = fft(grain)
   flogs2 = 20*log10(0.00001+abs(fout))

   #----- figures for real-time spectral shape up to FS/2 -----
   subplot(3,1,1)
   plot(arange(1,WindowLength2/2)*44100/WindowLength, flogs[1:WindowLength2/2])
   title('a) original spectrum')
   #drawnow;
   subplot(3,1,2)
   plot(arange(1,WindowLength2/2)*44100/WindowLength, flogs1[1:WindowLength2/2])
   title('b) spectrum of time-scaled signal')
   subplot(3,1,3)
   plot(arange(1,WindowLength2/2)*44100/WindowLength, flogs2[1:WindowLength2/2])
   title('c) formant changed spectrum')
   xlabel('f in Hz \rightarrow')
   #drawnow

# ===========================================
   DAFx_out[pout:pout+WindowLength] = DAFx_out[pout:pout+WindowLength] + grain
   pin  = pin + n1
   pout = pout + n2
#UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU


#----- listening and saving the output -----
#soundsc(DAFx_out, SR);
DAFx_out_norm = .99* DAFx_out/max(abs(DAFx_out)) # scale for wav output
print len(DAFx_out_norm)
print max(abs(DAFx_out_norm))
show()
DAFx_out_norm = array(DAFx_out_norm * 2**16, dtype = int16)
print len(DAFx_out_norm)
print max(abs(DAFx_out_norm))
wavfile.write('la_fmov11e.wav',SR,DAFx_out_norm)
