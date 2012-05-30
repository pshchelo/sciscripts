"""Renames fluctuation analysis image files saved with wrong year in their name."""
import glob
import os

iterfilenames = glob.iglob('*/20070730*.*')

for filename in iterfilenames:
    dir, name = os.path.split(filename)
    newname = name.replace('7','9', 1)
    newfilename = os.path.join(dir, newname)
    os.rename(filename, newfilename)
