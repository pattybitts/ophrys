import librosa, numpy as np

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
        print("Created Transcriber Object. Song Length: " + str(self.song_dur_s))

    def get_song_length(self):
        y, sr = librosa.load(self.in_file, sr=1000)
        return len(y)/sr

    def transcribe_chromagram(self):
        offset = 0
        full_chromagram = []
        while offset < self.song_dur_s:
            y, sr = librosa.load(self.in_file, offset=offset, duration=self.t_inc)
            y_harmonic, y_percussive = librosa.effects.hpss(y)
            chromagram = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr)
            for i in range(len(chromagram[0])):
                point = []
                for c in chromagram:
                    point.append(c[i])
                full_chromagram.append(point)
            print("\nAdded: {cl} lines to full chromagram. : {fl}".format(cl=len(chromagram[0]), fl=len(full_chromagram)))
            print("Offset: " + str(offset))
            offset += self.t_inc
        filename = const.OUT_PATH + "chromagram_" + txt.date_file_str(util.now())
        print("Attempting to dump pickle at: " + filename)
        ds.dump_pickle(full_chromagram, filename)

    def transcribe_spectogram(self, name=""):
        offset = 0
        full_spec = np.ndarray((108, 0))
        while offset < self.song_dur_s:
            y, sr = librosa.load(self.in_file, offset=offset, duration=self.t_inc)
            spec = librosa.feature.melspectrogram(y, sr=sr, n_mels=108, fmin=15.8846, fmax=8133.68)
            db_spec = librosa.power_to_db(spec, ref=np.max)
            full_spec = np.concatenate((full_spec, db_spec), 1)
            #for i in range(len(db_spec[0])):
            #    point = []
            #    for s in db_spec:
            #        point.append(s[i])
            #    full_spec.append(point)
            print("\nAdded: {cl} lines to full spectrogram.".format(cl=len(db_spec[0])))
            print("Offset: " + str(offset))
            offset += self.t_inc
        filepath = "{p}melspec_{n}_{d}".format(p=const.OUT_PATH, n=name, d=txt.date_file_str(util.now()))
        print("Attempting to dump pickle at: " + filepath)
        ds.dump_pickle(full_spec, filepath)
        csv_path = "{p}profile_csv_{n}_{d}.csv".format(p=const.OUT_PATH, n=name, d=txt.date_file_str(util.now()))
        print("Attempting to convert to csv at: " + csv_path)
        util.file(util.nparr_to_csv(full_spec), csv_path)