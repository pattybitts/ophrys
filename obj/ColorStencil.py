import math
import numpy as np

import util.const as const
import util.util as util

from obj.PixelArray import PixelArray

class ColorStencil():

    def __init__(self, profile):
        profile = util.swap_axes(profile)
        self.chroma_sums = []
        self.chroma_max = 0
        self.set_chroma_sums(profile)
        self.stencil = self.create_stencil(profile)

    def create_point(self, point, chroma_sum):
        com_num = 0
        for idx, c in np.ndenumerate(point):
            c = round(c, 1)
            com_num += c * idx[0]
        com = 0 if chroma_sum == 0 else (com_num / chroma_sum)
        com_offset = com + 10 #constant offset to set d as central note
        theta = com_offset % 12 / 12 * 2 * math.pi
        #setting relative strengths of rgu
        r = const.R_RANGE[0] + .5 * const.R_RANGE[1] - math.cos(theta) * .5 * (const.R_RANGE[1] - const.R_RANGE[0])
        g = const.G_RANGE[0] + .5 * const.G_RANGE[1] + math.cos(theta) * .5 * (const.G_RANGE[1] - const.G_RANGE[0])
        u = const.U_RANGE[0] + .5 * const.U_RANGE[1] + math.sin(theta) * .5 * (const.U_RANGE[1] - const.U_RANGE[0])
        brightness = chroma_sum / self.chroma_max 
        r = int(round(r * brightness * 255, 0))
        g = int(round(g * brightness * 255, 0))
        u = int(round(u * brightness * 255, 0))
        return [r, g, u]

    def create_stencil(self, profile):
        stencil = []
        for i in range(len(self.chroma_sums)):
            stencil.append(self.create_point(profile[i], self.chroma_sums[i]))
        return stencil

    def set_chroma_sums(self, profile):
        for p in profile:
            n_sum = 0
            for n in p:
                n_sum += n
            self.chroma_sums.append(n_sum)
        for c in self.chroma_sums:
            if c > self.chroma_max: self.chroma_max = c 
