import librosa, librosa.display
import numpy as np
import matplotlib.pyplot as plt

import util.const as const
import util.ds as ds
import util.util as util
import util.txt as txt
import util.ret as ret

class Transcriber():

    def __init__(self, in_file, out_dest, t_inc, t_res=None, f_res=None):
        self.in_file = in_file
        self.out_dest = out_dest
        self.t_inc = t_inc
        self.t_res = t_res
        self.f_res = f_res
        self.song_dur_s = self.get_song_length()
        self.profile = None
        print("Created Transcriber Object. Song Length: " + str(self.song_dur_s))

    def get_song_length(self):
        y, sr = librosa.load(self.in_file, sr=1000)
        return len(y)/sr

    def transcribe_chromagram(self):
        offset = 0
        full_spec = np.ndarray((12, 0))
        while offset < self.song_dur_s:
            y, sr = librosa.load(self.in_file, offset=offset, duration=self.t_inc)
            y_harmonic, y_percussive = librosa.effects.hpss(y)
            chromagram = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr)
            full_spec = np.concatenate((full_spec, chromagram), 1)
            print("\nAdded: {cl} lines to full chromagram.".format(cl=len(chromagram[0])))
            print("Offset: " + str(offset))
            offset += self.t_inc
        self.profile = full_spec

    def transcribe_stft(self):
        offset = 0
        full_spec = np.ndarray((1025, 0))
        while offset < self.song_dur_s:
            y, sr = librosa.load(self.in_file, offset=offset, duration=self.t_inc)
            spec = np.abs(librosa.stft(y))
            full_spec = np.concatenate((full_spec, spec), 1)
            print("\nAdded: {cl} lines to full spectrogram.".format(cl=len(spec[0])))
            print("Offset: " + str(offset))
            offset += self.t_inc
        #trimming here if necessary
        full_spec = librosa.power_to_db(full_spec, ref=np.max)
        self.profile = full_spec

    def transcribe_spectogram(self):
        offset = 0
        full_spec = np.ndarray((108, 0))
        while offset < self.song_dur_s:
            y, sr = librosa.load(self.in_file, offset=offset, duration=self.t_inc)
            spec = librosa.feature.melspectrogram(y, sr=sr, n_mels=108, fmin=15.8846, fmax=8133.68)
            full_spec = np.concatenate((full_spec, spec), 1)
            print("\nAdded: {cl} lines to full spectrogram.".format(cl=len(spec[0])))
            print("Offset: " + str(offset))
            offset += self.t_inc
        #trimming here if necessary
        full_spec = librosa.power_to_db(full_spec, ref=np.max)
        self.profile = full_spec

    def plot(self, save_path=None):
        librosa.display.specshow(self.profile, x_axis='time', y_axis='hz')
        plt.colorbar(format='%+2.0f dB')
        if save_path: plt.savefig(save_path, format='png')
        plt.show()

    def save_profile(self, name=""):
        filepath = "{p}profile_{n}_{d}".format(p=const.OUT_PATH, n=name, d=txt.date_file_str(util.now()))
        print("Attempting to dump pickle at: " + filepath)
        ds.dump_pickle(self.profile, filepath)

    def save_csv(self, name=""):
        csv_path = "{p}profile_csv_{n}_{d}.csv".format(p=const.OUT_PATH, n=name, d=txt.date_file_str(util.now()))
        print("Attempting to convert to csv at: " + csv_path)
        util.file(util.nparr_to_csv(self.profile), csv_path)