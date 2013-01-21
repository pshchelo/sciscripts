#!/usr/bin/env python
from __future__ import division
import numpy as np 

def volume_trapz_rotx(y, x):
    """Volume of solid of rotation around X-axis.
    
    """
    dx = np.diff(x)
    dy = np.diff(y)
    x = x[:-1]
    y = y[:-1]
    # taking each slice as a truncated cone with radii y and y+dy and height dx
    dV = np.pi/3 * np.abs(dx) * (y**2 + (y+dy)**2 + y*(y+dy))
    return sum(dV)

def surface_trapz_rotx(y, x):
    """Surface of solid of rotation around X axis.

    """
    dx = np.diff(x)
    dy = np.diff(y)
    x = x[:-1]
    y = y[:-1]
    # taking each slice as a truncated cone with radii y and y+dy and height dx
    dS = np.pi * (2*y+dy) * np.sqrt(dx**2 + dy**2)
    return sum(dS)

def volume_concave(contoury, contourx):
    """Volume of a body of rotation with a cavity at the left side of X"""
    border = np.argmin(contourx)
    cavityx = contourx[:border+1]
    cavityy = contoury[:border+1]
    bodyx = contourx[border:]
    bodyy = contoury[border:]
    return volume_trapz_rotx(bodyy, bodyx) - volume_trapz_rotx(cavityy, cavityx)

def contour(img, seed):
    """Returns correctly ordered contour made by non-zero elements of the image.

    img is binary image as ``ndarray`` read by ``imread``
    seed is a starting coordinate as tuple ``(y,x)``

    img has to be cleared so that each point of the contour has exactly 2
    neighbours in 8 directions, i.e. the contour is a line of 1 pixel width

    """
    line = [seed]
    shifts_CCW = np.asarray(
        ((1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)))
    neighbours = [tuple(np.asarray(seed) + shift) for shift in shifts_CCW]
    for neighbour in neighbours:
        if img[neighbour]:
            current = neighbour
            line.append(current)
            break
    nofpoints = len(np.nonzero(img)[0])
    for _i in range(nofpoints - 2):
        neighbours = [tuple(np.asarray(current) + shift) 
                        for shift in shifts_CCW]
        for neighbour in neighbours:
            if img[neighbour] and neighbour != line[-2]:
                current = neighbour
                line.append(current)
                break
    if len(line) != nofpoints:
        return None
    else:
        return np.asarray(line)
