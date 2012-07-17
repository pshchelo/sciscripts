#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

def load_trajs(fname):
    """Loads trajectories from MOSAIC table and calculates momentary speeds.
    
    Returns trajectories list, where each trajectory is 3D array in the form
    [point, pos or vel, x or y].
    
    """    

    with open(fname) as f:
        lines = f.readlines()
        
#    head = lines[0].split()
    rawdata = [line.split() for line in lines[1:]]
    
#    ntracks = max([int(item[1]) for item in rawdata])
    
    datadict = {}
    
    for item in rawdata:
        ntrack = int(item[1])
        l = datadict.get(ntrack, [])
        l.append((item[4], item[3]))
        datadict[ntrack] = l
        
    tracks = [np.asarray(datadict[key], dtype=float).T for key in sorted(datadict.keys())]
    
    speeds = [np.column_stack((np.diff(track), np.asarray((np.NaN, np.NaN)))) for track in tracks]

    trajs = [np.hstack((tracks[i].T, speeds[i].T)) for i in range(len(tracks))]
    
    trajs = [traj.reshape(len(traj),2,2) for traj in trajs]
    
    return trajs
    
def filter_trajs_by_length(trajs, minlength):
    outtrajs = []
    for traj in trajs:
        if len(traj) >= minlength:
            outtrajs.append(traj)
    return outtrajs

def plot_trajs(trajs):
    """Plots trajectories as path and arrow field of corresponding speeds."""
    for traj in trajs:
        plt.plot(traj[:,0,0], traj[:,0,1])
        plt.quiver(traj[:,0,0], traj[:,0,1], traj[:,1,0], traj[:,1,1])
    plt.axis('equal')

def mean_speeds(trajs):
    avervel = []
    averx = []
    for traj in trajs:
        aver = traj[:-1].mean(0)
        avervel.append(aver[1])
        averx.append(aver[0,1])
    return np.asarray(averx), np.asarray(avervel)

if __name__=='__main__':
    import sys

    if len(sys.argv) >1:
        fname = sys.argv[1]
    else:
        fname = 'mosaic.txt'

    trajs = load_tracks(fname)

    plt.figure(1)
    minlength = 30
    plot_trajs(filter_trajs_by_length(trajs, minlength))
    plt.show()    