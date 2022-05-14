import math

import util.const as const
import util.ds as ds
import util.ret as ret
import util.util as util
import util.txt as txt

from obj.PixelArray import PixelArray
from obj.DualRadial import DualRadial
from obj.ColorStencil import ColorStencil

new_stencil = True

profile = ds.load_pickle("output\profile_chroma_epiphany_22_05_12_1942_50")
if not ret.success(profile):
    print("Invalid profile")
    quit()

stencil_file = "{p}stencil_soul".format(p=const.OUT_PATH)
if new_stencil:
    print("Starting stencil generation at: " + str(util.now()))
    stencil = ColorStencil(profile)
    ds.dump_pickle(stencil, stencil_file)
else:
    stencil = ds.load_pickle(stencil_file)
if not ret.success(stencil):
    print("Invalid stencil")
    quit()

#fyi height is 1000, width is 1618
parr = PixelArray(1000 * const.GOLDEN, 1000)
dr = DualRadial(parr, 600, 500, 1100, 550, 200, 120, -1 * math.pi * .33)
start_time = util.now()
print("Starting canvas generation at: " + str(util.now()))
dr.draw_canvas(stencil.stencil)
print("Canvas generated at: " + str(util.now()) + ", now drawing ...")
parr.show()
print("Canvas drawn at: " + str(util.now()))
render_time = util.now() - start_time
print("Total render time: {r:.2f}".format(r=render_time.total_seconds()/60))