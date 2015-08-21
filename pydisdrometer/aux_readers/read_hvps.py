# -*- coding: utf-8 -*-
from __future__ import division

import csv
import datetime
import itertools

import numpy as np
import numpy.ma as ma
import scipy.optimize

from pytmatrix.psd import GammaPSD
from ..DropSizeDistribution import DropSizeDistribution

def read_hvps(filename):
    ''' Read a airborne HVPS Cloud Probe File into a DropSizeDistribution Object.

    Takes a filename pointing to a HVPS Horizontal G1 Aircraft file and returns a drop size distribution object.

    Parameters:
    -----------
    filename: string
       HVPS Cloud Probe Filename

    Usage:
    ------
    dsd = read_hvps(filename)

    Returns:
    --------
    dsd: `DropSizeDistribution`
        `DropSizeDistribution` object

    Note:
    -----
    No rain rate in the raw file.
    '''

    reader = HVPSReader(filename)

    if reader:
        dsd = DropSizeDistribution(reader.time, reader.Nd, reader.spread,
                                   diameter=reader.diameter, bin_edges = reader.bin_edges)
        return dsd

    else:
        return None

    del(reader)

class HVPSReader(object):
    '''
    This class reads and parses data from 2DS data files.
    Use the read_2ds_h() function to interface with this.
    '''

    def __init__(self, filename): #, campaign)
        '''
        Handles settuping up a 2DS H reader
        '''

        time = []
        Nd = []
        bin_edges = np.array([75,225,375,525,675,825,975,1125,1275,1425,1575,1725,1875,2025,2175,2325,
                2475,2625,2775,2925,3075,3375,3675,3975,4275,4575,4875,5175,5475,5775,
                6075,6375,6675,6975,7275,7575,8325,9075,9825,10575,11325,12075,12825,
                13575,14325,15075,16575,18075,19575,21075,22575,24075,25575,27075,28575,
                30075,33075,36075,39075,42075,45075,48075])

        self.f = open(filename, 'rU')
        reader = csv.reader(self.f)

        #Remove Header lines
        next(self.f)
        next(self.f)
        next(self.f)
        next(self.f)


        for row in reader:
            time.append(float(row[0].split()[0]))
            Nd.append(map(float,row[10:71]))

        Nd = np.array(Nd)

        time = np.array(time)

        #spread
        spread = np.diff(bin_edges)

        diameter = bin_edges[:-1] + spread/2.0

        #Unit conversions to decimal hours, mm, m^3
        self.time = time/3600. #seconds since midnight to decimal hours, UTC
        self.bin_edges = bin_edges/1000. #micrometers to mm
        self.spread = spread/1000. #micrometers to mm
        self.diameter = diameter/1000. #micrometers to mm
        self.Nd = Nd *1000.*1000. # #/L/micrometer to #/m^3/mm




































