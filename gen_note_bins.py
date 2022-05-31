import util.ds as ds

A1_REF = 27.5
note = A1_REF

note_bins = []
#octaves
for i in range(0, 8):
    #notes
    for j in range(0, 12):
        note_bins.append(note)
        note *= 2 ** (1/12)

#for n in note_bins:
#    print("{n:>.2f}".format(n=n))

ds.dump_pickle(note_bins, "input\\note_bins")