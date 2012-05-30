"""Rename recovered TIF fluctuation images files

Files are renamed according to their name, guessing the date
and the experiment number for easier storing and comparison with back up copy.

"""
import os
from glob import iglob


globpatterns = {
'year': '20[0-1][0-9]',
'month': '[0-1][0-9]',
'day': '[0-3][0-9]',
}

# for my fluctuation image files with all-numeric, no-dashes ets names
PATTERN = '%(year)s%(month)s%(day)s[0-3][0-9][0-9][0-9][0-9][0-9][0-9][0-9].tif'%globpatterns

fnames = iglob(PATTERN)
for f in fnames:
	dir1 = '-'.join((f[:4], f[4:6], f[6:8]))
	dir2=f[8:10]
	dest = os.path.join(dir1, dir2, f)
	os.renames(f, dest)
