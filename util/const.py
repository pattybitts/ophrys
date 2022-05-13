import math, pytz

IMG_SAVE = "C:\\Users\\patbi\\OneDrive\\Documents\\2022\\ophrys\\image_files\\"
OUT_PATH = "C:\\Users\\patbi\\OneDrive\\Git\\python_projects\\ophrys\\output\\"

#librosa
IN_PATH = "C:\\Users\\patbi\\OneDrive\\Git\\python_projects\\ophrys\\input\\"

GOLDEN = 1.618
#detailed zone
D_START = 5 * math.pi / 4
DLP = 10000
DDR = 2 * math.pi / 4000
#loose zone
L_START = 6 * math.pi / 4
LLP = 100
LDR = 2 * math.pi / 200

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