from pylab import *
from scipy import signal

def ws_compexp(x, CT, CS, ET, ES):
#in2: thresh hold for compressor in dB
#in3: ratio for compressor in log, 0 => ratio of 1, 1 => ratio of +inf
#in4: thresh hold for expander in dB
#in5: ratio for expander in log, 0 => ratio of 1, -inf => ratio of +inf
	tav = 0.01;
	at = 0.03;
	rt = 0.003;
	delay = 150;
	xrms = 0;
	g = 1;
	buff = zeros(delay);
	y = zeros(len(x));
	for n in range(len(x)):
	    xrms = (1-tav) * xrms + tav * x[n]**2; 
	    if xrms == 0:
	    	X = 0;
	    else:
	    	X = 10*log10(xrms);
	    G = min([0, CS*(CT-X), ES*(ET-X)]); 
	    f = 10**(G/20);
	    if f < g:
	        coeff = at;
	    else:
	        coeff = rt;
	    g = (1-coeff) * g + coeff * f; 
	    y[n] = g * buff[-1];

	    for i in range(1,len(buff)):
	    	buff[i] = buff[i-1];
		buff[0] = x[n];
	return y;
	



def ws_limiter(x, lt):
# in2: threshold in magnitude, between 1 and 0.
	at = 0.3;
	rt = 0.01;
	delay = 5;
	xpeak = 0;
	g = 1;
	buff = zeros(delay);
	y = zeros(len(x));
	for n in range(len(x)):
	  	a = abs(x[n]);
	 	if a > xpeak:
	   		coeff = at;
	  	else:
	  		coeff = rt;
	  	xpeak = (1-coeff) * xpeak + coeff * a; 
	  	if(xpeak == 0):
	  		f = 0;
	  	else:
	  		f = min([1, lt/xpeak]);
	  	if f < g:
	  		coeff = at;
	  	else:
	  		coeff = rt;
	  	g = (1-coeff) * g + coeff * f; 
	  	y[n] = g * buff[-1];
	  	for i in range(1,len(buff)):
			buff[i] = buff[i-1];
		buff[0] = x[n];
	return y;


def ws_noisegt(x,holdtime,ltrhold,utrhold,release,attack,a,Fs):
# function y=noisegt(x,holdtime,ltrhold,utrhold,release,attack,a,Fs) %
# Author: R. Bendiksen
# noise gate with hysteresis
# holdtime - time in seconds the sound level has to be below the threshhold value before the gate is activated
# ltrhold - threshold value for activating the gate
# utrhold - threshold value for deactivating the gate > ltrhold 
# release - time in seconds before the sound level reaches zero 
# attack - time inseconds before the output sound level is the same as the input level
#           after deactivating the gate
# a  - pole placement of the envelope detecting filter <1
# Fs - sampling frequency
	rel=round(release*Fs); #number of samples for fade 
	att=round(attack*Fs); #number of samples for fade 
	g=zeros(len(x));
	lthcnt=0;
	uthcnt=0;
	ht=round(holdtime*Fs);
	h=signal.lfilter([(1-a)**2],[1.0000,-2*a,a**2],abs(x));#envelope detection 
	h=h/max(h);
	for i in range(len(h)):
	    if (h[i]<=ltrhold) or ((h[i]<utrhold) and (lthcnt>0)):
	    # Value below the lower threshold?
	        lthcnt=lthcnt+1;
	        uthcnt=0;
	        if lthcnt>ht:
	            # Time below the lower threshold longer than the hold time? 
	            if lthcnt>(rel+ht):
	                g[i]=0; 
	            else:
	                g[i]=1-(lthcnt-ht)/rel; # fades the signal to zero
	        elif ((i<ht) and (lthcnt==i)):
	            g[i]=0;
	        else:
	            g[i]=1;
	    elif (h[i]>=utrhold) or ((h[i]>ltrhold) and (uthcnt>0)):
	        # Value above the upper threshold or is the signal being faded in? 
	        uthcnt=uthcnt+1;
	        if (g[i-1]<1):
	        # Has the gate been activated or isnt the signal faded in yet?
	        	g[i] = max([uthcnt/att,g[i-1]]);
	        else:
	            g[i]=1;
	        lthcnt=0;
	    else:
	        g[i]=g[i-1];
	        lthcnt=0;
	        uthcnt=0;
	y=x*g;
	y=y*max(abs(x))/max(abs(y));
	return y;
