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
ELP = 500
EDR = math.pi / 1000

#for rgu color scaling
R_RANGE = [0, .5]
G_RANGE = [0, .7]
U_RANGE = [0, 1]

#Spectrogram interpretation
FREQ_INC = 22050 / 8192

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

#imported time constants
TZ = pytz.UTC
LTZ = pytz.timezone('US/Eastern')
LTZ_OFFSET = -5

#datetime formatting
MONTHS = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, \
    "Jul": 7, "Aug": 8, "Sep": 9, "Dec": 10, "Nov": 11, "Dec": 12}
SHORT_DATE = "%y_%m_%d"
DATE_FORMAT = "%d-%b-%y %H:%M:%S"
TIME_FORMAT = "%H:%M:%S"
DATE_FILE_FORMAT = "%y_%m_%d_%H%M_%S"
TD_DATE_FORMAT = "%Y-%m-%d"