import librosa, librosa.display
import numpy as np
import matplotlib.pyplot as plt

import util.const as const
import util.ds as ds

filename = const.OUT_PATH + "profile_spec_test_a4_a5_22_05_23_0908_15"
#filename = const.OUT_PATH + "profile_spec_epiphany_22_05_23_0904_55"

profile = ds.load_pickle(filename)

short_profile = profile[:, 0:1000]

librosa.display.specshow(short_profile, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.show()