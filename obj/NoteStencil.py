import numpy as np
import math as math

from statistics import mean

import util.calc as calc
import util.const as const

class NoteStencil:

    def __init__(self, profile, custom_spec_x, custom_spec_y):
        self.profile = profile
        self.stencil = self.generate_note_profile(custom_spec_x, custom_spec_y)
        self.stencil = self.define_note_properties()

    #profile axes come in as nested lists [x_values[y_values]]
    #that is, a list of bins containing lists of frames
    #or an array of shape [x_values, y_values] [bins, frames]
    #other stencil classes have begun by swapping those axes. lets see.
        
    #second draft of note generation
    #might need to draw a diagram to explain these parsing variables
    #TODO implement actual filtering functions
    def generate_note_profile(self, custom_spec_x, custom_spec_y, dx=3, dy=2, x_slope=11, y_slope=-5, wmax=20, pmin=1):
        pro = self.profile
        xmax = custom_spec_x if custom_spec_x else pro.shape[0] - (1 + 2 * dx)
        ymax = custom_spec_y if custom_spec_y else pro.shape[1] - 1
        ymin = 2 * dy - 1
        #first filter, using 3 slope scans to find ts
        #scanning y top down so that duplicate notes are quickly skipped
        notes_1 = []
        for y in range(ymax, ymin, -1):
            #scanning x for rising slope
            for x in range(0, xmax):
                avg_x0 = 0; avg_x1 = 0
                for i in range(0, dx):
                    avg_x0 += pro[x+i, y]
                    avg_x1 += pro[x+dx+i, y]
                mx = (avg_x1 - avg_x0) / dx
                if mx < x_slope: continue
                #checking if within existing note
                in_note = False
                for n in reversed(notes_1):
                    if y >= n['y0'] and y <= n['y1'] and x <= n['x1'] and x >= n['x0']:
                        n['points'] += 1
                        in_note = True
                        break
                if in_note: continue
                #scanning x for falling slope
                x1 = None
                xcap = xmax if xmax < x+wmax else x+wmax
                for xp in range(x, xcap):
                    avg_x0 = 0; avg_x1 = 0
                    for i in range(0, dx):
                        avg_x0 += pro[xp+i, y]
                        avg_x1 += pro[xp+dx+i, y]
                    mx = (avg_x1 - avg_x0) / dx
                    if mx <= x_slope * -1: x1 = xp + dx * 2; break
                if not x1: continue
                #scanning down y for t edge
                y0 = ymin
                for yp in range(y, ymin, -1):
                    avg_y0 = 0; avg_y1 = 0
                    for xp in range(x, x1):
                        for i in range(0, dy):
                            avg_y0 += pro[xp, yp-i]
                            avg_y1 += pro[xp, yp-dy-i]
                    my = (avg_y1 - avg_y0) / (x1 - x) / dy
                    if my <= y_slope: y0 = yp - dy; break
                #creating note item
                notes_1.append({'x0': x, 'x1': x1, 'y0': y0, 'y1': y, 'points': 1})
        #second filter, combining overlapping notes
        notes_2 = []
        for n in notes_1:
            overlap = False
            for n2 in notes_2:
                #new logic! way way simpler if any n minimum is outside the n2 maximum
                x00 = n['x0'] < n2['x0']; x01 = n['x0'] > n2['x1']
                x10 = n['x1'] < n2['x0']; x11 = n['x1'] > n2['x1']
                y00 = n['y0'] < n2['y0']; y01 = n['y0'] > n2['y1']
                y10 = n['y1'] < n2['y0']; y11 = n['y1'] > n2['y1']
                if x01+x10+y01+y10: continue
                overlap = True
                if x00: n2['x0'] = n['x0']
                if x11: n2['x1'] = n['x1']
                if y00: n2['y0'] = n['y0']
                if y11: n2['y1'] = n['y1']
                n2['points'] += n['points']
            if not overlap: notes_2.append(n)
        #third filter, cutting notes with few points
        notes_3 = []
        for n2 in notes_2:
            if n2['points'] >= pmin: notes_3.append(n2)
        #sort bottom up left to right
        notes_3.sort(key=lambda n: n['x0'])
        notes_3.sort(key=lambda n: n['y0'])
        return notes_3
    
    #at this time, 5 note properties are
    #origin: y0 coordinate; unit: frame
    #pitch: xcom coordinate; unit: hz
    #volume: sum amplitudes; unit: decibel
    #breadth: minimum width from xcom containing x% volume; unit: d-hz
    #stretch: distance between y0 and yCoM; unit: d-frame
    def define_note_properties(self, xpct=.5, dx=.2):
        pro = self.profile
        amin = np.amin(pro)
        for n in self.stencil:
            #creating array of xcolumn sums for total volume, com, breadth
            xsums = []
            for x in range(n['x0'], n['x1']+1):
                xsum = 0
                for y in range(n['y0'], n['y1']+1):
                    xsum += pro[x, y] - amin
                xsums.append(xsum)
            xcom = calc.array_com(xsums)
            volume = np.sum(xsums)
            #calculating breadth by exoanding xvol by dx, using xsums
            xvol = xsums[round(xcom)] * dx
            xinc = 0; xwidth = 0
            while(xvol < volume * xpct):
                xinc += 1
                if round(xcom + xinc * dx) < len(xsums):
                    xwidth += 1
                    xvol += xsums[round(xcom + xinc * dx)] * dx
                if round(xcom - xinc * dx) >= 0:
                    xwidth += 1
                    xvol += xsums[round(xcom - xinc * dx)] * dx
            breadth = dx * (1 + xwidth) * const.FREQ_INC
            #creating array of yrow sums for yCoM -> stretch
            ysums = []
            for y in range(n['y0'], n['y1']+1):
                ysum = 0
                for x in range(n['x0'], n['x1']+1):
                    ysum += pro[x, y] - amin
                ysums.append(ysum)
            ycom = calc.array_com(ysums)
            n['origin'] = n['y0']
            n['volume'] = volume
            n['pitch'] = (xcom + n['x0'] + .5) * const.FREQ_INC
            n['breadth'] = breadth
            n['stretch'] = ycom
        return self.stencil

    #note this scanner is 6 pixels wide, hence the range modifications
    def generate_note_profile_dep(self, custom_spec_x, custom_spec_y):
        #MAYBE: add customization of dx_width with a avgs formed with for loops
        pro = self.profile
        xmax = custom_spec_x if custom_spec_x else pro.shape[0] - 4
        ymax = custom_spec_y if custom_spec_y else pro.shape[1] - 1
        #first filter, list of points of notable slope
        slope_points = []
        for y in range(0, ymax):
            for x in range(2, xmax):
                avg_x0 = mean([pro[x-2, y], pro[x-1, y], pro[x, y]])
                avg_x1 = mean([pro[x+1, y], pro[x+2, y], pro[x+3, y]])
                dx = avg_x1 - avg_x0
                if dx >= 10: slope_points.append({'x': x, 'y': y})
        #second filter, slope points grouped
        slope_groups = []
        yin_min = 0; yin_max = 10; xin_min = -2; xin_max = 3
        for sp in slope_points:
            in_group = False
            for sg in reversed(slope_groups):
                if sp['y'] <= sg['lead_y'] + yin_max and sp['x'] <= sg['lead_x'] + xin_max \
                    and sp['y'] >= sg['lead_y'] + yin_min and sp['x'] >= sg['lead_x'] + xin_min:
                    sg['points'].append(sp)
                    sg['lead_x'] = sp['x']
                    sg['lead_y'] = sp['y']
                    in_group = True
                    break
            if not in_group:
                new_group = {}
                new_group['lead_x'] = sp['x']
                new_group['lead_y'] = sp['y']
                new_group['points'] = [sp]
                slope_groups.append(new_group)
        #third filter, removing small groups
        large_groups = []
        for sg in slope_groups:
            if len(sg['points']) > 4: large_groups.append(sg)
        #setting group properties
        for lg in large_groups:
            lg['xmin'] = xmax
            lg['xmax'] = 0
            lg['ymin'] = ymax
            lg['ymax'] = 0
            for p in lg['points']:
                if p['x'] < lg['xmin']: lg['xmin'] = p['x']
                if p['x'] > lg['xmax']: lg['xmax'] = p['x']
                if p['y'] < lg['ymin']: lg['ymin'] = p['y']
                if p['y'] > lg['ymax']: lg['ymax'] = p['y']
        return large_groups