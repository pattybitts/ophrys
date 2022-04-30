import util.const as const

from obj.PixelArray import PixelArray

parr = PixelArray(1000 * const.GOLDEN, 1000)
for x in range(parr.x):
    for y in range(parr.y):
        parr.setp(x, y, x%255, y%255, (x+y)%255)
parr.show()