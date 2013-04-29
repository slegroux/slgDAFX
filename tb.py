from fx import *


fs = 44100;
t = arange(0.0,1.0,1.0/fs);
signal = sin(2 * pi * 2 * t);

#talk about in2 = 0.3 and 0.7
#explain why not hard cut but using two one-pole filters to obtain the magnitude.
#y = ws_limiter(signal,0.7);

#def ws_noisegt(x,holdtime,ltrhold,utrhold,release,attack,a,Fs):
# noise gate with hysteresis
# holdtime - time in seconds the sound level has to be below the threshhold value before the gate is activated
# ltrhold - threshold value for activating the gate
# utrhold - threshold value for deactivating the gate > ltrhold 
# release - time in seconds before the sound level reaches zero 
# attack - time inseconds before the output sound level is the same as the input level
#           after deactivating the gate
# a  - pole placement of the envelope detecting filter <1
# Fs - sampling frequency

#y = ws_noisegt(signal,0.02,0.5,0.6,0.01,0.01,0.9,44100); #noise gate. The little tip at the begining is because it is under hold time.
#y = ws_noisegt(signal,0.02,0.5,0.6,0.01,0.1,0.9,44100); #noise gate with longer atack time
#y = ws_noisegt(signal,0.02,0.5,0.6,0.1,0.01,0.9,44100); #noise gate with longer release time
#y = ws_noisegt(signal,0.08,0.5,0.6,0.01,0.01,0.9,44100); #noise gate with longer hold time


##y = ws_compexp(signal, -3., 1, -10.,0.);#expander off, limiter
#y = ws_compexp(signal, -3., 0.5, -10.,0.);#expander off, compressor
#y = ws_compexp(signal, -3., 0, -6.,-inf);#extreme noise gate, compressor off
#y = ws_compexp(signal, -3., 0, -2.,-1);#expander to make a vivid sound, compressor off


subplot(2,1,1);
plot(signal);
title('input')
subplot(2,1,2);
plot(y);
title('output')
show();