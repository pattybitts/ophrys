import math
import numpy as np

import util.calc as calc
import util.const as const
import util.util as util

from obj.PixelArray import PixelArray

class AngularElipses():

    def __init__(self, parr):
        self.parr = parr

    def draw_elipse(self, x0, y0, x1, y1, k):
        xc = (x0 + x1) / 2
        yc = (y0 + y1) / 2
        for i in range(2):
            theta = 0
            direction = 1 if i == 0 else -1
            while theta < math.pi:
                m = math.tan(theta)
                dt = k / const.ELP * direction
                x = xc; xp = xc; xpp = None
                y = yc; yp = yc; ypp = None
                for j in range(const.ELP):
                    d0 = calc.distance(x0, y0, x, y)
                    d1 = calc.distance(x1, y1, x, y)
                    if d0 + d1 >= k - const.EW / 2 and d0 + d1 <= k + const.EW / 2:
                        xp = int(round(x, 0))
                        yp = int(round(y, 0))
                        if xp != xpp or yp != ypp:
                            if xp <= self.parr.x and xp >= 0 and yp <= self.parr.y and yp >= 0:
                                self.parr.setp(xp, yp, 255, 255, 255)
                                xpp = xp; ypp = yp
                                break
                    if abs(m) >= 1:
                        y += dt
                        x += dt / m
                    else:
                        x += dt
                        y += dt * m
                theta += const.EDR