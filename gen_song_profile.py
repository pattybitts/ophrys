from obj.Transcriber import Transcriber

import util.const as const

input_file = const.MUSIC_PATH + "epiphany.wav"
output_dest = const.OUT_PATH

trans = Transcriber(input_file, output_dest, 10)
trans.transcribe()