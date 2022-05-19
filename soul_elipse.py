import math

import util.const as const
import util.util as util
import util.ds as ds
import util.ret as ret

from obj.PixelArray import PixelArray
from obj.AngularElipses import AngularElipses
from obj.RGUElipseStencil import RGUElipseStencil

start_time = util.now()
print("Intializing at : " + str(start_time))
profile = ds.load_pickle("output\profile_chroma_epiphany_22_05_12_1942_50")
if not ret.success(profile):
    print("Invalid profile")
    quit()

new_stencil = True

stencil_file = "{p}stencil_soul".format(p=const.OUT_PATH)
if new_stencil:
    print("Starting stencil generation at: " + str(util.now()))
    stencil = RGUElipseStencil(profile, .3, math.pi / 2)
    ds.dump_pickle(stencil, stencil_file)
else:
    stencil = ds.load_pickle(stencil_file)
if not ret.success(stencil):
    print("Invalid stencil")
    quit()

#fyi height is 1000, width is 1618
parr = PixelArray(1000 * const.GOLDEN, 1000)

x0 = 500
y0 = 200
x1 = 1500
y1 = 900
k_shift = 15
ae = AngularElipses(parr, x0, y0, x1, y1, k_shift)
print("Starting canvas generation at: " + str(util.now()))
ae.draw_canvas(stencil)
print("Canvas generated at: " + str(util.now()) + ", now drawing ...")
parr.show()
render_time = util.now() - start_time
print("Total render time: {r:.1f}".format(r=render_time.total_seconds()))