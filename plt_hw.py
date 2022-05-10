import librosa, librosa.display
import numpy as np
import matplotlib.pyplot as plt

import util.const as const
import util.ds as ds

filename = const.OUT_PATH + "melspec_test_notes_22_05_10_0901_34"

profile = ds.load_pickle(filename)

sm = plt.cm.ScalarMappable()

librosa.display.specshow(profile, x_axis='time', y_axis='mel')
plt.colorbar(format='%+2.0f dB')
plt.show()