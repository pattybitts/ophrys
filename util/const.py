import math, pytz

IMG_SAVE = "C:\\Users\\patbi\\OneDrive\\Documents\\2022\\ophrys\\image_files\\"
OUT_PATH = "C:\\Users\\patbi\\OneDrive\\Git\\python_projects\\ophrys\\output\\"

#librosa
IN_PATH = "C:\\Users\\patbi\\OneDrive\\Git\\python_projects\\ophrys\\input\\"
SAMPLE_RATE = 10000
HOP_LENGTH = 10

GOLDEN = 1.618
#note i needed 50/5000 for a full render
DX_ST = 1
DR_ST = 2 * math.pi / 2500

TEST_PER = 5
TEST_SET = []
for i in range(100):
    pitch = i%TEST_PER
    amp = i
    TEST_SET.append([pitch, amp])

#time values, formatting
TZ = pytz.UTC
LTZ = pytz.timezone('US/Eastern')
LTZ_OFFSET = -5

DATE_FILE_FORMAT = "%y_%m_%d_%H%M_%S"