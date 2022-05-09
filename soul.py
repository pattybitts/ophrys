import util.const as const
import util.ds as ds
import util.ret as ret

from obj.PixelArray import PixelArray
from obj.DualRadial import DualRadial

soul_profile = ds.load_pickle(const.OUT_PATH + "chromagram_22_05_05_1116_50")
if not ret.success(soul_profile):
    print("Invalid file")
    quit()

#fyi width is 1618
parr = PixelArray(1000 * const.GOLDEN, 1000)
dr = DualRadial(parr, 800, 800, 900, 550, 250, 100)
dr.draw_canvas(soul_profile)
parr.show()