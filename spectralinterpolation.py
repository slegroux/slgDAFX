
import numpy
from pylab import *
from scipy.io import wavfile

#----- USER DATA -----

SR,DAFx_in1 = wavfile.read('claire_oubli_voix.WAV')  # sound 1 
SR2,DAFx_in2      = wavfile.read('claire_oubli_flute.WAV') # sound 2

n1            = 512;            # analysis hop size

n2            = n1;             # synthesis hop size

WindowLength  = 2048;           # window length

w1            = hanning(WindowLength); # analysis window

w2            = w1;             # syhnthesis window

cut           = 50              # cut quefrency



#----- initialisations -----

L             = min(len(DAFx_in1), len(DAFx_in2));

DAFx_in1       = numpy.concatenate([zeros(WindowLength),DAFx_in1,zeros(WindowLength-mod(L,n1))])
append(DAFx_in1,1)
DAFx_in1 = DAFx_in1/max(abs(DAFx_in1))                                  


DAFx_in2       = numpy.concatenate([zeros(WindowLength),DAFx_in2,zeros(WindowLength-mod(L,n1))]) 
append(DAFx_in2,1)
DAFx_in2 = DAFx_in2/max(abs(DAFx_in2))

DAFx_out      = zeros(len(DAFx_in1));



#UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU

pin  = 0;

pout = 0;

pend = L - WindowLength;

while pin<pend:

   #----- here is the k factor varies between 0 and 1

   k      = pin/pend;               # spectral mix

   kp     = 1-k;



   grain1 = DAFx_in1[pin:pin+WindowLength]* w1;

   grain2 = DAFx_in2[pin:pin+WindowLength]* w1;

#===========================================

   f1    = fft(fftshift(grain1));

   flog  = log(0.00001+abs(f1));

   cep   = fft(flog);

   cep[1] = cep[1]/2
   cep_coupe  = numpy.concatenate([cep[0:cut],zeros(WindowLength-cut)])

   flog_coupe1 = 2*real(ifft(cep_coupe));

   spec1 = exp(flog_coupe1);        # spectral shape of sound 1

   

   f2    = fft(fftshift(grain2));

   flog  = log(0.00001+abs(f2));

   cep   = fft(flog);

   cep[1] = cep[1]/2
   cep_coupe  = numpy.concatenate([cep[0:cut],zeros(WindowLength-cut)])

   flog_coupe2 = 2*real(ifft(cep_coupe));

   spec2 = exp(flog_coupe2);        # spectral shape of sound 2

   

   #----- here we interpolate the spectral shapes in dBs

   spec  = exp(kp*flog_coupe1+k*flog_coupe2);

   

   ft    = (kp*f1/spec1+k*f2/spec2)*spec;

   grain = fftshift(real(ifft(ft)))*w2;

#===========================================

   DAFx_out[pout:pout+WindowLength] = DAFx_out[pout:pout+WindowLength] + grain;

   pin  = pin + n1;

   pout = pout + n2;



#UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU


#----- listening and saving the output -----



DAFx_out = DAFx_out[WindowLength+1:WindowLength+L] / max(abs(DAFx_out));
DAFx_out = array(DAFx_out * 2**16, dtype = int16)

#soundsc(DAFx_out, SR);

wavfile.write('spec_interp.wav',SR,DAFx_out,)

