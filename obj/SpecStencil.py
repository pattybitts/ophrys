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
        stencil = {'freq':[], 'amp':[], 'spike':[], 'peak':[], 'com':[]}
        for i in range(len(profile)):
            frame = profile[i]
            #separating spec values into appropriate bins
            freqs = []; amps = []; spikes = []; peaks = []; coms = []
            for n in note_bins:
                note = []
                l = n * .5 ** (1/24)
                h = n * 2 ** (1/24)
                for j in range(len(frame)):
                    hz = calc.freq(j)
                    if hz < l:
                        continue
                    elif hz >= l and hz <= h:
                        note.append([hz, frame[j] - amin])
                    elif hz > h:
                        break
                if not note:
                    com = n
                    amp = 0
                    spike = 0
                    peak = 0
                else:
                    com = SpecStencil.bin_com(note, 20)
                    amp  = SpecStencil.bin_mass(note, 10)
                    spike = SpecStencil.spike_score(note, com)
                    peak  = SpecStencil.bin_peak(note)
                freqs.append(n); amps.append(amp); spikes.append(spike); peaks.append(peak); coms.append(com)
            for x in [('freq', freqs), ('amp', amps), ('spike', spikes), ('peak', peaks), ('com', coms)]:
                stencil[x[0]].append(copy.copy(x[1]))
        #oof. ok at this point we should have a stencil with distinct np-compatible arrays
        #new_stencil = np.ndarray((len(stencil['freq']), len(stencil['freq'][0])))
        new_stencil = [] #there's no way this works, right? #harumph. right
        for i in range(len(stencil['freq'])):
            ns = []
            for j in range(len(stencil['freq'][0])):
                ns.append({})
            new_stencil.append(copy.copy(ns))
        for key, val in stencil.items():
            amin  = np.amin(val)
            amax  = np.amax(val)
            for idx, v in np.ndenumerate(val):
                new_stencil[idx[0]][idx[1]][key] = v if key == 'freq' or key == 'com' else (v - amin) / (amax - amin)
        return new_stencil

    #static bin computation functions
    @staticmethod
    def bin_peak(points):
        max = 0
        for p in points:
            if p[1] > max: max = p[1]
        return max

    @staticmethod
    def bin_mass(points, threshold=None):
        count = 0
        mass = 0
        for p in points:
            if threshold and p[1] < threshold: continue
            count += 1
            mass += p[1]
        if count > 0: return mass / count
        return mass

    #i should figure out how i want to structure returns on this
    @staticmethod
    def bin_com(points, th=20):
        numerator = 0
        denominator = 0
        for p in points:
            if p[1] < th: continue
            numerator += p[0] * p[1]
            denominator += p[1]
        if denominator == 0: return 0
        return numerator / denominator

    #returns the width in hz at which the mass of the spike reaches the given percentage of the bin's mass
    @staticmethod
    def spike_score(points, center, mass_th=0, spike_th=.25):
        mass = 0
        for p in points:
            if p[1] >= mass_th: mass += p[1]
        if mass == 0: return 0
        center_idx = 0
        for p in points:
            if abs(p[0] - center) <= const.FREQ_INC / 2: center_idx = points.index(p); break
        spike_mass = points[center_idx][1]
        r = 1
        while spike_mass / mass < spike_th:
            rl = center_idx - r
            rh = center_idx + r
            if rl >= 0: spike_mass += points[rl][1]
            if rh < len(points): spike_mass += points[rh][1]
            r += 2
        return (r / len(points)) * (spike_th / (spike_mass / mass))