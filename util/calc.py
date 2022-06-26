import math, numpy as np

import util.const as const

def distance(x0, y0, x1, y1):
    return math.sqrt((x1-x0)**2+(y1-y0)**2)

def freq(n):
    unit = const.FREQ_INC
    return n * unit + unit / 2

def note_freq(f0, steps):
    return f0 * 2 ** (steps / 12)

def note_steps(f0, f1):
    return 12 * math.log(f1 / f0) / math.log(2)