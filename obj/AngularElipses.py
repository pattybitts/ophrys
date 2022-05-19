import math
import numpy as np

import util.calc as calc
import util.const as const
import util.util as util

from obj.PixelArray import PixelArray

class AngularElipses():

    def __init__(self, parr, x0, y0, x1, y1, k_shift):
        self.parr = parr
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.k = calc.distance(x0, y0, x1, y1) + k_shift

    def draw_elipse(self, x1, y1, r, g, u):
        xc = (self.x0 + x1) / 2
        yc = (self.y0 + y1) / 2
        for i in range(2):
            theta = 0
            direction = 1 if i == 0 else -1
            while theta < math.pi:
                m = math.tan(theta)
                dt = self.k / const.ELP * direction
                x = xc; xp = xc; xpp = None
                y = yc; yp = yc; ypp = None
                for j in range(const.ELP):
                    d0 = calc.distance(self.x0, self.y0, x, y)
                    d1 = calc.distance(x1, y1, x, y)
                    if d0 + d1 >= self.k - const.EW / 2 and d0 + d1 <= self.k + const.EW / 2:
                        xp = int(round(x, 0))
                        yp = int(round(y, 0))
                        if xp != xpp or yp != ypp:
                            if xp <= self.parr.x and xp >= 0 and yp <= self.parr.y and yp >= 0:
                                self.parr.setp(xp, yp, r, g, u)
                                xpp = xp; ypp = yp
                                break
                    if d0 + d1 > self.k + const.EW / 2: break
                    if abs(m) >= 1:
                        y += dt
                        x += dt / m
                    else:
                        x += dt
                        y += dt * m
                theta += const.EDR

    #under this design paradigm all the 'artistic' tuning will occur here
    #we scale t to 1 so that we can normalize these equations to the canvas
    def par_x(self, t):
        return (self.x1 - self.x0) * t + self.x0

    def par_y(self, t):
        return (self.y1 - self.y0) * t ** 2 + self.y0

    def draw_canvas(self, stencil):
        frames = len(stencil.chroma_sums)
        frame_t = 1 / frames
        for s in stencil.stencil:
            t = (frames - s[3]) * frame_t
            x = self.par_x(t)
            y = self.par_y(t)
            self.draw_elipse(x, y, s[0], s[1], s[2])