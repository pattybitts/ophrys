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
        note_ref = 55
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
                amp  = calc.bin_mass(note, 20)
                com = calc.bin_com(note)
                spike = calc.spike_score(note, calc.bin_mass(note), com)
                peak  = calc.bin_peak(note)
                notes.append({'amp': amp, 'com': com, 'spike': spike, 'peak': peak})
            stencil.append(copy.copy(notes))
        return stencil