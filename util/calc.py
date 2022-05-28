import math 

def distance(x0, y0, x1, y1):
    return math.sqrt((x1-x0)**2+(y1-y0)**2)

def freq(n):
    unit = 22050 / 8192
    return n * unit + unit / 2