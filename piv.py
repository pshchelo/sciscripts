#!/usr/bin/env python
"""Analyze particle trajectories for determination of channel speed profile.

The (lamilar) flow is supposed to be along Y direction

Approximate workflow:
    load_trajs(fname) - load 'Results...txt' file saved by MOSAIC
    filter_trajs_by_dir(trajs) - remove back- and sidesteps
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
    rawdata = [line.split() for line in lines[1:]]   
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
    
def filter_trajs_by_backsteps(trajs):
    """Removes trajectoreis with backward steps"""
    return [traj for traj in trajs if not check_backstep(traj)]

def check_backstep(traj):
    """Check that all steps are in one Y direction"""
    velsy = traj[:-1,1,1]  # first :-1 due to last element being NaN
    return not (np.all(velsy >= 0) or np.all(velsy <=0))
    
def filter_trajs_by_sidesteps(trajs):
    """Removes trajectories with sidesteps"""
    return [traj for traj in trajs if not check_sidestep_hard(traj)]
#    return [traj for traj in trajs if not check_sidestep_soft(traj)]

def check_sidestep_hard(traj):
    """Returns True if maximal absolute X speed is bigger than minimal Y speed.

    This is quite hard restriction, applying to the whole trajectory.    

    """
    velsx = traj[:-1,1,0]  # first :-1 are due to last element being NaN
    velsy = traj[:-1,1,1]
    return np.max(np.fabs(velsx)) > np.min(np.fabs(velsy))

def check_sidestep_soft(traj):
    """Returns True if for any step deviation in X is bigger than deviation in Y.

    This restriction is softer, applying to individual steps only.
    
    """
    velsx = traj[:-1,1,0]  # first :-1 are due to last element being NaN
    velsy = traj[:-1,1,1]
    return np.any(np.abs(velsx)>=np.abs(velsy)) 

def filter_trajs_by_dir(trajs):
    """Removes trajectories with either side- or backsteps."""
    return filter_trajs_by_sidesteps(filter_trajs_by_backsteps(trajs))
    
def filter_trajs_by_deltaY(trajs, mindeltaY):
    """Removes trajectories displaced along Y shorter than mindeltaY."""
    return [traj for traj in trajs if np.abs(traj[0,0,1]-traj[-1,0,1]) >= mindeltaY]

def plot_trajs(trajs, title=None):
    """Plots trajectories as path and arrow field of corresponding speeds."""
    plt.figure(title)
    for traj in trajs:
        plt.plot(traj[:,0,0], traj[:,0,1])
        plt.quiver(traj[:,0,0], traj[:,0,1], traj[:,1,0], traj[:,1,1], 
                   units="dots", width=2)
    plt.axis('equal')

def mean_speeds(trajs):
    """Returns average X position and average X and Y velocities for each trajectory."""
    avervel = []
    stdvels = []
    averx = []
    for traj in trajs:
        aver = traj[:-1].mean(0)
        stdvel = traj[:-1].std(0)
        avervel.append(aver[1])
        averx.append(aver[0,1])
        stdvels.append(stdvel[1])
    return np.asarray(averx), np.asarray(avervel), np.asarray(stdvels)

def total_mean_speeds(avervel, stdvels):
    """Returns mean X and Y velocities (and their STD) averaged between trajectories.
    
    If there is only one trajectory, return the STD of Y velocity for this one trajectory.
    
    """
    velx = avervel[:, 0]
    vely = avervel[:, 1]
    stdvely = stdvels[:, 1]
    if len(vely) == 1:
        velystd = stdvely[0]
    else:
        velystd = np.std(vely)
    return (np.mean(velx), np.std(velx)), (np.mean(vely), velystd)
    
def meanvels(trajs):
    """Convenience function, combinig mean_speeds() and total_mean_speeds()"""
    averx, avervel, stdvels = mean_speeds(trajs)
    return total_mean_speeds(avervel, stdvels)
    
def optimal_length(trajs, minnum):
    """Returns optimal minimal length for trajectories to minimize STD of Y velocity."""
    lengths = [len(traj) for traj in trajs]
    maxlength = max(lengths)    
    lrange = range(2, maxlength+1)
    velystd = []
    for l in lrange:
        trajs_f = filter_trajs_by_length(trajs, l)
        if len(trajs_f) >= minnum:
            velystd.append(meanvels(trajs_f)[1][1])
        else:
            velystd.append(np.infty)
    return lrange[np.argmin(velystd)]
    
def process_one(fname, minnum, mindeltaY, plot=False, disp=False):
    trajs = load_trajs(fname)
    trajs_f = filter_trajs_by_dir(trajs)
    trajs_l = filter_trajs_by_deltaY(trajs_f, mindeltaY)
    if len(trajs_l) > minnum:
        l = optimal_length(trajs_l, minnum)
        trajs_ff = filter_trajs_by_length(trajs_l, l)
    else:
        l = len(trajs_l)
        trajs_ff = trajs_l
    vels = meanvels(trajs_ff)
    if plot:
        plot_trajs(trajs_ff, title='%s - %i trajs, minL=%i'%(fname, len(trajs_ff), l))
    if disp:
        print "number of trajectories:", len(trajs_ff)
        print "average X speed: %f +- %f"%(vels[0])
    return l, vels[1]

def process_all(fnames, minnum, mindeltaY, plot=False, disp=False):
    output = []
    for fname in fnames:
        l, velsy = process_one(fname, minnum, mindeltaY, plot=plot, disp=disp)
        output.append(velsy)
    output = np.abs(np.asarray(output))
    return output.T

if __name__=='__main__':
    print __doc__
