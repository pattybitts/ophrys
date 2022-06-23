import util.pixel as pix

#one thing i don't love here is that we're hardcoding the length to the stencil length
class ColorMap():

    def __init__(self, layers):
        self.map = [None for i in range(72)]
        for l in layers:
            self.add_layer(l)

    def add_layer(self, layer):
        notes = []
        for i in range(12):
            notes.append(ColorMap.note_rgu(i, layer['path']))
        for i in range(layer['start'], layer['end']+1):
            note_idx = (i - layer['start']) % len(notes)
            self.map[i] = notes[note_idx]

    #did this become horrific?    
    @staticmethod
    def note_rgu(idx, path):
        lp = path[0]
        for p in path:
            if idx > p[0]: lp = p; continue
            pr = p[1]; pg = p[2]; pu = p[3]
            lpr = lp[1]; lpg = lp[2]; lpu = lp[2]
            if idx == p[0]: return (pr, pg, pu)
            r = (pr - lpr) * (idx - lp[0]) / (p[0] - lp[0]) + lpr
            g = (pg - lpg) * (idx - lp[0]) / (p[0] - lp[0]) + lpg
            u = (pu - lpu) * (idx - lp[0]) / (p[0] - lp[0]) + lpu
            return pix.intify((r, g, u))
        return 255, 255, 255