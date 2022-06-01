import math, numpy as np

import util.const as const

def distance(x0, y0, x1, y1):
    return math.sqrt((x1-x0)**2+(y1-y0)**2)

def freq(n):
    unit = const.FREQ_INC
    return n * unit + unit / 2

#at this point these functions really aren't fit for a universal calc module
#let's find a home for them

def bin_mass(points, average=False):
    mass = 0
    for p in points:
        mass += p[1]
    if average: return mass / len(points)
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

def spike_score(points, pct_radius=.2):
    mass = bin_mass(points)
    if mass == 0: return 0
    center = bin_com(points)
    width = points[-1][0] - points[0][0]
    spike = 0
    for p in points:
        if p[0] >= center - pct_radius * width and p[0] <= center + pct_radius * width: spike += p[1]
    return spike / mass