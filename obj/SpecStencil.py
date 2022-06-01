import numpy as np, copy

import util.util as util
import util.calc as calc
import util.const as const

class SpecStencil:

    def __init__(self, profile):
        self.profile = profile
        self.stencil = self.generate_note_profile()

    def generate_note_profile(self):
        #generating note bins
        note_ref = 110
        note_bins = []
        for i in range(0, 6):
            for j in range(0, 12):
                note_bins.append(note_ref)
                note_ref *= 2 ** (1/12)
        #creating stencil
        profile = util.swap_axes(self.profile)
        amin = np.amin(profile)
        stencil = []
        for frame in profile:
            #separating spec values into appropriate bins
            notes = []
            for n in note_bins:
                note = []
                l = n * .5 ** (1/24)
                h = n * 2 ** (1/24)
                for i in range(len(frame)):
                    hz = calc.freq(i)
                    if hz < l:
                        continue
                    elif hz >= l and hz <= h:
                        note.append([hz, frame[i] - amin])
                    elif hz > h:
                        break
                if not note: continue
                #calculating bin characteristics
                amp = calc.bin_mass(note, average=True)
                com = calc.bin_com(note)
                spike = calc.spike_score(note)
                notes.append({'amp': amp, 'com': com, 'spike': spike})
            stencil.append(copy.copy(notes))
        return stencil

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