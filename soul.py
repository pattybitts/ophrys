import math

import util.const as const

from obj.PixelArray import PixelArray
from obj.DualRadial import DualRadial

parr = PixelArray(1000 * const.GOLDEN, 1000)
dr = DualRadial(parr, 500, 500, 400, 250, 250, 100)
for i in range(100):
    dr.draw_line(i/(2*math.pi), const.TEST_SET)
#for x in range(parr.x):
#    for y in range(parr.y):
#        parr.setp(x, y, x%255, y%255, (x+y)%255)
parr.show()