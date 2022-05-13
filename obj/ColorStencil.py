import math
import numpy as np

import util.const as const
import util.util as util

from obj.PixelArray import PixelArray

class ColorStencil():

    def __init__(self, profile):
        self.stencil = self.create_stencil(profile)

    def create_point(self, point):
        com_num = 0
        com_den = 0
        for idx, c in np.ndenumerate(point):
            c = round(c, 1)
            com_num += c * idx[0]
            com_den += c
        com = 0 if com_den == 0 else (com_num / com_den)
        com_offset = com + 10 #constant offset to set d as central note
        theta = com_offset % 12 / 12 * 2 * math.pi
        r = int(round(127.5 - math.cos(theta) * 127.5, 0))
        g = int(round(127.5 + math.cos(theta) * 127.5, 0))
        u = int(round(177.5 + math.sin(theta) * 77.5, 0))
        return [r, g, u]

    def create_stencil(self, profile):
        stencil = []
        profile = util.swap_axes(profile)
        for p in profile:
            stencil.append(self.create_point(p))
        return stencil