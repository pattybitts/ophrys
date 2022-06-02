import math
import numpy as np

import util.calc as calc
import util.const as const
import util.util as util

from obj.PixelArray import PixelArray

class RadialParElipses():

    def __init__(self, parr, x0, y0, r0, r1, theta0, theta1, thetar, k_shift):
        self.parr = parr
        self.x0 = x0
        self.y0 = y0
        self.r0 = r0
        self.r1 = r1
        self.theta0 = theta0
        self.theta1 = theta1
        self.thetar = thetar
        self.k_shift = k_shift

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

    def par_xy(self, t):
        r = self.r0 + (self.r1 - self.r0) * t ** 2
        theta = self.theta0 + (self.theta1 - self.theta0) * t ** 3
        x = self.x0 + r * math.cos(theta)
        y = self.y0 + r * math.sin(theta)
        return x, y

    #let's just throw some angels at the wall
    def theta_offset(self, x, y, theta):
        r = calc.distance(self.x0, self.y0, x, y)
        lx = x - self.x0; ly = y - self.y0
        if ly == 0: return x, y
        theta2 =  math.atan(lx/ly) + theta
        dx = r * math.sin(theta2)
        dy = r * math.cos(theta2)
        return self.x0 + dx, self.y0 + dy

    def draw_guidelines(self):
        frame_t = 1 / 1000
        for i in range(1000):
            x, y = self.par_xy(i * frame_t)
            xp = int(round(x, 0)); yp = int(round(y, 0))
            if xp <= self.parr.x and xp >= 0 and yp <= self.parr.y and yp >= 0: self.parr.setp(xp, yp, 255, 0, 0)

            xm, ym = self.theta_offset(x, y, -1 * self.thetar)
            xp = int(round(xm, 0)); yp = int(round(ym, 0))
            if xp <= self.parr.x and xp >= 0 and yp <= self.parr.y and yp >= 0: self.parr.setp(xp, yp, 0, 255, 0)

            xm, ym = self.theta_offset(x, y, -.5 * self.thetar)
            xp = int(round(xm, 0)); yp = int(round(ym, 0))
            if xp <= self.parr.x and xp >= 0 and yp <= self.parr.y and yp >= 0: self.parr.setp(xp, yp, 255, 255, 0)

            xm, ym = self.theta_offset(x, y, 1 * self.thetar)
            xp = int(round(xm, 0)); yp = int(round(ym, 0))
            if xp <= self.parr.x and xp >= 0 and yp <= self.parr.y and yp >= 0: self.parr.setp(xp, yp, 0, 0, 255)

            xm, ym = self.theta_offset(x, y, .5 * self.thetar)
            xp = int(round(xm, 0)); yp = int(round(ym, 0))
            if xp <= self.parr.x and xp >= 0 and yp <= self.parr.y and yp >= 0: self.parr.setp(xp, yp, 255, 0, 255)                      

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