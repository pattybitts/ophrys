import util.calc as calc

from obj.Pixel import Pixel

class ColorPath():


    def __init__(self, cp_points):
        self.path = []
        for c in cp_points:
            self.add_point(c[0], c[1], c[2], c[3])

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
                max_steps = calc.note_steps(lcp['freq'], cp['freq'])
                steps = calc.note_steps(lcp['freq'], freq)
                r = (p.r - lp.r) * steps / max_steps + lp.r
                g = (p.g - lp.g) * steps / max_steps + lp.g
                u = (p.u - lp.u) * steps / max_steps + lp.u
                return int(round(r, 0)), int(round(g, 0)), int(round(u, 0))
        return 255, 255, 255