def max(rgu):
    ret = 0
    for c in rgu:
        if c > ret: ret = c
    return ret

def min(rgu):
    ret = 255
    for c in rgu:
        if c < ret: ret = c
    return ret

#these should both work with m in range(-1, 1)?
def adjust_brightness(rgu, m):
    new_rgu = []
    for c in rgu:
        mod = c if m <= 0 else 255 - c
        new_rgu.append(mod * m + c)
    return intify((new_rgu[0], new_rgu[1], new_rgu[2]))

def adjust_saturation(rgu, m):
    new_rgu = []
    for c in rgu:
        mod = c if m <= 0 else 255 / c
        new_rgu.append(c * mod ** m)
    return intify((new_rgu[0], new_rgu[1], new_rgu[2]))

def brighten(rgu, m):
    cmax = max(rgu)
    r = (255 - cmax) * m + rgu[0]
    g = (255 - cmax) * m + rgu[1]
    u = (255 - cmax) * m + rgu[2]
    return intify((r, g, u))

def saturate(rgu, m):
    cmax = max(rgu)
    if cmax == 0: return rgu
    r = rgu[0] * (255 / cmax) ** m
    g = rgu[1] * (255 / cmax) ** m
    u = rgu[2] * (255 / cmax) ** m
    return intify((r, g, u))

def intify(rgu):
    return int(round(rgu[0], 0)), int(round(rgu[1], 0)), int(round(rgu[2], 0))