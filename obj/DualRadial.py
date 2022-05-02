import math

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

    def draw_line(self, theta, profile):
        #don't forget rounding to our pixel resolution!
        x0 = self.c2x - self.r2 * math.sin(theta)
        y0 = self.c2y - self.r2 * math.cos(theta)
        x1 = self.c1x - self.r1 * math.sin(theta)
        y1 = self.c1y - self.r1 * math.cos(theta)
        m = (y1 - y0) / (x1 - x0)
        pl = len(profile)
        dx = (x1 - x0) / pl / 10 #trying 10 for now, will vary with pixel density?
        for p in profile:
            for i in range(10):
                x = int(x0 + dx)
                y = int(y0 + m * dx)
                r = int(100 * p[1] / 100)
                g = int(100 * p[1] / 100)
                u = int(100 * p[1] / 100) + int(150 * p[0] / 12)
                self.parr.setp(x, y, r, g, u)