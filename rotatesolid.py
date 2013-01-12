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
