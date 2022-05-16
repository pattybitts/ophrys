import math, pytz

IMG_SAVE = "C:\\Users\\patbi\\OneDrive\\Documents\\2022\\ophrys\\image_files\\"
OUT_PATH = "C:\\Users\\patbi\\OneDrive\\Git\\python_projects\\ophrys\\output\\"

#librosa
IN_PATH = "C:\\Users\\patbi\\OneDrive\\Git\\python_projects\\ophrys\\input\\"

GOLDEN = 1.618
#detailed zone
D_START = 5 * math.pi / 4
DLP = 15000
DDR = 2 * math.pi / 6000
#loose zone
L_START = 6 * math.pi / 4
LLP = 15000
LDR = 2 * math.pi / 6000

#elipse drawing constants
#1000/1000 gives a decent profile in ~6s
ELP = 1000
EDR = math.pi / 10000
EW = 1

#for rgu color scaling
R_RANGE = [0, .5]
G_RANGE = [0, .7]
U_RANGE = [0, 1]

#time values, formatting
TZ = pytz.UTC
LTZ = pytz.timezone('US/Eastern')
LTZ_OFFSET = -5

DATE_FILE_FORMAT = "%y_%m_%d_%H%M_%S"

#when using test profile (deprecated)
TEST_PER = 5
TEST_SET = []
for i in range(100):
    pitch = i%TEST_PER
    amp = i
    TEST_SET.append([pitch, amp])