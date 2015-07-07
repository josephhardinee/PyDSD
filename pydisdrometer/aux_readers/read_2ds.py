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

def read_2ds(filename, campaign='acapex'):
    '''
    Takes a filename pointing to a 2DS Horizontal G1 Aircraft file and returns a drop size distribution object.

    Usage:
    dsd = read_2ds_h(filename, campaign='acapex')

    Current Options for campaign are:
    'acapex'

    Returns:
    DropSizeDistribution object

    Note: No rain rate in the raw file.
    '''

    reader = twoDS_reader_h(filename)

    if reader:
        dsd = DropSizeDistribution(reader.time, reader.Nd, reader.spread,
                                   diameter=reader.diameter, bin_edges = reader.bin_edges)
        #, total_conc= reader.conc)
        return dsd

    else:
        return None

    del(reader)

class twoDS_reader_h(object):
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
        bins = []

       # if not campaign in self.supported_campaigns:
       #     print('Campaign type not supported')
       #     return

        self.f = open(filename, 'rU')
        reader = csv.reader(self.f)

        #Remove Header lines but save them to variables for use later
        next(self.f)
        next(self.f)
        next(self.f)
        header_line4 = next(self.f)

        for row in reader:
            time.append(float(row[0].split()[0]))
            conc.append(float(row[4].split()[0]))

        time = np.array(time)
        conc = np.array(conc)

        header = header_line4.split(",")
        bins = header[10:71]

        #Loop over the bins, split them, remove the C, split again into bin edges
        bin_no_c = []
        bin_no_clist = []
        bin_edge_str = []
        for i in range(len(bins)):
            s = bins[i].split(":")
            bin_no_c.append(s)
            bin_no_clist.append(bin_no_c[i][1])
            s1 = bin_no_clist[i].split('-')
            bin_edge_str.append(s1)

        #Loop over the list of strings containing bin edges, turn them into integers
        bin_edge_int = []
        for i in range(len(bin_edge_str)):
            if i == 0:
                bin_edge_int.append(int(bin_edge_str[i][0]))
                bin_edge_int.append(int(bin_edge_str[i][1]))
            if i > 0 and i < 60:
                bin_edge_int.append(int(bin_edge_str[i][1]))
            if i == 60:
                bin_edge_int.append(4000.)

        bin_edges = np.array(bin_edge_int)

        #spread
        spread = np.empty(61)
        for i in range(len(bin_edges)):
            if i < 61:
                spread[i] = bin_edges[i+1] - bin_edges[i]

        #diameter
        diameter = np.empty(61)
        for i in range(len(bin_edges)):
            if i < 61:
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
        self.Nd = Nd  #*1000.*1000. # #/L/micrometer to #/m^3/mm
        self.conc = conc#*1000. # #/L to #/m^3




































