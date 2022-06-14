import math
import numpy as np

import util.calc as calc
import util.const as const
import util.util as util

from obj.PixelArray import PixelArray

class RadialParElipses():

    def __init__(self, parr, x0, y0, r0, r1, theta0, theta1, thetaw, k_shift):
        self.parr = parr
        self.x0 = x0
        self.y0 = y0
        self.r0 = r0
        self.r1 = r1
        self.theta0 = theta0
        self.theta1 = theta1
        self.thetaw = thetaw
        self.k_shift = k_shift

    #TODO simplification pass
    def draw_elipse(self, x1, y1, r, g, u, dr=math.pi/200, lp=200):
        xc = (self.x0 + x1) / 2
        yc = (self.y0 + y1) / 2
        k = calc.distance(self.x0, self.y0, x1, y1) + self.k_shift
        for i in range(2):
            theta = 0
            direction = 1 if i == 0 else -1
            while theta < math.pi:
                m = math.tan(theta)
                dt = k / lp * direction
                x = xc; xp = xc; xpp = None
                y = yc; yp = yc; ypp = None
                for j in range(lp):
                    d0 = calc.distance(self.x0, self.y0, x, y)
                    d1 = calc.distance(x1, y1, x, y)
                    if d0 + d1 >= k:
                        xp = int(round(x, 0))
                        yp = int(round(y, 0))
                        if xp != xpp or yp != ypp:
                            if xp < self.parr.x and xp >= 0 and yp <= self.parr.y and yp > 0:
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
                theta += dr

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
        theta1 = (math.asin(ly/r) if lx >= 0 else math.pi - math.asin(ly/r)) % (2 * math.pi)
        theta2 = theta1 + theta
        dx = r * math.cos(theta2)
        dy = r * math.sin(theta2)
        return self.x0 + dx, self.y0 + dy

    def draw_guidelines(self):
        frame_t = 1 / 3000
        for i in range(3000):
            x, y = self.par_xy(i * frame_t)
            xp = int(round(x, 0)); yp = int(round(y, 0))
            if xp <= self.parr.x and xp >= 0 and yp <= self.parr.y and yp >= 0: self.parr.setp(xp, yp, 255, 0, 0)

            xm, ym = self.theta_offset(x, y, .25 * self.thetaw)
            xp = int(round(xm, 0)); yp = int(round(ym, 0))
            if xp <= self.parr.x and xp >= 0 and yp <= self.parr.y and yp >= 0: self.parr.setp(xp, yp, 255, 255, 0)

            xm, ym = self.theta_offset(x, y, .5 * self.thetaw)
            xp = int(round(xm, 0)); yp = int(round(ym, 0))
            if xp <= self.parr.x and xp >= 0 and yp <= self.parr.y and yp >= 0: self.parr.setp(xp, yp, 0, 255, 0)

            xm, ym = self.theta_offset(x, y, .75 * self.thetaw)
            xp = int(round(xm, 0)); yp = int(round(ym, 0))
            if xp <= self.parr.x and xp >= 0 and yp <= self.parr.y and yp >= 0: self.parr.setp(xp, yp, 0, 255, 255)

            xm, ym = self.theta_offset(x, y, 1 * self.thetaw)
            xp = int(round(xm, 0)); yp = int(round(ym, 0))
            if xp <= self.parr.x and xp >= 0 and yp <= self.parr.y and yp >= 0: self.parr.setp(xp, yp, 0, 0, 255)                      

    '''
    stencil data:
    amp: sum of bin amplitudes above a cutoff threshold (20 rn) (this may vary far too widely to be practical?)
    com: center of mass in Hz of note
    peak: highest bin amplitude (0-80 dB)
    spike: width in Hz, centered around CoM at which a threshold (50% rn) of bin mass is reached
    '''

    def draw_canvas(self, stencil, color_path):
        frames = len(stencil)
        frame_t = 1 / frames
        for i in range(frames):
            t = 1 - i * frame_t
            x, y = self.par_xy(t)
            bins = stencil[i]
            for b in bins:
                if b['peak'] < 60: continue
                theta = self.note_theta(b['com'])
                xt, yt = self.theta_offset(x, y, theta)
                r, g, u = color_path.freq_rgu(b['com'])
                self.draw_elipse(xt, yt, r, g, u)
            if i > 750: break
    
    def note_theta(self, com):
        base_note = 55
        max_steps = 48
        steps = calc.note_steps(base_note, com)
        return steps / max_steps * self.thetaw