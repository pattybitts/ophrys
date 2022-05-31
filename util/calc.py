import math, numpy as np

import util.const as const

def distance(x0, y0, x1, y1):
    return math.sqrt((x1-x0)**2+(y1-y0)**2)

def freq(n):
    unit = const.FREQ_INC
    return n * unit + unit / 2

#i should figure out how i want to structure returns on this
def com(list, start=0.0, inc=1.0):
    numerator = 0
    denominator = np.sum(list)
    if denominator == 0: return 0
    for idx, l in np.ndenumerate(list):
        numerator += l * (start + idx[0] * inc)
    return numerator / denominator

#homemade, measure of sharpeness by finding percentage of mass
def spike_score(list, window=.2):
    mass = np.sum(list)
    if mass == 0: return 0
    center = com(list)
    spike = 0
    width = len(list) - 1
    for idx, x in np.ndenumerate(list):
        if idx[0] >= center - width * window * .5 and idx[0] <= center + width * window * .5:
            spike += x
    return spike / mass
