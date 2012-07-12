import sys
import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv) >1:
    fname = sys.argv[1]
else:
    fname = 'mosaic.txt'
with open(fname) as f:
    lines = f.readlines()
    
head = lines[0].split()
rawdata = [line.split() for line in lines[1:]]

ntracks = max([int(item[1]) for item in rawdata])

datadict = {}

for item in rawdata:
    ntrack = int(item[1])
    l = datadict.get(ntrack, [])
    l.append((item[4], item[3]))
    datadict[ntrack] = l
    
tracks = [np.asarray(datadict[key], dtype=float).T for key in sorted(datadict.keys())]

speeds = [np.column_stack((np.diff(track), np.asarray((np.NaN, np.NaN)))) for track in tracks]

filtertracks = 20
plt.figure(1)
for i in range(len(tracks)):
    track = tracks[i]
    speed = speeds[i]
    if track.shape[1] > filtertracks:
        plt.plot(track[0], track[1])
        plt.quiver(track[0], track[1], *speed)

plt.axis('equal')

plt.show()