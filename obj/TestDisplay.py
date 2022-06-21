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
        rgumod = 255 / (self.max - self.min)
        for idx, val in np.ndenumerate(nparr):
            val  = int(abs(val * rgumod))
            self.parr.setp(idx[0], idx[1], val, val, val)
            if idx[0] >= 5000: break

    def peak_overlay(self, nparr):
        frames = []
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
        for idx, val in np.ndenumerate(nparr):
            if val > -10: self.parr.setp(idx[0], idx[1], 0, 0, 255)
            elif val > -20: self.parr.setp(idx[0], idx[1], 0, 255, 0)
            elif val > -30: self.parr.setp(idx[0], idx[1], 255, 0, 0)
            if idx[0] >= 5000: break

    def octave_overlay(self, nparr):
        a_notes = [110, 220, 440, 880, 1760, 3520]
        for idx, val in np.ndenumerate(nparr):
            hz = calc.freq(idx[1])
            for a in a_notes:
                if a - hz > -2.7 and a - hz < 0:
                    self.parr.setp(idx[0], idx[1], 255, 255, 0)
                    break

    def note_overlay(self, nparr):
        note_bins = ds.load_pickle("input\\note_bins")
        for idx, val in np.ndenumerate(nparr):
            hz = calc.freq(idx[1])
            for n in note_bins:
                if n - hz > -1.35 and n - hz < 1.35:
                    self.parr.setp(idx[0], idx[1], 0, 255, 255)
                    break

    '''
    stencil data:
    amp: sum of bin amplitudes above a cutoff threshold (20 rn) averaged over valid points
    com: center of mass in Hz of note
    peak: highest bin amplitude (0-80 dB)
    spike: width in Hz, centered around CoM at which a threshold (50% rn) of bin mass is reached
    '''

    def com_overlay(self, stencil):
        for i in range(len(stencil)):
            s = stencil[i]
            for n in s: 
                amp_val = n['amp'] / (self.max - self.min)
                peak_val = n['peak'] / (self.max - self.min)
                y = int(round((n['com'] - const.FREQ_INC / 2) / const.FREQ_INC))
                if amp_val > .3: self.parr.setp(i, y, 255, 0, 0)
                if peak_val > .7: self.parr.setp(i, y, 0, 255, 0)
                if n['spike'] < 10: self.parr.setp(i, y, 0, 0, 255)

    def color_overlay(self, stencil, color_map):
        for i in range(len(stencil)):
            frame = copy.copy(stencil[i])
            for j in range(len(frame)):
                bin = copy.copy(frame[j])
                if bin['peak'] < 50: continue
                #we might just center these on bins eventually
                y = int(round((bin['com'] - const.FREQ_INC / 2) / const.FREQ_INC))
                pixel = copy.copy(color_map[j])
                #amp_val = bin['amp'] / (self.max - self.min)
                amp_val = (bin['peak'] - 50) / 30
                pixel.saturate(amp_val)
                self.parr.setp(y, i, pixel.r, pixel.g, pixel.u)