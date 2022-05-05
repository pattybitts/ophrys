import util.const as const
import util.ds as ds
import util.util as util
import util.txt as txt

#ya, ya, i'll make a bloody class later, ok?
print("\nWriting csv of chromagram ...")

filename = const.OUT_PATH + "chromagram_22_05_05_1116_50"

chromagram = ds.load_pickle(filename)

csv_str = "c,db,d,eb,e,f,gb,g,ab,a,bb,b"
for c in chromagram:
    csv_str += "\n"
    for n in c:
        csv_str += str(n) + ","
    csv_str = csv_str.rstrip(",")
util.file(csv_str, const.OUT_PATH + "chromagram_csv_" + txt.date_file_str(util.now()))