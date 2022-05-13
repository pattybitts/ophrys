import math
import numpy as np

import util.const as const
import util.util as util

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

    #temporarily modding to only draw a quarter to take down testing time
    def draw_canvas(self, stencil):
        theta = const.D_START
        while theta <= const.L_START:
            self.draw_line(theta, stencil, loose=False)
            theta += const.DDR
        theta = 0
        while theta <= 2 * math.pi - (const.L_START - const.D_START):
            self.draw_line(theta + const.L_START, stencil, loose=True)
            theta += const.LDR

    def draw_line(self, theta, stencil, loose=True):
        #don't forget rounding to our pixel resolution!
        #this will definitely get more complex as we go
        x0 = self.c2x - self.r2 * math.sin(theta)
        y0 = self.c2y - self.r2 * math.cos(theta)
        x1 = self.c1x - self.r1 * math.sin(theta)
        y1 = self.c1y - self.r1 * math.cos(theta)
        line_x_len = (x1 - x0)
        if line_x_len == 0: return
        m = (y1 - y0) / line_x_len
        line_points = const.LLP if loose else const.DLP
        dx = line_x_len / line_points
        x = x0; xp = x0; xpp = None
        y = y0; yp = y0; ypp = None
        for i in range(line_points):
            s = stencil[int(round(i / line_points * len(stencil), 0))]
            xp = int(round(x, 0))
            yp = int(round(y, 0))
            if xp != xpp or yp != ypp:
                if xp <= self.parr.x and xp >= 0 \
                    and yp <= self.parr.y and yp >= 0: self.parr.setp(xp, yp, s[0], s[1], s[2])
            xpp = xp; ypp = yp
            x += dx
            y += dx * m
