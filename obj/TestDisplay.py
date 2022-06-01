import math
import numpy as np
import copy

import util.calc as calc
import util.const as const
import util.util as util
import util.ds as ds

from obj.PixelArray import PixelArray

class TestDisplay():

    def __init__(self, parr, min, max):
        self.parr = parr
        self.min = min
        self.max = max

    def draw_array(self, nparr):
        nparr = util.swap_axes(nparr)
        rgumod = 255 / (self.max - self.min)
        for idx, val in np.ndenumerate(nparr):
            val  = int(abs(val * rgumod))
            self.parr.setp(idx[0], idx[1], val, val, val)
            if idx[0] >= 5000: break

    def peak_overlay(self, nparr):
        frames = []
        nparr = util.swap_axes(nparr)
        for frame in nparr:
            notes = []
            prev_x = 0
            prev_dx = 0
            for i in range(0, len(frame), 10):
                field_width = i if i <= 19 else 19
                field = []
                for j in range(field_width+1):
                    field.append(frame[i - j])
                lmax = np.amax(field)
                lidx = field.index(lmax)
                if lmax >= -25: notes.append([i - lidx, 'max'])
                '''
                x = frame[i]
                dx = x - prev_x
                ddx = dx - prev_dx
                if abs(dx) < 2:
                    if ddx < -5: notes.append([i, 'max'])
                    if ddx > 5: notes.append([i, 'min'])
                prev_x = x
                prev_dx = dx
                '''
            frames.append(copy.copy(notes))
        for i in range(len(frames)):
            f = frames[i]
            for n in f:
                c = [255, 0, 0] if n[1] == 'max' else [0, 255, 0]
                self.parr.setp(i, n[0], c[0], c[1], c[2])

    def heat_overlay(self, nparr):
        nparr = util.swap_axes(nparr)
        for idx, val in np.ndenumerate(nparr):
            if val > -10: self.parr.setp(idx[0], idx[1], 0, 0, 255)
            elif val > -20: self.parr.setp(idx[0], idx[1], 0, 255, 0)
            elif val > -30: self.parr.setp(idx[0], idx[1], 255, 0, 0)
            if idx[0] >= 5000: break

    def octave_overlay(self, nparr):
        nparr = util.swap_axes(nparr)
        a_notes = [110, 220, 440, 880, 1760, 3520]
        for idx, val in np.ndenumerate(nparr):
            hz = calc.freq(idx[1])
            for a in a_notes:
                if a - hz > -2.7 and a - hz < 0:
                    self.parr.setp(idx[0], idx[1], 255, 255, 0)
                    break

    def note_overlay(self, nparr):
        nparr = util.swap_axes(nparr)
        note_bins = ds.load_pickle("input\\note_bins")
        for idx, val in np.ndenumerate(nparr):
            hz = calc.freq(idx[1])
            for n in note_bins:
                if n - hz > -1.35 and n - hz < 1.35:
                    self.parr.setp(idx[0], idx[1], 0, 255, 255)
                    break

    def com_overlay(self, nparr, stencil):
        nparr = util.swap_axes(nparr)
        for i in range(len(stencil)):
            s = stencil[i]
            for n in s: 
                val = n['amp'] / (self.max - self.min)
                if val < .75: continue
                int_val = int(round(val * 255))
                y = int(round((n['com'] - const.FREQ_INC / 2) / const.FREQ_INC))
                self.parr.setp(i, y, 0, 255 - int_val, int_val)
    
    '''
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
    '''