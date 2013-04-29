

from pylab import *
import numpy as np
from scipy.signal import lfilter


def tube(x, gain, Q, dist, rh, rl, mix):
	q = x * gain / max(abs(x))
	if Q == 0:
		z = q / (1 - exp(-1 * dist *q))
		for i in range(0, len(q)):
			if q[i] == Q:
				z[i] = 1 / dist
	else:
		z = (q - Q) / (1 - exp(-1 * dist * (q-Q))) + Q / (1 - exp(dist * Q))
		#z = zeros(len(q))
		#for i in range(0, len(q)):
		#	z[i] = (q[i] - Q) / (1 - exp(-1 * dist * (q[i] - Q))) + Q / (1 - exp(dist * Q))
		for i in range(0, len(q)):
			if q[i] == Q:
				z[i] = 1 / dist + Q / (1 - exp(dist * Q))

	y = mix * z * max(abs(x)) / max(abs(z)) + (1 - mix) * x
	y = y * max(abs(x)) / max(abs(y))
	y = lfilter([1, -2, 1], [1, -2 * rh, rh * rh], y)
	y = lfilter([1 - rl], [1, -1*rl], y)

	y = y / max(abs(y))
	return y


def symclip(x):
	N = len(x)
	th = 1 / 3.
	y = zeros(N)

	for i in range(0, N):
		if abs(x[i] < th):
			y[i] = 2 * x[i]
		if abs(x[i]) >= th:
			if x[i] > 0:
				y[i] = (3 - (2 - x[i] * 3)**2) / 3.0
			if x[i] < 0:
				y[i] = -1 * (3 - (2 - abs(x[i]) * 3)**2) / 3.0

		if abs(x[i]) > 2 * th:
			if x[i] > 0:
				y[i] = 1
			if x[i] < 0:
				y[i] = -1

	y = y / max(abs(y))
	return y

def expdist(x, gain, mix):
	q = x * gain
	z = np.sign(q) * (1 - exp(-1 * abs(q)))
	y = mix * z + (1 - mix) * x

	y = y / max(abs(y))
	return y

# def sign(x):
# 	for i in range(0, len(x)):
# 		if x[i] < 0:
# 			x[i] = -1.0
# 		elif x[i] == 0:
# 			x[i] = 0.0
# 		else:
# 			x[i] = 1.0
# 	return
