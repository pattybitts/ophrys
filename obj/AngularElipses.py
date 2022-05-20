import math
import numpy as np

import util.calc as calc
import util.const as const
import util.util as util

from obj.PixelArray import PixelArray

class AngularElipses():

    def __init__(self, parr, x0, y0, x1, y1, k_shift, t_min=.1):
        self.parr = parr
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.k_shift = k_shift
        self.t_min = t_min

    def draw_elipse(self, x1, y1, r, g, u):
        xc = (self.x0 + x1) / 2
        yc = (self.y0 + y1) / 2
        k = calc.distance(self.x0, self.y0, x1, y1) + self.k_shift
        for i in range(2):
            theta = 0
            direction = 1 if i == 0 else -1
            while theta < math.pi:
                m = math.tan(theta)
                dt = k / const.ELP * direction
                x = xc; xp = xc; xpp = None
                y = yc; yp = yc; ypp = None
                for j in range(const.ELP):
                    d0 = calc.distance(self.x0, self.y0, x, y)
                    d1 = calc.distance(x1, y1, x, y)
                    if d0 + d1 >= k:
                        xp = int(round(x, 0))
                        yp = int(round(y, 0))
                        if xp != xpp or yp != ypp:
                            if xp <= self.parr.x and xp >= 0 and yp <= self.parr.y and yp >= 0:
                                self.parr.setp(xp, yp, r, g, u)
                                xpp = xp; ypp = yp
                                #we may replace this with a simple counter so that we draw x pixels beyond r
                                break
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
        return (self.x1 - self.x0) * (self.t_min ** 2 + ((1 - self.t_min) * t) ** 2) + self.x0

    def par_y(self, t):
        return (self.y1 - self.y0) * (self.t_min + (1 - self.t_min) * t) + self.y0

    def theta_offset(self, x, y, theta):
        r = calc.distance(self.x0, self.y0, x, y)
        if theta < 0:
            theta2 = math.atan((x - self.x0)/(y - self.y0)) - abs(theta)
            dx = r * math.sin(theta2)
            dy = r * math.cos(theta2)
        else:
            theta2 = math.atan((y - self.y0)/(x - self.x0)) - abs(theta)
            dx = r * math.cos(theta2)
            dy = r * math.sin(theta2)
        return self.x0 + dx, self.y0 + dy

    #testing rn to understand boundary conditions
    def draw_canvas(self, stencil):
        elipses = len(stencil.stencil)
        frames = len(stencil.chroma_sums)
        print("Elipses to draw: " + str(elipses))
        frame_t = 1 / frames
        for s in stencil.stencil:
        #for i in range(elipses-1, elipses):
        #    s = stencil.stencil[i]
            t = (frames - s[0]) * frame_t
            x = self.par_x(t)
            y = self.par_y(t)
            xt, yt = self.theta_offset(x, y, s[1])
            #self.draw_elipse(xt, yt, 255, 255, 255)
            self.draw_elipse(xt, yt, s[2], s[3], s[4])