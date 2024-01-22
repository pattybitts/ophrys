import math, numpy as np

import util.util as util
import util.txt as txt
import util.ret as ret
import util.ds as ds
import util.const as const

from obj.NoteStencil import NoteStencil
from obj.PixelArray import PixelArray
from obj.TestDisplay import TestDisplay

#specify run parameters
new_stencil = False
draw_spec = True

profile_path = "output\profile_spec_epiphany_22_05_26_2051_53"
#profile_path = "output\profile_spec_test_a4_a5_22_05_26_2013_55"
#profile_path = "output\profile_chroma_epiphany_22_07_23_1133_22"
stencil_path = "{p}spec_note_stencil_soul".format(p=const.OUT_PATH)

custom_profile_w = 800 #cuts off high end frequency bins
custom_spec_x = 0
custom_spec_y = 400

#initialization, loading profile if we need one
start_time = util.now()
print("Intializing at: " + txt.time_str(util.now()))
if new_stencil or draw_spec:
    print("Loading profile at: " + txt.time_str(util.now()))
    profile = ds.load_pickle(profile_path)
    if not ret.success(profile):
        print("Invalid profile" + profile_path)
        quit()
    if custom_profile_w: profile = profile[0:custom_profile_w,:]

#loading/generating stencil
if new_stencil:
    print("Starting stencil generation at: " + txt.time_str(util.now()))
    stencil = NoteStencil(profile)
    ds.dump_pickle(stencil, stencil_path)
else:
    stencil = ds.load_pickle(stencil_path)
if not ret.success(stencil):
    print("Invalid stencil")
    quit()
print("Stencil Length: " + str(len(stencil.stencil)))

#skipping color stuff for now (may return) (likely refactored)

#drawing spectrogram (with filters/overlays)
if draw_spec:
    x, y = profile.shape
    if custom_spec_x: x = custom_spec_x
    if custom_spec_y: y = custom_spec_y
    parr = PixelArray(x, y)
    td = TestDisplay(parr, np.amin(profile), np.amax(profile))
    print("Starting visual spec generation at: " + txt.time_str(util.now()))
    #TestDisplay functions draw profiles and overlay filters in order listed
    td.draw_array(profile)
    #td.note_overlay(profile)
    #td.octave_overlay(profile)
    #td.note_stencil_overlay(stencil.stencil)
    print("Spec generated at: " + txt.time_str(util.now()) + ", now drawing ...")
    parr.show()

process_time = util.now() - start_time
print("Total process time: " + txt.delta_str(process_time))