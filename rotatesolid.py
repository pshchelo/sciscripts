#!/usr/bin/env python
from __future__ import division
import numpy as np 

def volume_trapz_rotx(y, x):
    """Calculate vulume of body of rotation around X-axis.

    Subsequent points can have the same x-coordinate,
    in this case the volume between them would be NaN
    due to 0-devision, but then NaN is substituted for 0,
    making no contribution to the integral.
    
    """
    dx = np.diff(x)
    dy = np.diff(y)
    x = x[:-1]
    y = y[:-1]
    k = dy/dx # in case of vertically aligned points
    b = y - x*k
    # integrated square of the radius of revolution for trapezoid
    r2integrated = lambda t: k*k*t*t*t/3 + k*b*t*t + b*b*t
    dv = np.pi*(r2integrated(x+dx)-r2integrated(x))
    dv = np.nan_to_num(dv)
    return np.sum(dv)

def volume_concave(bodyy, bodyx, cavityy, cavityx):
    return volume_trapz_rotx(bodyy, bodyx) - volume_trapz_rotx(cavityy, cavityx)
def contour(img, seed):
    """Returns correctly ordered contour made by non-zero elements of the image.

    img is binary image as ``ndarray`` read by ``imread``
    seed is a starting coordinate as tuple ``(y,x)``

    img has to be cleared so that each point of the contour has exactly 2
    neighbours in 8 directions, i.e. the contour is a line of 1 pixel width

    """
    line = [seed]
    shifts_CW = np.asarray(
        ((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)))
    neighbours = [tuple(np.asarray(seed) + shift) for shift in shifts_CW]
    for neighbour in neighbours:
        if img[neighbour]:
            current = neighbour
            line.append(current)
            break
    nofpoints = len(np.nonzero(img)[0])
    for _i in range(nofpoints - 2):
        neighbours = [tuple(np.asarray(current) + shift) for shift in shifts_CW]
        for neighbour in neighbours:
            if img[neighbour] and neighbour != line[-2]:
                current = neighbour
                line.append(current)
                break
    if len(line) != nofpoints:
        return None
    else:
        return np.asarray(line)
