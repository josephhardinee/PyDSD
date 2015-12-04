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

def read_2ds(filename, campaign='acapex'):
    '''Read a airborne 2DS Cloud Probe File into a DropSizeDistribution Object.

    Takes a filename pointing to a 2DS Horizontal G1 Aircraft file and returns a `DropSizeDistribution` object.

    Parameters:
    -----------
    filename: string
       2DS Cloud Probe Filename
    campaign: optional, string
        Optional campaign setting, currently does nothing. Defaults to acapex

    Usage:
    ------
    dsd = read_2ds_h(filename, campaign='acapex')

    Current Options for campaign are:
    'acapex'

    Returns:
    --------
    dsd: `DropSizeDistribution`
        `DropSizeDistribution` object

    Note:
    -----
    No rain rate in the raw file.
    '''

    reader = TwoDSReader(filename, campaign)

    if reader:
        dsd = DropSizeDistribution(reader.time, reader.Nd, reader.spread,
                                   diameter=reader.diameter, bin_edges = reader.bin_edges)
        return dsd
    else:
        return None

    del(reader)


class TwoDSReader(object):
    ''' TwoDSReader class for 2DS Cloud Probe Data.

    This class reads and parses data from 2DS data files. Use the read_2ds() function to interface with this.
    '''

    def __init__(self, filename, campaign='acapex'): 
        ''' Initializer for a 2DS Cloud Probe class.

            Read and process a 2DS Cloud Probe data file. This should only be called by the read_2ds() function.

            Parameters:
            -----------
            filename: string
                filename pointing to a 2DS file.
            campaign: optional, string
                campaign name, currently only supports acapex. Defaults to 'acapex'

            Returns:
            --------
            two_ds: TwoDSReader
                TwoDSReader class
        '''

        time = []
        bins = []
        Nd = []

        self.f = open(filename, 'rU')
        reader = csv.reader(self.f)

        #Remove Header lines but save them to variables for use later
        next(self.f)
        next(self.f)
        next(self.f)
        header_l = next(self.f)

        for row in reader:
            time.append(float(row[0].split()[0]))
            Nd.append(map(float,row[10:71]))

        Nd = np.array(Nd)
        time = np.array(time)

        header = header_l.split(",")
        bins = header[10:71]

        #Loop over the bins, split them, remove the C, split again into bin edges
        bin_edge_str = []
        for i,sbin in enumerate(bins):
            s = sbin.split(":")
            bin_no_clist=s[1]
            s1 = bin_no_clist.split('-')
            bin_edge_str.append(s1)

        #Loop over the list of strings containing bin edges, turn them into integers
        
        bin_edge_int = []
        bin_edge_int.append(float(bin_edge_str[0][0]))
        for sbins in bin_edge_str:
            bin_edge_int.append(float(sbins[1]))

        bin_edge_int[-1] = 4000
        bin_edges = np.array(bin_edge_int)

        spread = np.diff(bin_edges)

        #diameter
        diameter = bin_edges[0:-1] + spread/2.0

        #Unit conversions to decimal hours, mm, m^3
        self.time = time/3600.0 #seconds since midnight to decimal hours, UTC
        self.bin_edges = bin_edges/1000.0 #micrometers to mm
        self.spread = spread/1000.0 #micrometers to mm
        self.diameter = diameter/1000.0 #micrometers to mm
        self.Nd = Nd *1000.*1000. # #/L/micrometer to #/m^3/mm




































