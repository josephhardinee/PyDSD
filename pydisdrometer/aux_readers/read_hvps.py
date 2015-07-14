__author__ = 'Alyssa Matthews'

# -*- coding: utf-8 -*-
import numpy as np
import numpy.ma as ma
from ..DropSizeDistribution import DropSizeDistribution
import itertools
import scipy.optimize
from pytmatrix.psd import GammaPSD
import csv
import datetime

def read_hvps(filename):
    '''
    Takes a filename pointing to a HVPS Horizontal G1 Aircraft file and returns a drop size distribution object.

    Usage:
    dsd = read_hvps(filename, campaign='acapex')

    Current Options for campaign are:
    'acapex'

    Returns:
    DropSizeDistribution object

    Note: No rain rate in the raw file.
    '''

    reader = hvps_reader(filename)

    if reader:
        dsd = DropSizeDistribution(reader.time, reader.Nd, reader.spread,
                                   diameter=reader.diameter, bin_edges = reader.bin_edges)
        #, total_conc= reader.conc)
        return dsd

    else:
        return None

    del(reader)

class hvps_reader(object):
    '''
    This class reads and parses data from 2DS data files.
    Use the read_2ds_h() function to interface with this.
    '''

    def __init__(self, filename): #, campaign)
        '''
        Handles settuping up a 2DS H reader
        '''

        time = []
        conc = []
        bin_edge_str= [75,225,375,525,675,825,975,1125,1275,1425,1575,1725,1875,2025,2175,2325,
                2475,2625,2775,2925,3075,3375,3675,3975,4275,4575,4875,5175,5475,5775,
                6075,6375,6675,6975,7275,7575,8325,9075,9825,10575,11325,12075,12825,
                13575,14325,15075,16575,18075,19575,21075,22575,24075,25575,27075,28575,
                30075,33075,36075,39075,42075,45075,48075]
        bin_edge_int = []
        for i in range(len(bin_edge_str)):
            bin_edge_int.append(int(bin_edge_str[i]))

        bin_edges = np.array(bin_edge_int)

        self.f = open(filename, 'rU')
        reader = csv.reader(self.f)

        #Remove Header lines but save them to variables for use later
        next(self.f)
        next(self.f)
        next(self.f)
        next(self.f)

        for row in reader:
            time.append(float(row[0].split()[0]))
            conc.append(float(row[4].split()[0]))

        time = np.array(time)
        conc = np.array(conc)

        #spread
        spread = np.empty(61)
        for i in range(len(bin_edges)):
            if i < len(bin_edges)-1:
                spread[i] = bin_edges[i+1] - bin_edges[i]

        #diameter
        diameter = np.empty(61)
        for i in range(len(bin_edges)):
            if i < len(bin_edges)-1:
                diameter[i] = (bin_edges[i+1] + bin_edges[i])/2.

        #reread the file in to loop over and get Nd at each time for each bin size
        self.f.seek(0)
        reader = csv.reader(self.f)
        header_line1 = next(self.f)
        header_line2 = next(self.f)
        header_line3 = next(self.f)
        header_line4 = next(self.f)

        Nd = []
        for row in reader:
            Nd.append(row[10:71])

        Nd = np.array(Nd)

        #Loop over Nd, split each string into number and exponent, and append these to a num or exp array respectively
        Nd_num = np.empty_like(Nd)
        Nd_exp = np.empty_like(Nd)
        for i in range(len(Nd)):
            for j in range(len(Nd[0])):
                s = Nd[i][j]
                splits = s.split('E')
                Nd_num[i][j] = splits[0]
                Nd_exp[i][j] = splits[1]

        #Loop over the Nd num and exp arrays to turn them into floats
        Nd_num_t = np.empty([len(time),len(spread)])
        Nd_exp_t = np.empty([len(time),len(spread)])
        for i in range(len(Nd_num)):
            for j in range(len(Nd_num[0])):
                Nd_num_t[i][j] = float(Nd_num[i][j])
                Nd_exp_t[i][j] = float(Nd_exp[i][j])

        #math to combine num and exp arrays into one array of numbers.
        Nd = Nd_num_t*(10.**Nd_exp_t)

        #Unit conversions to decimal hours, mm, m^3
        self.time = time/3600. #seconds since midnight to decimal hours, UTC
        self.bin_edges = bin_edges/1000. #micrometers to mm
        self.spread = spread/1000. #micrometers to mm
        self.diameter = diameter/1000. #micrometers to mm
        self.Nd = Nd *1000.*1000. # #/L/micrometer to #/m^3/mm
        self.conc = conc#*1000. # #/L to #/m^3




































