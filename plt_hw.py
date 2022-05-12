import librosa, librosa.display
import numpy as np
import matplotlib.pyplot as plt

import util.const as const
import util.ds as ds

#filename = const.OUT_PATH + "melspec_test_notes_22_05_10_1032_19"
filename = const.OUT_PATH + "melspec_soul_22_05_10_0826_55"

profile = ds.load_pickle(filename)

librosa.display.specshow(profile, x_axis='time', y_axis='mel')
plt.colorbar(format='%+2.0f dB')
plt.show()