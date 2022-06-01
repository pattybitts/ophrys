import math, numpy as np

import util.const as const
import util.util as util
import util.ds as ds
import util.ret as ret
import util.txt as txt

from obj.PixelArray import PixelArray
from obj.AngularElipses import AngularElipses
from obj.RGUElipseStencil import RGUElipseStencil
from obj.SpecStencil import SpecStencil
from obj.TestDisplay import TestDisplay

start_time = util.now()
print("Intializing at: " + txt.time_str(util.now()))
#profile = ds.load_pickle("output\profile_spec_test_a4_a5_22_05_26_2013_55")
profile = ds.load_pickle("output\profile_spec_epiphany_22_05_26_2051_53")
if not ret.success(profile):
    print("Invalid profile")
    quit()
profile = profile[0:800,:]

new_stencil = True

stencil_file = "{p}spec_stencil_test".format(p=const.OUT_PATH)
if new_stencil:
    print("Starting stencil generation at: " + txt.time_str(util.now()))
    stencil = SpecStencil(profile)
    ds.dump_pickle(stencil, stencil_file)
else:
    stencil = ds.load_pickle(stencil_file)
if not ret.success(stencil):
    print("Invalid stencil")
    quit()

x, y  = profile.shape
parr = PixelArray(y, x)
td = TestDisplay(parr, np.amin(profile), np.amax(profile))
print("Starting canvas generation at: " + txt.time_str(util.now()))
td.draw_array(profile)
#td.heat_overlay(profile)
#td.peak_overlay(profile)
td.octave_overlay(profile)
#td.note_overlay(profile)
td.com_overlay(profile, stencil.stencil)
print("Canvas generated at: " + txt.time_str(util.now()) + ", now drawing ...")
parr.show()

render_time = util.now() - start_time
print("Total render time: " + txt.delta_str(render_time))

'''
stencil_file = "{p}stencil_soul".format(p=const.OUT_PATH)
if new_stencil:
    print("Starting stencil generation at: " + str(util.now()))
    stencil = RGUElipseStencil(profile, .5, math.pi)
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
x1 = 1600
y1 = 1000
k_shift = 20
ae = AngularElipses(parr, x0, y0, x1, y1, k_shift, .05)
print("Starting canvas generation at: " + str(util.now()))
ae.draw_canvas(stencil)
print("Canvas generated at: " + str(util.now()) + ", now drawing ...")
parr.show()
render_time = util.now() - start_time
print("Total render time: {r:.1f}".format(r=render_time.total_seconds()))
'''