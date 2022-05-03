import datetime

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