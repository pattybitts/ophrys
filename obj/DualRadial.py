import math

import util.const as const

from obj.PixelArray import PixelArray

class DualRadial():

    def __init__(self, parr, c1x, c1y, r1, c2x, c2y, r2):
        self.parr = parr
        self.c1x = c1x
        self.c1y = c1y
        self.r1 = r1
        self.c2x = c2x
        self.c2y = c2y
        self.r2 = r2

    def draw_canvas(self, profile):
        theta = 0
        while theta <= 2 * math.pi:
            self.draw_line(theta, profile)
            theta += const.DR_ST

    def draw_line(self, theta, profile):
        #don't forget rounding to our pixel resolution!
        #this will definitely get more complex as we go
        x0 = self.c2x - self.r2 * math.sin(theta)
        y0 = self.c2y - self.r2 * math.cos(theta)
        x1 = self.c1x - self.r1 * math.sin(theta)
        y1 = self.c1y - self.r1 * math.cos(theta)
        m = (y1 - y0) / (x1 - x0)
        pl = len(profile)
        dx = (x1 - x0) / pl / const.DX_ST
        for p in reversed(profile):
            for i in range(const.DX_ST):
                x = int(x0 + dx * i)
                y = int(y0 + m * dx * i)
                if x > self.parr.x or x < 0 or y > self.parr.y or y < 0: continue
                #color setting will need to be standardized and implemented through our color filter
                #this is next, I think. before importing a sound profile
                r = int(100)
                g = int(100)
                u = int(100 + 155 * p[0])
                #this paradigm will be useful to remember once I get into color filtering
                self.parr.setp(x, y, r, g, u)
            x0 = x0 + dx * const.DX_ST
            y0 = y0 + m * dx * const.DX_ST

    def color_filter(self, point):
        pass
