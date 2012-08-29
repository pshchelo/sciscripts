#!/usr/bin/env python
"""Analyze particle trajectories for determination of channel speed profile.

Approximate workflow:
    load_trajs(fname) - load 'Results...txt' file saved by MOSAIC
    plot_trajs(filter_trajs_by_length(trajs, minL)) - decide how many 
        trajectories to keep
    meanvels(filter_trajs_by_length(trajs, minL)) - get mean X and Y velosities
        and their STDs
"""

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
    """Returns trajectories no shorter than minlength of points"""
    return [traj for traj in trajs if len(traj) >= minlength]
    
def filter_trajs_by_backward(trajs):
    return [traj for traj in trajs if not backstep_found(traj)]

def backstep_found(traj):
    """Check that all steps are in one Y direction"""
    velsy = traj[:-1,1,1]  # first :-1 due to last element being NaN
    return not (np.all(velsy >= 0) or np.all(velsy <=0))
    
def filter_trajs_by_sidesteps(trajs):
    return [traj for traj in trajs if not sidestep_found(traj)]

def sidestep_found(traj):
    """Returns True if maximal absolute X speed is bigger than minimal Y speed"""
    velsx = traj[:-1,1,0]  # first :-1 are due to last element being NaN
    velsy = traj[:-1,1,1]
    if np.max(np.fabs(velsx)) > np.min(np.fabs(velsy)):
        return True
    else:
        return False

def filter_trajs_by_dir(trajs):
    return [traj for traj in trajs if not (backstep_found(traj) or  
                                           sidestep_found(traj))]

def plot_trajs(trajs, **kwargs):
    """Plots trajectories as path and arrow field of corresponding speeds."""
    for traj in trajs:
        plt.plot(traj[:,0,0], traj[:,0,1])
        plt.quiver(traj[:,0,0], traj[:,0,1], traj[:,1,0], traj[:,1,1], 
                   units="dots", width=2)
    plt.axis('equal')

def mean_speeds(trajs):
    avervel = []
    averx = []
    for traj in trajs:
        aver = traj[:-1].mean(0)
        avervel.append(aver[1])
        averx.append(aver[0,1])
    return np.asarray(averx), np.asarray(avervel)
    
def total_mean_speeds(avervel):
    velx = avervel[:,0]
    vely = avervel[:,1]
    return (np.mean(velx), np.std(velx)), (np.mean(vely), np.std(vely))
    
def meanvels(trajs):
    averx, avervel = mean_speeds(trajs)
    return total_mean_speeds(avervel)
    
def optimal_set(trajs, startLcut):
    """"""
    return

if __name__=='__main__':
    import sys

    if len(sys.argv) >1:
        fname = sys.argv[1]
    else:
        fname = 'mosaic.txt'

    trajs = load_trajs(fname)

    plt.figure(1)
    minlength = 30
    plot_trajs(filter_trajs_by_length(trajs, minlength))
    plt.show()
