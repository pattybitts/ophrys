from matplotlib import cm


class Pixel():

    def __init__(self, r, g, u):
        self.r = r
        self.g = g
        self.u = u

    def set_rgu(self, r, g, u):
        self.r = r
        self.g = g
        self.u = u

    def max(self):
        ret = 0
        for c in [self.r, self.g, self.u]:
            if c > ret: ret = c
        return ret

    def brighten(self, m):
        cmax = self.max()
        self.r = (255 - cmax) * m + self.r
        self.g = (255 - cmax) * m + self.g
        self.u = (255 - cmax) * m + self.u
        self.intify()

    def saturate(self, m):
        cmax = self.max()
        if cmax == 0: return
        self.r = self.r * (255 / cmax) ** m
        self.g = self.g * (255 / cmax) ** m
        self.u = self.u * (255 / cmax) ** m
        self.intify()

    def intify(self):
        self.r = int(round(self.r, 0))
        self.g = int(round(self.g, 0))
        self.u = int(round(self.u, 0))