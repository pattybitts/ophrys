import math
from turtle import color
import numpy as np

import util.calc as calc
import util.const as const
import util.util as util
import util.pixel as pix

from obj.PixelArray import PixelArray

class RadialParElipses():

    def __init__(self, x0, y0, r0, r1, itheta, curve, width, k_shift):
        #define elipse origin
        self.x0 = x0
        self.y0 = y0
        #define min/max distance of curves from origin
        self.r0 = r0
        self.r1 = r1
        #defines starting angle of curve
        self.itheta = itheta
        #defines intensity of curve
        self.curve = curve
        #defines range of theta_offsets
        self.width = width
        #defines padding of elipses
        self.k_shift = k_shift

    #TODO simplification pass
    def draw_elipse(self, parr, x1, y1, rgu, dr=100, lp=100):
        dr = math.pi/dr
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
                            if xp < parr.x and xp >= 0 and yp <= parr.y and yp > 0:
                                parr.setp(xp, yp, rgu)
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
        theta = self.itheta + (self.curve) * t ** 3
        x = self.x0 + r * math.cos(theta)
        y = self.y0 + r * math.sin(theta)
        return x, y

    def theta_offset(self, x, y, theta):
        r = calc.distance(self.x0, self.y0, x, y)
        lx = x - self.x0; ly = y - self.y0
        theta1 = (math.asin(ly/r) if lx >= 0 else math.pi - math.asin(ly/r)) % (2 * math.pi)
        theta2 = theta1 + theta
        dx = r * math.cos(theta2)
        dy = r * math.sin(theta2)
        return self.x0 + dx, self.y0 + dy

    def draw_guidelines(self, parr):
        frame_t = 1 / 3000
        for i in range(3000):
            x, y = self.par_xy(i * frame_t)
            for j in range(2):
                xm, ym = self.theta_offset(x, y, 1.0 * j * self.width)
                xp = int(round(xm, 0)); yp = int(round(ym, 0))
                if xp <= parr.x and xp >= 0 and yp <= parr.y and yp >= 0: parr.setp(xp, yp, (255, 255, 255))       
        return parr

    '''
    stencil data:
    amp: sum of bin amplitudes above a cutoff threshold (20 rn) (this may vary far too widely to be practical?)
    com: center of mass in Hz of note
    peak: highest bin amplitude (0-80 dB)
    spike: width in Hz, centered around CoM at which a threshold (50% rn) of bin mass is reached
    '''

    #TODO this still needs to be updated to the colormap paradigm
    @staticmethod
    def draw_canvas(parr, stencil, map_rpes, res_pars):
        len_frames = len(stencil)
        frame_t = 1 / len_frames
        for i in range(len_frames):
            t = 1 - i * frame_t
            for mr in map_rpes:
                color_map = mr[0]
                cm_min = None
                cm_max = len(color_map) - 1
                for j in range(len(color_map)):
                    if not color_map[j] is None and cm_min is None: cm_min = j
                    if color_map[j] is None and not cm_min is None: cm_max = j; break
                rpe = mr[1]
                x, y = rpe.par_xy(t)
                bins = stencil[i]
                for j in range(len(bins)):
                    b = bins[j]
                    #we could use another module to create consistent filtering between test and elipse
                    #(it's unlikely i'll actually do that)
                    if b['peak'] < 50: continue
                    if color_map[j] is None: continue
                    amp_val = (b['peak'] - 50) / 30 * 1.5
                    if amp_val > 1: amp_val = 1
                    theta = rpe.note_theta(cm_min, cm_max, j)
                    xt, yt = rpe.theta_offset(x, y, theta)
                    rgu = pix.saturate(color_map[j], amp_val)
                    rpe.draw_elipse(parr, xt, yt, rgu, res_pars[1], res_pars[2])
            if res_pars[0] and i > res_pars[0]: break
        return parr
    
    def note_theta(self, min, max, bin):
        return (bin - min) / (max - min) * self.width