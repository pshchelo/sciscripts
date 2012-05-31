"""Rename recovered TIF fluctuation images files

Files are renamed according to their name, guessing the date
and the experiment number for easier storing and comparison with back up copy.

"""
import os
from glob import iglob
import datetime


globpatterns = {
'year': '20[0-1][0-9]',
'month': '[0-1][0-9]',
'day': '[0-3][0-9]',
}

# for my fluctuation image files with all-numeric names with dashes
PATTERN = 'img[0-9][0-9][0-9][0-9][0-9][0-9]_*.tif'
fnames = iglob(PATTERN)
print "Starting rename..."

for f in fnames:
    mtstamp = os.path.getmtime(f)
    date = datetime.datetime.fromtimestamp(mtstamp)
    dir = str(date)[:10]
    basedir='../tiff'
    dest = os.path.join(basedir, dir, f)
    os.renames(f, dest)

print "Finished rename."
