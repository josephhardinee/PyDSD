# -*- coding: utf-8 -*-
import numpy as np
import numpy.ma as ma
import itertools
import scipy.optimize
from pytmatrix.psd import GammaPSD
import csv
import datetime
from netCDF4 import Dataset

from ..DropSizeDistribution import DropSizeDistribution
from ..io import common


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
        return DropSizeDistribution(reader)
    else:
        return None

    del(reader)


class ARM_APU_reader(object):
    '''
    This class reads and parses parsivel disdrometer data from ARM netcdf
    files. These conform to document (Need Document).

    Use the read_parsivel_arm_netcdf() function to interface with this.
    '''
    def __init__(self, filename):
        '''
        Handles setting up a APU Reader.
        '''
        self.fields = {}
        self.time = []  # Time in minutes from start of recording
        self.Nd = []

        self.nc_dataset = Dataset(filename)

        time = np.ma.array(self.nc_dataset.variables['time'][:])
        # NEED TO GRAB DATE FROM FILE
        yyyy = os.path.basename(self.filename).split(".")[1][0:4]
        mm = os.path.basename(self.filename).split(".")[1][4:6]
        dd = os.path.basename(self.filename).split(".")[1][6:8]
        t_units = 'minutes since ' + "-".join([yyyy, mm, dd]) + 'T00:00:00'
        # Return a common epoch time dictionary
        self.time = _get_epoch_time(time, t_units)

        Nd = np.ma.array(
            self.nc_dataset.variables['number_density_drops'][:])
        velocity = np.ma.array(
            self.nc_dataset.variables['fall_velocity_calculated'][:])
        rain_rate = np.ma.array(
            self.nc_dataset.variables['precip_rate'][:])

        self.bin_edges = common.var_to_dict(
            'bin_edges',
            np.hstack((0, self.diameter + np.array(self.spread) / 2)),
            'mm', 'Boundaries of bin sizes')
        self.spread = common.var_to_dict(
            'spread', self.nc_dataset.variables['class_size_width'][:],
            'mm', 'Bin size spread of bins')
        self.diameter = common.var_to_dict(
            'diameter', self.nc_dataset.variables['particle_size'][:],
            'mm', 'Particle diameter of bins')

        self.fields['Nd'] = common.var_to_dict(
            'Nd', Nd, 'm^-3 mm^-1',
            'Liquid water particle concentration')
        self.fields['velocity'] = common.var_to_dict(
            'velocity', velocity, 'm s^-1',
            'Terminal fall velocity for each bin')
        self.fields['rain_rate'] = common.var_to_dict(
            'rain_rate', rain_rate, 'mm h^-1',
            'Rain rate')

    def _get_epoch_time(sample_times, t_units):
        """Convert time to epoch time and return a dictionary."""
        # Convert the time array into a datetime instance
        dts = num2date(sample_times, t_units)
        # Now convert this datetime instance into a number of seconds since Epoch
        timesec = date2num(dts, common.EPOCH_UNITS)
        # Now once again convert this data into a datetime instance
        time_unaware = num2date(timesec, common.EPOCH_UNITS)
        eptime = {'data': time_unaware, 'units': common.EPOCH_UNITS,
                  'standard_name': 'Time', 'long_name': 'Time (UTC)'}
