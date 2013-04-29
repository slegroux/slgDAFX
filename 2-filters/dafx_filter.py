#
#
#   dafx_filter.py
#
#   module for basic filter structures
#
#
#

from pylab import *

LOWPASS = 1
HIGHPASS = -1
BANDPASS = -1
BANDREJECT = 1

fs = 44100.


def find_c(freq, sampleRate):
    """
    Find the feedback/feedforward coefficient for allpass/comb filters given
    input frequency in hertz
    """
    return (tan(pi * freq / sampleRate) - 1) / (tan(pi * freq / sampleRate) + 1)


def apfilter(x, cutoff, filterType):
    """
    General allpass low/highpass filter implementation

    All variables correspond to similar variables as pgs. 52 - 54
    Figure 2.5 in DAFX
    """

    # find tuning parameter
    c = (tan(pi * cutoff / 2.0) - 1.0) / (tan(pi * cutoff / 2.0) + 1.0)
    # initialize first delayed value -> xh(n - 1)
    xh = 0
    # initialize output
    y = zeros(len(x))

    for index, xn in enumerate(x):
        x_new = xn - c[index] * xh         # x_new -> xh(n) in DAFX
        ap_y = c[index] * x_new + xh
        xh = x_new
        y[index] = 0.5 * (xn + filterType * ap_y)

    return y


def aplowpass(x, cutoff):
    """
    Lowpass filter implementation based off of allpass
    filter implementation.

    x - input signal
    cutoff - cutoff frequency, static or vector (normalized 0 < cutoff < 1, 2 * fc / fs)
    """
    return apfilter(x, cutoff, LOWPASS)


def aphighpass(x, cutoff):
    """
    Lowpass filter implementation based off of allpass
    filter implementation.

    x - input signal
    cutoff - cutoff frequency, static or vector (normalized 0 < cutoff < 1, 2 * fc / fs)
    """
    return apfilter(x, cutoff, HIGHPASS)


def apbandfilter(x, cutoff, bandwidth, filterType):
    """
    General bandpass/bandreject filter implementation
    """
    c = (tan(pi * bandwidth / 2.0) - 1) / (tan(pi * bandwidth / 2.0) + 1)
    d = -cos(pi * cutoff)
    # Initialize
    xh = [0, 0]

    #
    y = zeros(len(x))

    for index, xn in enumerate(x):
        xh_new = xn - d * (1 - c) * xh[0] + c * xh[1]
        ap_y = -c * xh_new + d * (1 - c) * xh[0] + xh[1]
        xh = [xh_new, xh[0]]
        y[index] = 0.5 * (xn + filterType * ap_y)

    return y


def apbandpass(x, cutoff, bandwidth):
    """
    """
    return apbandfilter(x, cutoff, bandwidth, BANDPASS)


def apbandreject(x, cutoff, bandwidth):
    """
    """
    return apbandfilter(x, cutoff, bandwidth, BANDREJECT)


def universal_comb(x, delayAmount, blend, feedforward, feedback):
    """
    General comb filter implementation
    """
    # create delay line
    delayLine = zeros(delayAmount)

    # output
    extra = zeros(len(x))
    y = zeros(len(x) + delayAmount + len(extra))

    # add zeros to x to get tail
    x = concatenate((x, delayLine))
    x = concatenate((x, extra))

    for index, xn in enumerate(x):
        xh = xn + feedback * delayLine[delayAmount - 1]
        y[index] = (feedforward * delayLine[delayAmount - 1]) + (blend * xh)
        # shifting samples within delay line
        delayLine[1:] = delayLine[0:-1]
        delayLine[0] = xh

    return y


def universal_comb_variable(x, delayAmount, widthAmount, blend, feedforward, feedback, breakPoint):
    """
    Universal comb filter with variable lenght delay line + interpolation

    delay amounts are in ms instead of samples

    This implementation allows a breakpoint vector to be specified as well.
    """
    delayLineLength = round(delayAmount * fs)  # convert to number of samples
    width = round(widthAmount * fs)

    if width > delayLineLength:
        print "Breakpoint greater than max delay length"
        return False

    totalLength = round(2 + delayLineLength + width * 2)  # widthLength takees whole range into account
    delayLine = zeros(totalLength)

    y = zeros(len(x))
    a_int = 0

    for index, xn in enumerate(x):
        tap = (delayLineLength + width * breakPoint[index]) - 1
        if tap < 1:
            tap = 1
        elif tap > totalLength:
            tap = totalLength - 1

        integerPortion = floor(tap)
        fractionPortion = tap - integerPortion

        if (integerPortion - 1 > len(delayLine)):
            integerPortion = len(delayLine) - 3

        delayLine = concatenate(([xn], delayLine[0:integerPortion + 1]), axis=0)
        # linear interpolation
        try:
            delayVal = delayLine[integerPortion + 1] * fractionPortion + delayLine[integerPortion] * (1 - fractionPortion)
        except IndexError:
            print "Delay Line Length: ", len(delayLine)
            print "Index: ", integerPortion
        # allpass interpolation
        # delayVal = (delayLine[integerPortion + 1] * (1 - fractionPortion) * delayLine[integerPortion] - (1 - fractionPortion) * a_int)
        # a_int = delayVal
        # normal filtering
        xh = xn + feedback * delayVal
        y[index] = (feedforward * delayVal) + (blend * xh)

    return y


def fir_comb(x, delayAmount, feedforward):
    """
    FIR comb filter implementation
    """
    return universal_comb(x, delayAmount, 1.0, feedforward, 0.0)


def iir_comb(x, delayAmount, blend, feedback):
    """
    IIR comb filter implementation
    """
    return universal_comb(x, delayAmount, blend, 0.0, feedback)


def allpass(x, delayAmount, blend, feedback, feedforward):
    """
    Allpass implementation
    """
    return universal_comb(x, delayAmount, blend, feedforward, feedback)




