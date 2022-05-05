import librosa
import numpy as np

import util.const as const
import util.util as util

# 1. Get the file path to an included audio example
#filename = librosa.example('nutcracker')
filename = const.MUSIC_PATH + "epiphany.wav"

# 2. Load the audio as a waveform `y`
#    Store the sampling rate as `sr`    
y, sr = librosa.load(filename, duration=10, offset=10)
print("\nSR: {s} Y Length: {y}".format(s=sr, y=len(y)))

'''
# 3. Run the default beat tracker
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
print("\nBeat Frames: Length: {l} Arr:".format(l=len(beat_frames)))
print(beat_frames)

print('\nEstimated tempo: {:.2f} beats per minute'.format(tempo))

# 4. Convert the frame indices of beat events into timestamps
beat_times = librosa.frames_to_time(beat_frames, sr=sr)
print("\nBeat Times: Length: {l} Arr:".format(l=len(beat_times)))
print(beat_times)

print("\nWriting csv of beat times ...")
csv_str = "b\n"
for b in beat_times:
    csv_str += str(b) + "\n"
util.file(csv_str, const.OUT_PATH + "beat_arr.csv")
'''

# Set the hop length; at 22050 Hz, 512 samples ~= 23ms
hop_length = 512

# Separate harmonics and percussives into two waveforms
y_harmonic, y_percussive = librosa.effects.hpss(y)

# Beat track on the percussive signal
tempo, beat_frames = librosa.beat.beat_track(y=y_percussive,
                                             sr=sr)

# Compute MFCC features from the raw signal
mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop_length, n_mfcc=13)

# And the first-order differences (delta features)
mfcc_delta = librosa.feature.delta(mfcc)

# Stack and synchronize between beat events
# This time, we'll use the mean value (default) instead of median
beat_mfcc_delta = librosa.util.sync(np.vstack([mfcc, mfcc_delta]),
                                    beat_frames)

# Compute chroma features from the harmonic signal
chromagram = librosa.feature.chroma_cqt(y=y_harmonic,
                                        sr=sr)

# Aggregate chroma features between beat events
# We'll use the median value of each feature between beat frames
beat_chroma = librosa.util.sync(chromagram,
                                beat_frames,
                                aggregate=np.median)

# Finally, stack all beat-synchronous features together
beat_features = np.vstack([beat_chroma, beat_mfcc_delta])

#ya, ya, i'll make a bloody class later, ok?
print("\nWriting csv of chromagram ...")
csv_str = "c,db,d,eb,e,f,gb,g,ab,a,bb,b"
columns = []
for c in chromagram:
    columns.append(c)
for i in range(len(columns[0])):
    csv_str += "\n"
    for c in columns:
        csv_str += "{n:>.5f},".format(n=c[i])
    csv_str = csv_str.rstrip(",")
util.file(csv_str, const.OUT_PATH + "chromagram_10.csv")