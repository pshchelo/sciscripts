#!/usr/bin/env python
from __future__ import division
import numpy as np

def volume_trapz_rotx(y, x):
    """Volume of solid of rotation around X-axis.
    
    """
    dx = np.diff(x)
    y2 = np.roll(y, -1)[:-1]
    y1 = y[:-1]
    # taking each slice as a truncated cone with radii y and y+dy and height dx
    dV = np.pi/3 * dx * (y1**2 + y2**2 + y1*y2)
    return np.abs(np.sum(dV))

def surface_trapz_rotx(y, x):
    """Surface of solid of rotation around X axis.

    """
    dx = np.diff(x)
    dy = np.diff(y)
    y1 = y[:-1]
    y2 = np.roll(y, -1)[:-1]
    # taking each slice as a truncated cone with radii y and y+dy and height dx
    dS = np.pi * np.abs(y1+y2) * np.sqrt(dx**2 + dy**2)
    return np.sum(dS)

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
        return np.transpose(np.asarray(line))

def split_top_bottom(contoury, contourx):
    """Split closed CCW contour to top and bottom halves"""
    top = contoury<0
    bottom = contoury>=0
    topx = contourx[top]
    topy = -contoury[top]
    topx = topx[::-1]
    topy = topy[::-1]
    bottomx = contourx[bottom]
    bottomy = contoury[bottom]
    return (topy, topx), (bottomy, bottomx)
    
def process(img, seed):
    """Calculate volume, equivolumetric radius and excess area."""
    contourxy = contour(img, seed)
    contour_shifted = np.copy(contourxy)
    contour_shifted[0,:] -= seed[0]
    
    top, bottom = split_top_bottom(*contour_shifted)
    
    volume_bottom = volume_concave(*bottom)
    volume_top = volume_concave(*top)
    
    area_bottom = surface_trapz_rotx(*bottom)
    area_top = surface_trapz_rotx(*top)
    
    V = (volume_bottom+volume_top)/2
    A = (area_bottom+area_top)/2
    
    R0 = (0.75*V/np.pi)**(1/3)
    dA = 4*np.pi*(A/(36*np.pi*V*V)**(1/3)-1)
    
    return {'V':V, 'R0':R0, 'dA':dA, 'seed':seed, 'contour':contourxy.tolist()}
