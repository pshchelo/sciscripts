import os
from glob import iglob

fnames = iglob('20*.tif')

for f in fnames:
    dir1 = '-'.join((f[:4], f[4:6], f[6:8]))
    dir2=f[8:10]
    dest = os.path.join(dir1, dir2, f)
    os.renames(f, dest)