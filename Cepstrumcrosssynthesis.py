import numpy
from pylab import *
from scipy.io import wavfile




#----- USER DATA -----

SR,DAFx_in1 = wavfile.read("/Users/fanziwen/Desktop/dafxchapnine/moore_guitar.wav") #sound 1: excitation
SR2,DAFx_in2 = wavfile.read("/Users/fanziwen/Desktop/dafxchapnine/toms_diner.wav") #sound 2: spectral env.
WindowLength   = 1024            # window size
n1             = 256             # hop size
ordre1         = 30              # cut quefrency for sound 1
ordre2         = 30              # cut quefrency for sound 2


#----- initialisations -----
w1             = hanning(WindowLength) #analysis window
w2             = w1              #synthesis window
WindowLength2  = WindowLength/2
grain1         = zeros(WindowLength)
grain2         = zeros(WindowLength)
pin            = 0               # start index
L              = min(len(DAFx_in1),len(DAFx_in2))
pend           = L - WindowLength # end index
DAFx_in1       = numpy.concatenate([zeros(WindowLength),DAFx_in1,zeros(WindowLength-mod(L,n1))])
append(DAFx_in1,1)
DAFx_in1 = DAFx_in1/max(abs(DAFx_in1))                                  


DAFx_in2       = numpy.concatenate([zeros(WindowLength),DAFx_in2,zeros(WindowLength-mod(L,n1))]) 
append(DAFx_in2,1)
DAFx_in2 = DAFx_in2/max(abs(DAFx_in2))

DAFx_out       = zeros(L)

#----- cross synthesis -----
while pin<pend:
   grain1     = DAFx_in1[pin:pin+WindowLength]* w1
   grain2     = DAFx_in2[pin:pin+WindowLength]* w1
#===========================================
   f1         = fft(grain1)

   f          = fft(grain2)/WindowLength2
   flog       = log(0.00001+abs(f))
   cep        = ifft(flog)                 # cepstrum of sound 2
   cep[1] = cep[1]/2
   cep_coupe  = numpy.concatenate([cep[0:ordre1],zeros(WindowLength-ordre1)])
   append(cep_coupe,1)                               
   flog_coupe = 2*real(fft(cep_coupe))
   f2         = exp(flog_coupe)            # spectral shape of sound 2
   len(f1)
   grain      = (real(ifft(f1*f2)))*w2   # resynthesis grain
# ===========================================
   DAFx_out[pin:pin+WindowLength] = DAFx_out[pin:pin+WindowLength] + grain
   pin        = pin + n1
#end

#----- listening and saving the output -----

#DAFx_out = DAFx_out[WindowLength:len(DAFx_out)] / max(abs(DAFx_out))
DAFx_out = DAFx_out[0:len(DAFx_out)] / float(max(abs(DAFx_out)))
print len(DAFx_out)
print max(abs(DAFx_out))
#soundsc(DAFx_out, SR)
DAFx_out_norm = .99* DAFx_out/max(abs(DAFx_out)) #scale for wav output
print len(DAFx_out_norm)
print max(abs(DAFx_out_norm))
plot(real(fft(DAFx_out_norm))[0:len(DAFx_out_norm)/2])
axis([0,10000,0,1500])
show()

DAFx_out_norm = array(DAFx_out_norm * 2**16, dtype = int16)
wavfile.write("/Users/fanziwen/Desktop/dafxchapnine/1111.wav",SR,DAFx_out_norm)
woca,canimei = wavfile.read("/Users/fanziwen/Desktop/dafxchapnine/CrossCepstrum.wav")
print(max(abs(DAFx_out_norm)))
'''x = arange(0,1024)
x = x*44100/1024
print(len(x))
print(len(real(fft(DAFx_out_norm,1024))))'''

#fs,dafxin
#dafxin = float32(dafxin/float(2**16))
#dafxout = array(dafxout * 2**16, dtype = int16)
#wavefilewrite()
