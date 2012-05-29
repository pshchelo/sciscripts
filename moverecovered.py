import os
import sys
import glob

ext = sys.argv[1]
fnames = glob.iglob("*.%s"%ext)
j=0
print "Start renaming..."
for f in fnames:
    dest = os.path.join('../recovery/%s'%ext, f)
    os.renames(f, dest)
    j += 1
    if j%100==0:
        print "%i files moved..."%j
print "Finished."