import os
from glob import iglob

fnames = iglob('20[0-1]*.tif')

for f in fnames:
    if f[:10].isdigit():
        dir1 = '-'.join((f[:4], f[4:6], f[6:8]))
        dir2=f[8:10]
        dest = os.path.join(dir1, dir2, f)
        os.renames(f, dest)