import util.calc as calc

from obj.Pixel import Pixel

class ColorPath():


    def __init__(self):
        self.path = []

    def add_point(self, freq, r, g, u):
        self.path.append({'freq': freq, 'pix': Pixel(r, g, u)})

    def freq_rgu(self, freq):
        len_points = len(self.path)
        for i in range(len_points):
            cp = self.path[i]
            if freq < cp['freq']:
                p = cp['pix']
                if i == 0: return p.r, p.g, p.u
                lcp = self.path[i-1]
                lp = lcp['pix']
                steps = calc.note_steps(lcp['freq'], freq)
                r = (p.r - lp.r) * steps / 12 + lp.r
                g = (p.g - lp.g) * steps / 12 + lp.g
                u = (p.u - lp.u) * steps / 12 + lp.u
                return int(round(r, 0)), int(round(g, 0)), int(round(u, 0))
        return 255, 255, 255