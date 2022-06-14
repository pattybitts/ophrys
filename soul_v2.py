import math, numpy as np

import util.const as const
import util.util as util
import util.ds as ds
import util.ret as ret
import util.txt as txt

from obj.PixelArray import PixelArray
from obj.SpecStencil import SpecStencil
from obj.ColorPath import ColorPath
from obj.TestDisplay import TestDisplay
from obj.RadialParElipses import RadialParElipses

start_time = util.now()
print("Intializing at: " + txt.time_str(util.now()))
#profile = ds.load_pickle("output\profile_spec_test_a4_a5_22_05_26_2013_55")
profile = ds.load_pickle("output\profile_spec_epiphany_22_05_26_2051_53")
if not ret.success(profile):
    print("Invalid profile")
    quit()
profile = profile[0:800,:]

new_stencil = False
stencil_file = "{p}spec_stencil_soul".format(p=const.OUT_PATH)

if new_stencil:
    print("Starting stencil generation at: " + txt.time_str(util.now()))
    stencil = SpecStencil(profile)
    ds.dump_pickle(stencil, stencil_file)
else:
    stencil = ds.load_pickle(stencil_file)
if not ret.success(stencil):
    print("Invalid stencil")
    quit()

new_color_path = False
cp_points = [
    [4, 28, 134],
    [85, 100, 170],
    [114, 204, 244],
    [249, 160, 6],
    [240, 233, 57],
    [255, 255, 255]
]

cp_file = "{p}epiphany_cp".format(p=const.OUT_PATH)
if new_color_path:
    print("Starting color_path generation at: " + txt.time_str(util.now()))
    color_path = ColorPath()
    base_note = 55
    for c in cp_points:
        color_path.add_point(base_note, c[0], c[1], c[2])
        base_note *= 2
    ds.dump_pickle(color_path, cp_file)
else:
    color_path = ds.load_pickle(cp_file)
if not ret.success(color_path):
    print("Invalid color_path")
    quit()

if 0:
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

if 1:
    parr = PixelArray(1000 * const.GOLDEN, 1000)
    x0 = 500
    y0 = 800
    r0 = 20
    r1 = 1100
    theta0 = 10 / 12 * math.pi
    theta1 = 16 / 12 * math.pi
    thetaw = 14 / 12 * math.pi
    k_shift = 20
    rpe = RadialParElipses(parr, x0, y0, r0, r1, theta0, theta1, thetaw, k_shift)
    print("Starting canvas generation at: " + txt.time_str(util.now()))
    rpe.draw_canvas(stencil.stencil, color_path)
    rpe.draw_guidelines()
    print("Canvas generated at: " + txt.time_str(util.now()) + ", now drawing ...")
    parr.show()

print("Canvas rendered at: " + txt.time_str(util.now()))
render_time = util.now() - start_time
print("Total render time: " + txt.delta_str(render_time))