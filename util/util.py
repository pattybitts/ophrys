import datetime, numpy as np

import util.ret as ret

#our f_dst resolution (for now) is to handle all time objects as offset naive
def now():
    return datetime.datetime.now()

def file(variable, filename):
    try:
        output_str = str(variable)
        archive = open(filename, 'ab')
        archive.write(bytearray(output_str, 'utf-8'))
        archive.close()
        return ret.SUCCESS
    except:
        return ret.ERROR

def swap_axes(nparr):
    nparr = np.rot90(nparr)
    nparr = np.flip(nparr, 0)
    return nparr

def nparr_to_csv(arr):
    arr = swap_axes(arr)
    csv_str = ""
    for a1 in arr:
        for a2 in a1:
            csv_str += "{a:>7.3f},".format(a=a2)
        csv_str = csv_str.rstrip(",")
        csv_str += "\n"
    return csv_str