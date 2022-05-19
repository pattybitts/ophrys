import math, numpy as np

import util.util as util
import util.const as const

#unclear what exact purpose the object structure of this is performing
#seems more organizational convenience than actual oop
class RGUElipseStencil:

    def __init__(self, profile, threshold, theta_window):
        profile = util.swap_axes(profile)
        profile = self.prune_profile(profile, threshold)
        self.chroma_sums = []
        self.chroma_max = 0
        self.set_chroma_sums(profile)
        self.stencil = []
        self.fill_stencil(profile)
        self.theta_window = theta_window

    def prune_profile(self, profile, threshold):
        pruned_profile = []
        for p in profile:
            pruned_p = []
            for n in p:
                if n < threshold: n = 0
                n = round(n, 2)
                pruned_p.append(n)
            pruned_profile.append(pruned_p)
        return pruned_profile

    def set_chroma_sums(self, profile):
        for p in profile:
            n_sum = 0
            for n in p:
                n_sum += n
            self.chroma_sums.append(n_sum)
        for c in self.chroma_sums:
            if c > self.chroma_max: self.chroma_max = c

    def fill_stencil(self, profile):
        for i in range(len(self.chroma_sums)):
            self.add_frame(profile[i], self.chroma_sums[i], i)
        
    #leaving off here. I think we need to iterate with index, then do a 
    #(relatively simple) translation of index offset to theta_window/2
    def add_frame(self, point, chroma_sum, index):
        rgu = self.point_rgu(point, chroma_sum)
        for p in point:
            if p > 0: self.stencil.append(rgu + [index])

    def theta_offset(self, point):
        for idx, c in np.ndenumerate(point):
            pass

    def point_rgu(self, point, chroma_sum):
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