import math
import numpy as np

import util.calc as calc
import util.const as const
import util.util as util

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