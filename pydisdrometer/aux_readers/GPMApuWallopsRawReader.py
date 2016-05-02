# -*- coding: utf-8 -*-
import numpy as np
import numpy.ma as ma
from ..DropSizeDistribution import DropSizeDistribution

import itertools
import scipy.optimize
from pytmatrix.psd import GammaPSD
import csv
import datetime


def read_gpm_nasa_apu_raw_wallops(filename):
    '''
    Takes a filename pointing to a parsivel NASA Field Campaign file with RAW Data and returns
    a drop size distribution object.

    Usage:
    dsd = read_gpm_nasa_apu_raw_wallops(filename)


    Returns:
    DropSizeDistrometer object

    Note: NASA's processing strips out rain rate so we have to
    recalculate it based upon a fall speed relationship.
    '''

    reader = GPMApuWallopsRawReader(filename)
    #return reader
    if reader:
        reader.conv_md_to_nd(reader.Md)
        dsd = DropSizeDistribution(reader.time, reader.Nd_array, reader.spread,
                                   velocity=reader.velocity, diameter=reader.diameter,
                                   bin_edges=reader.bin_edges)
        return dsd,reader

    else:
        return None


class GPMApuWallopsRawReader(object):

    '''
    This class reads and parses parsivel disdrometer data from
    nasa ground campaigns. These conform to document

    '''

    def __init__(self, filename):
        '''
        Handles setting up a NASA APU Reader for Raw 1024 Size Data
        '''

        self.time = []  # Time in minutes from start of recording
        self.raw = []
        self.num_drops = []
        self.rr = []

        self.f = open(filename, 'r')
        reader = csv.reader(self.f)

        for row in reader:
            self.time.append(self._parse_time((row[0])))
            self.raw.append([float(x) for x in row[9:9+1024]])
            self.num_drops.append(float(row[3]))
            self.rr.append(float(row[4]))

        self.time = np.ma.array(self.time)
        self.Md = np.reshape(self.raw, (-1, 32, 32))
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
        return float(time_vector[8:10]) * 60.0 +\
            float(time_vector[10:12]) + float(time_vector[12:14])/60.0

    def conv_md_to_nd(self, Md, t=10/60.0):
        F = 0.0054
        #v = 9.65 - 10.3 * np.exp(-0.6 * self.diameter)
        vel_mat = np.tile(self.velocity, (32, 1))
        spread_mat = np.tile(np.ma.array(self.spread).T, (32, 1))
        self.Nd_mat = np.ma.zeros(np.shape(Md))
        self.Nd_array = np.ma.zeros((len(self.time), 32))
        for ti in range(0, len(self.time)):
            self.Nd_mat[ti] = np.divide(Md[ti],
                                    (F * 60*t * np.multiply(vel_mat, spread_mat)))
            self.Nd_array[ti] = np.sum(self.Nd_mat[ti], axis=0)


    spread = [
        0.129, 0.129, 0.129, 0.129, 0.129, 0.129, 0.129, 0.129, 0.129, 0.129, 0.257,
        0.257, 0.257, 0.257, 0.257, 0.515, 0.515, 0.515, 0.515, 0.515, 1.030, 1.030,
        1.030, 1.030, 1.030, 2.060, 2.060, 2.060, 2.060, 2.060, 3.090, 3.090]

    diameter = np.ma.array(
        [0.06, 0.19, 0.32, 0.45, 0.58, 0.71, 0.84, 0.96, 1.09, 1.22,
         1.42, 1.67, 1.93, 2.19, 2.45, 2.83, 3.35, 3.86, 4.38, 4.89,
         5.66, 6.70, 7.72, 8.76, 9.78, 11.33, 13.39, 15.45, 17.51,
         19.57, 22.15, 25.24])

    velocity = np.ma.array(
        [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.96, 1.13,
         1.35, 1.59, 1.83, 2.08, 2.40, 2.78, 3.15, 3.50, 3.84, 4.40, 5.20,
         6.00, 6.80, 7.60, 8.80, 10.40, 12.00, 13.60, 15.20, 17.60, 20.80])
