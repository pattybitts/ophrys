import util.const as const
import util.ds as ds
import util.util as util
import util.txt as txt

#ya, ya, i'll make a bloody class later, ok?
print("\nWriting csv of profile ...")

filename = const.OUT_PATH + "melspec_22_05_09_1016_19"

profile = ds.load_pickle(filename)

#csv_str = "c,db,d,eb,e,f,gb,g,ab,a,bb,b"
#csv_str = "goob"
for p in profile:
    csv_str += "\n"
    for n in p:
        csv_str += str(n) + ","
    csv_str = csv_str.rstrip(",")
util.file(csv_str, const.OUT_PATH + "profile_csv_" + txt.date_file_str(util.now()) + ".csv")