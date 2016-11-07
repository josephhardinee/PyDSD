# -*- coding: utf-8 -*-
import numpy as np
import numpy.ma as ma
import itertools
import scipy.optimize
from pytmatrix.psd import GammaPSD
import csv
import datetime
from netCDF4 import Dataset
import os

from ..DropSizeDistribution import DropSizeDistribution
from ..io import common


def read_disdrometer_arm_netcdf(filename):
    '''
    Takes a filename pointing to an ARM Parsivel netcdf file and returns
    a drop size distribution object.
    This was tested with acapex data.

    Usage:
    dsd = read_parsivel_parsivel_netcdf(filename)

    Returns:
    DropSizeDistrometer object

    '''

    reader = ArmDisdrometerReader(filename)

    if reader:
        return DropSizeDistribution(reader)
    else:
        return None

    del(reader)


class ArmDisdrometerReader(object):
    """
    This class reads and parses JWD Impact disdrometer data from ARM netcdf
    files. These conform to document (Need Document).

    Use the read_disdrometer_arm_netcdf() function to interface with this.
    """
    def __init__(self, filename):
        self.fields = {}
        self.time = []  # Time in minutes from start of recording
        self.Nd = []

        self.dataset = Dataset(filename)

        time_offset = np.ma.array(self.dataset.variables['time_offset'][:])
        base_time = datetime.datetime.fromtimestamp(self.dataset.variables['base_time'][0])

        # Return a common epoch time dictionary
        #self.time = self._epoch_time(time_offset, t_units)

        self.time = {'data': time_offset, 'units': 's since basetime',
                'standard_name': "Time", 'long_name': "Time (UTC)" }

        Nd = np.ma.array(
            self.dataset.variables['nd'][:])
        velocity = np.ma.array(
            self.dataset.variables['fall_vel'][:])
        rain_rate = np.ma.array(
            self.dataset.variables['rain_rate'][:])

        self.spread = common.var_to_dict(
            'spread', self.dataset.variables['delta_diam'][:],
            'mm', 'Bin size spread of bins')

        self.diameter = common.var_to_dict(
            'diameter', self.dataset.variables['mean_diam_drop_class'][:],
            'mm', 'Particle diameter of bins')

        self.bin_edges = common.var_to_dict(
            'bin_edges',
            np.hstack((0, self.diameter['data'] + np.array(self.spread['data']) / 2.0)),
            'mm', 'Boundaries of bin sizes')

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
