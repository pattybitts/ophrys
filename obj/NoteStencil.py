import numpy as np

from statistics import mean

class NoteStencil:

    def __init__(self, profile):
        self.profile = profile
        self.stencil = self.generate_note_profile()

    #profile axes come in as nested lists [x_values[y_values]]
    #that is, a list of bins containing lists of frames
    #or an array of shape [x_values, y_values] [bins, frames]
    #other stencil classes have begun by swapping those axes. lets see.
        
    #note this scanner is 6 pixels wide, hence the range modifications
    def generate_note_profile(self):
        stencil = []
        pro = self.profile
        for y in range(0, 400):
        #for y in range(0, pro.shape[1]-1):
            for x in range(2, pro.shape[0]-4):
                avg_x0 = mean([pro[x-2, y], pro[x-1, y], pro[x, y]])
                avg_x1 = mean([pro[x+1, y], pro[x+2, y], pro[x+3, y]])
                dx = avg_x1 - avg_x0
                if dx >= 10: stencil.append({'x': x, 'y': y})
        return stencil