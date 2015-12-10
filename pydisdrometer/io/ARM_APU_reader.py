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