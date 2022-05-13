from obj.Transcriber import Transcriber

import util.const as const
import util.txt as txt
import util.util as util

in_str = "epiphany"
profile_type = "chroma" #chroma, spec, melspec

input_file = const.IN_PATH + in_str + ".wav"
output_dest = const.OUT_PATH

trans = Transcriber(input_file, output_dest, 10)
if profile_type == "chroma": trans.transcribe_chromagram()
if profile_type == "spec": trans.transcribe_stft()
if profile_type == "melspec": trans.transcribe_spectogram()
save_name = "{n}_{f}".format(n=profile_type, f=in_str)
#trans.save_csv(name=save_name)
trans.save_profile(name=save_name)
plot_save_path = "{p}{n}_{d}.png".format(p=const.IMG_SAVE, n=save_name, d=txt.date_file_str(util.now()))
trans.plot(plot_save_path)