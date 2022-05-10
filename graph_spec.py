from obj.Transcriber import Transcriber

import util.const as const

input_file = const.IN_PATH + "test_a4_a5.wav"
output_dest = const.OUT_PATH

trans = Transcriber(input_file, output_dest, 10)
trans.transcribe_spectogram("test_notes")