
from obj.Pixel import Pixel

#one thing i don't love here is that we're hardcoding the length to the stencil length
class ColorMap():

    def __init__(self, layers):
        self.map = [Pixel(0, 0, 0) for i in range(72)]
        for l in layers:
            self.add_layer(l)

    def add_layer(self, layer):
        notes = []
        for i in range(12):
            notes.append(ColorMap.note_rgu(i, layer['path']))
        for i in range(layer['start'], layer['end']+1):
            note_idx = (i - layer['start']) % len(notes)
            self.map[i] = notes[note_idx]
        
    @staticmethod
    def note_rgu(idx, path):
        lp = path[0]
        for p in path:
            if idx > p[0]: lp = p; continue
            if idx == p[0]: return Pixel(p[1].r, p[1].g, p[1].u)
            r = (p[1].r - lp[1].r) * (idx - lp[0]) / (p[0] - lp[0]) + lp[1].r
            g = (p[1].g - lp[1].g) * (idx - lp[0]) / (p[0] - lp[0]) + lp[1].g
            u = (p[1].u - lp[1].u) * (idx - lp[0]) / (p[0] - lp[0]) + lp[1].u
            return Pixel(int(round(r, 0)), int(round(g, 0)), int(round(u, 0)))
        return Pixel(255, 255, 255)