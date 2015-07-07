# -*- coding: utf-8 -*-
import numpy as np
import numpy.ma as ma
from ..DropSizeDistribution import DropSizeDistribution

import itertools
import scipy.optimize
from pytmatrix.psd import GammaPSD
import csv
import datetime
from netCDF4 import Dataset


def read_parsivel_arm_netcdf(filename):
    '''
    Takes a filename pointing to an ARM Parsivel netcdf file and returns
    a drop size distribution object.

    Usage:
    dsd = read_parsivel_parsivel_netcdf(filename)

    Returns:
    DropSizeDistrometer object

    '''

    reader = ARM_APU_reader(filename)

    if reader:
        dsd = DropSizeDistribution(reader.time, reader.Nd, reader.spread,
                                   velocity=reader.velocity, diameter=reader.diameter,
                                   bin_edges=reader.bin_edges, rain_rate=reader.rain_rate)
        return dsd

    else:
        return None

    del(reader)


class ARM_APU_reader(object):

    '''
    This class reads and parses parsivel disdrometer data from ARM netcdf files. These conform to document (Need Document)

    Use the read_parsivel_arm_netcdf() function to interface with this.
    '''


    # Nt      = []
    # T       = []
    # W       = []
    # D0      = []
    # Nw      = []
    # mu      = []
    # rho_w = 1

    def __init__(self, filename):
        '''
        Handles setting up a APU Reader
        '''

        self.time = []  # Time in minutes from start of recording
        self.Nd = []

        self.nc_dataset = Dataset(filename)

        self.diameter = self.nc_dataset.variables['particle_size'][:]
        self.time = self.nc_dataset.variables['time'][:]
        self.Nd = self.nc_dataset.variables['number_density_drops'][:]
        self.spread = self.nc_dataset.variables['class_size_width'][:]
        self.velocity = self.nc_dataset.variables['fall_velocity_calculated'][:]
        self.rain_rate = self.nc_dataset.variables['precip_rate'][:]

        self.bin_edges = np.hstack((0, self.diameter + np.array(self.spread) / 2))


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
