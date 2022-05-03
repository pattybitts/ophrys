import math

import util.const as const

from obj.PixelArray import PixelArray
from obj.DualRadial import DualRadial

#fyi width is 1618
parr = PixelArray(1000 * const.GOLDEN, 1000)
dr = DualRadial(parr, 800, 800, 1600, 550, 250, 100)
dr.draw_canvas(const.TEST_SET)
parr.show()