import librosa
import numpy as np

import util.const as const
import util.util as util

# 1. Get the file path to an included audio example
#filename = librosa.example('nutcracker')
filename = const.MUSIC_PATH + "epiphany.wav"

# 2. Load the audio as a waveform `y`
#    Store the sampling rate as `sr`    
y, sr = librosa.load(filename, duration=10)
print("\nSR: {s} Y Length: {y}".format(s=sr, y=len(y)))

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