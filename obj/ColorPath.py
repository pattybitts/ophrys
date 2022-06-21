import util.calc as calc

#TODO This need a big refactoring pass if i decide to pick it up again
class ColorPath():

    def __init__(self, cp_points):
        self.path = []
        for c in cp_points:
            self.add_point(c[0], c[1], c[2], c[3])

    def add_point(self, freq, r, g, u):
        self.path.append({'freq': freq, 'pix': (r, g, u)})

    def freq_rgu(self, freq):
        len_points = len(self.path)
        for i in range(len_points):
            cp = self.path[i]
            if freq < cp['freq']:
                p = cp['pix']
                if i == 0: return p.r, p.g, p.u
                lcp = self.path[i-1]
                lp = lcp['pix']
                max_steps = calc.note_steps(lcp['freq'], cp['freq'])
                steps = calc.note_steps(lcp['freq'], freq)
                r = (p.r - lp.r) * steps / max_steps + lp.r
                g = (p.g - lp.g) * steps / max_steps + lp.g
                u = (p.u - lp.u) * steps / max_steps + lp.u
                return int(round(r, 0)), int(round(g, 0)), int(round(u, 0))
        return 255, 255, 255


'''
This is how I was initializing the color paths in soul_v2
cp0_points = [
    [calc.note_freq(55, 3), 4, 28, 134],
    [calc.note_freq(110, 3), 85, 100, 170],
    [calc.note_freq(220, 3), 145, 146, 191],
    [calc.note_freq(440, 2), 114, 204, 244]
]
cp1_points = [
    [calc.note_freq(440, 3), 249, 160, 6],
    [calc.note_freq(880, 3), 240, 233, 57],
    [calc.note_freq(1760, 3), 255, 255, 255]
]
cp0 = ColorPath(cp0_points)
cp1 = ColorPath(cp1_points)
'''