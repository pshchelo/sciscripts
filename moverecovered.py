import os
import glob

fnames = glob.iglob("*.tif")
j=0
print "Start renaming..."
for f in fnames:
    dest = os.path.join('m:/recovery/images/tif', f)
    os.renames(f, dest)
    j += 1
    if j%100==0:
        print "%i files moved..."%j
print "Finished."