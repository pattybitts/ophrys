import math, numpy as np

import util.const as const

def distance(x0, y0, x1, y1):
    return math.sqrt((x1-x0)**2+(y1-y0)**2)

def freq(n):
    unit = const.FREQ_INC
    return n * unit + unit / 2

#at this point these functions really aren't fit for a universal calc module
#let's find a home for them

def bin_peak(points):
    max = 0
    for p in points:
        if p[1] > max: max = p[1]
    return max

def bin_mass(points, threshold=None):
    count = 0
    mass = 0
    for p in points:
        if threshold and p[1] < threshold: continue
        count += 1
        mass += p[1]
    if count > 0: return mass / count
    return mass

#i should figure out how i want to structure returns on this
#adjusting this to take a list of tuples in the form of (x, m)
def bin_com(points):
    numerator = 0
    denominator = 0
    for p in points:
        numerator += p[0] * p[1]
        denominator += p[1]
    if denominator == 0: return 0
    return numerator / denominator

#returns the width in hz at which the mass of the spike reaches the given percentage of the bin's mass
def spike_score(points, mass, center, mass_th=.5):
    if mass == 0: return 0
    center_idx = 0
    for p in points:
        if abs(p[0] - center) <= const.FREQ_INC / 2: center_idx = points.index(p)
    spike_mass = points[center_idx][1]
    r = 1
    while spike_mass / mass < mass_th:
        rl = center_idx - r
        rh = center_idx + r
        if rl >= 0: spike_mass += points[rl][1]
        if rh < len(points): spike_mass += points[rh][1]
        r += 1
    return mass_th * r * 2 * const.FREQ_INC / (spike_mass / mass)

def note_freq(f0, steps):
    return f0 * 2 ** (steps / 12)

def note_steps(f0, f1):
    return 12 * math.log(f1 / f0) / math.log(2)