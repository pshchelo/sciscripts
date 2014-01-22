#!/usr/bin/env python
'''Convert mmH2O to Pa'''
import sys, os
import numpy as np

def mm_to_Pa(filename):
    dir, name =  os.path.split(filename)

    Pa = np.loadtxt(filename, comments='=', delimiter='\t')*9.81

##    Pa = (mm-mm[0])*9.81

    outname = 'press.txt'
    outfilename = os.path.join(dir, outname)
    np.savetxt(outfilename, Pa, fmt='%.3f', delimiter='\t')
    
if __name__=='__main__':
    filename = sys.argv[1]
    mm_to_Pa(filename)