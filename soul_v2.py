import math, numpy as np

import util.const as const
import util.util as util
import util.ds as ds
import util.ret as ret
import util.txt as txt
import util.calc as calc

from obj.PixelArray import PixelArray
from obj.SpecStencil import SpecStencil
from obj.ColorPath import ColorPath
from obj.TestDisplay import TestDisplay
from obj.RadialParElipses import RadialParElipses
from obj.ColorMap import ColorMap
from obj.Pixel import Pixel

new_stencil = False
draw_spec = True
draw_canvas = False

#lets clean up this initialization so that we're only using it when we need it
start_time = util.now()
print("Intializing at: " + txt.time_str(util.now()))
if new_stencil or draw_spec:
    print("Loading profile at: " + txt.time_str(util.now()))
    #profile = ds.load_pickle("output\profile_spec_test_a4_a5_22_05_26_2013_55")
    profile = ds.load_pickle("output\profile_spec_epiphany_22_05_26_2051_53")
    if not ret.success(profile):
        print("Invalid profile")
        quit()
    profile = profile[0:800,:]

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
print("Stencil Frames: " + str(len(stencil.stencil)))

layer_0 = {
    'start': 3,
    'end': 38,
    'path': [
        [0, Pixel(0x04, 0x2c, 0x86)],   #4, 44, 134
        [3.66, Pixel(0x55, 0x64, 0xaa)], #85, 100, 170
        [7.33, Pixel(0x91, 0x92, 0xbf)], #145, 146, 191
        [11, Pixel(0x7c, 0xcc, 0xf4)] #124, 204, 244
    ]
}
#NOTE I made some changes here to try to clarify my saturation questions
layer_1 = {
    'start': 39,
    'end': 62,
    'path': [
        [0, Pixel(0x40, 0xa0, 0x06)], #249, 160, 6
        [11, Pixel(0x40, 0xe4, 0x34)] #238, 228, 52
    ]
}
color_map = ColorMap([layer_0, layer_1])

if draw_spec:
    x, y  = profile.shape
    parr = PixelArray(x, y)
    td = TestDisplay(parr, np.amin(profile), np.amax(profile))
    print("Starting visual spec generation at: " + txt.time_str(util.now()))
    #td.draw_array(profile)
    #td.heat_overlay(profile)
    #td.peak_overlay(profile)
    #td.octave_overlay(profile)
    #td.note_overlay(profile)
    #td.com_overlay(stencil.stencil)
    td.color_overlay(stencil.stencil, color_map.map)
    print("Spec generated at: " + txt.time_str(util.now()) + ", now drawing ...")
    parr.show()

if draw_canvas:
    parr = PixelArray(1000 * const.GOLDEN, 1000)
    x0 = 500
    y0 = 800
    r0 = 20
    r1 = 700
    k_shift = 20
    #color_path_0
    itheta0 = 10 / 12 * math.pi
    curve0 = 3 / 12 * math.pi
    width0 = 14 / 12 * math.pi
    #color_path_1
    itheta1 = 14 / 12 * math.pi
    curve1 = 3 / 12 * math.pi
    width1 = 6 / 12 * math.pi

    print("Starting canvas generation at: " + txt.time_str(util.now()))
    rpe0 = RadialParElipses(x0, y0, r0, r1, itheta0, curve0, width0, k_shift)
    rpe1 = RadialParElipses(x0, y0, r0, r1, itheta1, curve1, width1, k_shift)
    #parr = RadialParElipses.draw_canvas(parr, stencil.stencil, [[cp0, rpe0], [cp1, rpe1]])
    #parr = RadialParElipses.draw_canvas(parr, stencil.stencil, [[cp0, rpe0]])
    parr = rpe0.draw_guidelines(parr)
    #parr = rpe1.draw_guidelines(parr)
    print("Canvas generated at: " + txt.time_str(util.now()) + ", now drawing ...")
    parr.show()

print("Canvas rendered at: " + txt.time_str(util.now()))
render_time = util.now() - start_time
print("Total render time: " + txt.delta_str(render_time))