from obj.Transcriber import Transcriber

import util.const as const
import util.txt as txt
import util.util as util

in_str = "test_a4_a5"

input_file = const.IN_PATH + in_str + ".wav"
output_dest = const.OUT_PATH

trans = Transcriber(input_file, output_dest, 10)
#trans.transcribe_stft()
#trans.transcribe_spectogram()
trans.transcribe_chromagram()
trans.save_csv(name=in_str)
trans.save_profile(name=in_str)
plot_save_path = "{p}chroma_{n}_{d}.png".format(p=const.IMG_SAVE, n=in_str, d=txt.date_file_str(util.now()))
trans.plot(plot_save_path)