# -*- coding: utf-8 -*-
import numpy as np
import numpy.ma as ma
from DropSizeDistribution import DropSizeDistribution

import itertools
import scipy.optimize
from pytmatrix.psd import GammaPSD
import csv
import datetime


def read_parsivel_nasa_gv(filename, campaign='ifloods'):
    '''
    Takes a filename pointing to a parsivel NASA Field Campaign file and returns
    a drop size distribution object.

    Usage:
    dsd = read_parsivel_nasa_gv(filename, campaign='MC3E_dsd')

    Current Options for campaign are:

    'ifloods'
    'mc3e_dsd'
    'mc3e_raw'

    Returns: 
    DropSizeDistrometer object
    
    Note: NASA's processing strips out rain rate so we have to 
    recalculate it based upon a fall speed relationship.
    '''

    reader = NASA_APU_reader(filename, campaign)

    if reader:
        dsd = DropSizeDistribution(reader.time, reader.Nd, reader.spread,
                                   velocity=reader.velocity, diameter=reader.diameter,
                                   bin_edges=reader.bin_edges)
        return dsd

    else:
        return None


class NASA_APU_reader(object):

    '''
    This class reads and parses parsivel disdrometer data from nasa ground campaigns. These conform to document 

    Use the read_parsivel_nasa_gv() function to interface with this.
    '''

    time = []  # Time in minutes from start of recording
    Nd = []
    # Nt      = []
    # T       = []
    # W       = []
    # D0      = []
    # Nw      = []
    # mu      = []
    # rho_w = 1

    def __init__(self, filename, campaign):
        '''
        Handles setting up a NASA APU Reader
        '''

        if not campaign in self.supported_campaigns:
            print('Campaign type not supported')
            return

        self.f = open(filename, 'r')
        reader = csv.reader(self.f)

        if campaign in ['ifloods']:
            self.diameter = np.array([float(x)
                                     for x in reader.next()[0].split()[1:]])
            self.velocity = np.array([float(x)
                                     for x in reader.next()[0].split()[1:]])

            for row in reader:
                self.time.append(float(row[0].split()[0]))
                self.Nd.append([float(x) for x in row[0].split()[1:]])

        if campaign in ['mc3e_dsd']:
            for row in reader:
                self.time.append(self._parse_time((row[0].split()[0:4])))
                self.Nd.append([float(x) for x in row[0].split()[4:]])

        self.time = np.array(self.time)
        self.Nd = np.array(self.Nd)
        self.bin_edges = np.hstack(
            (0, self.diameter + np.array(self.spread) / 2))

        self.f.close()

    def _regenerate_rainfall(self):
        '''
        The goal of this function is to recreate the rainfall that the 
        NASA processing removes. The alternative is to merge the dsd and
        raintables files together. We might add that later
        '''
        print('Not implemented yet')
        pass

    def _parse_time(self, time_vector):
        # For now we just drop the day stuff, Eventually we'll make this a
        # proper time
        return float(time_vector[2]) * 60.0 + float(time_vector[3])

    spread = [
        0.129, 0.129, 0.129, 0.129, 0.129, 0.129, 0.129, 0.129, 0.129, 0.129, 0.257,
        0.257, 0.257, 0.257, 0.257, 0.515, 0.515, 0.515, 0.515, 0.515, 1.030, 1.030,
        1.030, 1.030, 1.030, 2.060, 2.060, 2.060, 2.060, 2.060, 3.090, 3.090]

    supported_campaigns = ['ifloods', 'mc3e_dsd', 'mc3e_raw']

    diameter = np.array(
        [0.06, 0.19, 0.32, 0.45, 0.58, 0.71, 0.84, 0.96, 1.09, 1.22,
         1.42, 1.67, 1.93, 2.19, 2.45, 2.83, 3.35, 3.86, 4.38, 4.89,
         5.66, 6.70, 7.72, 8.76, 9.78, 11.33, 13.39, 15.45, 17.51,
         19.57, 22.15, 25.24])

    velocity = np.array(
        [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.96, 1.13,
         1.35, 1.59, 1.83, 2.08, 2.40, 2.78, 3.15, 3.50, 3.84, 4.40, 5.20,
         6.00, 6.80, 7.60, 8.80, 10.40, 12.00, 13.60, 15.20, 17.60, 20.80])
