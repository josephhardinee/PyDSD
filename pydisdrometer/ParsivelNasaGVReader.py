# -*- coding: utf-8 -*-
import numpy as np
import numpy.ma as ma
from DropSizeDistribution import DropSizeDistribution

import itertools
import scipy.optimize
from pytmatrix.psd import GammaPSD
import csv
import datetime

def read_parsivel_nasa_gv(filename):
    '''
    Takes a filename pointing to a parsivel NASA Field Campaign file and returns
    a drop size distribution object.

    Usage:
    dsd = read_parsivel_nasa_gv(filename)

    Returns: 
    DropSizeDistrometer object
    
    Note: NASA's processing strips out rain rate so we have to 
    recalculate it based upon a fall speed relationship.
    '''

    reader = NASA_APU_reader(filename)
    dsd = DropSizeDistribution(reader.time, reader.Nd, reader.spread,
                               velocity=reader.velocity, diameter=reader.diameter,
                               bin_edges=reader.bin_edges)

    return dsd




class NASA_APU_reader:
    '''
    This class reads and parses parsivel disdrometer data from nasa ground campaigns. These conform to document:

    Use the read_parsivel_nasa_gv() function to interface with this.
    '''

    time    = [] #Time in minutes from start of recording
    Nd      = []
    # Nt      = []
    # T       = []
    # W       = []
    # D0      = []
    # Nw      = []
    # mu      = []
    # rho_w = 1


    def __init__(self, filename):
        self.f = open(filename,'r')
        reader = csv.reader(self.f)
        self.diameter = np.array([float(x) for x in reader.next()[0].split()[1:]])
        self.velocity = np.array([float(x) for x in reader.next()[0].split()[1:]])

        for row in reader:
            self.time.append(float(row[0].split()[0]))
            self.Nd.append([float(x) for x in row[0].split()[1:]])

        self.time = np.array(self.time)
        self.Nd = np.array(self.Nd)
        self.bin_edges=np.hstack((0,self.diameter+np.array(self.spread)/2))
    
    spread = [0.129, 0.129, 0.129, 0.129,0.129,0.129,0.129,0.129,0.129,0.129,0.257,
            0.257,0.257,0.257,0.257,0.515,0.515,0.515,0.515,0.515,1.030,1.030,
            1.030,1.030,1.030,2.060,2.060,2.060,2.060,2.060,3.090, 3.090]


