import math
import numpy as np
import copy

import util.calc as calc
import util.const as const
import util.util as util
import util.ds as ds
import util.pixel as pix

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
            self.parr.setp(idx[0], idx[1], (val, val, val))
            #this should find a way to move into a script parameter
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

    def bin_val_overlay(self, stencil, val_str, dot=True):
        for i in range(len(stencil)):
            s = stencil[i]
            if dot:
                for bin in s:
                    y = int(round((bin['com'] - const.FREQ_INC / 2) / const.FREQ_INC, 0))
                    val = bin[val_str]
                    self.overlay_pixel(val, i, y)
            else:
                for y in range(len(self.parr.arr[0])):
                    freq = y * const.FREQ_INC + const.FREQ_INC
                    #eliminate hardcoding! :p
                    if freq < 55 or freq > 3520: continue
                    bin  = int(round(calc.note_steps(55, freq), 0))
                    if bin < 0 or bin >= len(s): continue
                    val = s[bin][val_str]
                    self.overlay_pixel(val, i, y)

    def overlay_pixel(self, val, i, y):
        if val >= .95: self.parr.setp(y, i, (0, 0, 255))
        elif val >= .875: self.parr.setp(y, i, (0, 255, 255))
        elif val >= .8: self.parr.setp(y, i, (0, 255, 0))
        elif val >= .725: self.parr.setp(y, i, (255, 255, 0))
        else: self.parr.setp(y, i, (255, 0, 0))
        '''
        else:
            cint = int(round(val * 255, 0))
            self.parr.setp(y, i, (cint, cint, cint))
        '''

    def color_overlay(self, stencil, color_map, spec_aligned=True):
        for i in range(len(stencil)):
            frame = stencil[i]
            for j in range(12, len(frame)):
                rgu = color_map[j]
                if not rgu: continue
                bin = frame[j]
                if bin['peak'] < .675: continue
                sat_val = calc.rescale(bin['peak'], .5, .75, 1.1)
                #satsign = 1 if sat_val > 0 else -1
                #sat_val = satsign * math.sqrt(abs(sat_val))
                #sharp_val here too?
                rgu = pix.adjust_saturation(color_map[j], sat_val)
                if spec_aligned: y = int(round((bin['freq'] - const.FREQ_INC / 2) / const.FREQ_INC))
                else: y = j * 12
                self.parr.setp(y, i, rgu)
                self.parr.setp(y+1, i, rgu)

    def sheet_music_overlay(self, stencil, color_map):
        for i in range(len(stencil)):
            frame = stencil[i]
            for j in range(0, len(frame)):
                rgu =  color_map[j]
                if not rgu: continue
                bin = frame[j]
                if bin['peak'] < .65: continue
                y = j * 12
                line_thickness = int(round(calc.rescale(bin['peak'], .65, .85, 1.05, 0, 6), 0))
                for k in range(line_thickness):
                    self.parr.setp(y+k, i, rgu)