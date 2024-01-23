import numpy as np

from statistics import mean

class NoteStencil:

    def __init__(self, profile, custom_spec_x, custom_spec_y):
        self.profile = profile
        self.stencil = self.generate_note_profile(custom_spec_x, custom_spec_y)

    #profile axes come in as nested lists [x_values[y_values]]
    #that is, a list of bins containing lists of frames
    #or an array of shape [x_values, y_values] [bins, frames]
    #other stencil classes have begun by swapping those axes. lets see.
        
    #note this scanner is 6 pixels wide, hence the range modifications
    def generate_note_profile(self, custom_spec_x, custom_spec_y):
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