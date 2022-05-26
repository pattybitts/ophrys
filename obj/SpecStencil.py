import numpy as np, copy

import util.util as util

class SpecStencil:

    def __init__(self, profile):
        self.profile = profile
        self.amin = np.amin(self.profile)
        amax  = np.amax(self.profile)
        self.active_val_th = self.amin + .1 * abs(self.amin)
        self.active_slope_th = (amax - self.amin) / 3
        self.bin_width = 10.76
        self.stencil = self.generate_note_list()

    def generate_note_list(self):
        profile = util.swap_axes(self.profile)
        stencil = []
        for frame in profile:
            notes = []
            prev_bin = self.amin; p_prev_bin = self.amin
            position = self.bin_width / 2
            note_status = "none" #none, rising, falling
            com_num = 0
            com_den = 0
            for bin in frame:
                note_width = position * 2 ** (1/12) - position * .5 ** (1/12)
                slope = (bin - p_prev_bin) / (note_width * 2) 
                if note_status == "none" and bin >= self.active_val_th and slope >= self.active_slope_th / (note_width * 2):
                    note_status = "rising"
                elif note_status == "rising" and slope <= self.active_slope_th / (note_width * -2):
                    note_status = "falling"
                elif note_status == "falling" and bin <= self.active_val_th or abs(slope) < self.active_slope_th:
                    note_status = "none"
                    if com_den == 0: continue
                    com = com_num / com_den
                    mass = com_den / self.bin_width
                    notes.append([round(com, 3), round(mass, 3)])
                    com_num = 0; com_den = 0
                if note_status != "none":
                    com_num += (bin - self.amin) * position
                    com_den += (bin - self.amin)
                position += self.bin_width
                p_prev_bin = prev_bin
                prev_bin = bin
            stencil.append(copy.copy(notes))
        print("bueler?")
        for s in stencil:
            if len(s) > 0:
                print(s)