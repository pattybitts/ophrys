import pickle

import util.ret as ret

def dump_pickle(object, filename):
    pfile = open(filename, 'wb')
    pickle.dump(object, pfile, pickle.DEFAULT_PROTOCOL)
    pfile.close()

def load_pickle(filename):
    try:
        pfile = open(filename, 'rb')
        object = pickle.load(pfile)
        pfile.close()
        return object
    except:
        return ret.ERROR