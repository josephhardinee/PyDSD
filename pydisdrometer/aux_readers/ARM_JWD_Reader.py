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
from ..utility import configuration
import os


def read_arm_jwd_b1(filename):
    '''
    Takes a filename pointing to an ARM Parsivel netcdf file and returns
    a drop size distribution object.

    Usage:
    dsd = read_parsivel_parsivel_netcdf(filename)

    Returns:
    DropSizeDistrometer object

    '''

    reader = ArmJwdReader(filename)

    if reader:
        return DropSizeDistribution(reader)
    else:
        return None

    del (reader)


class ArmJwdReader(object):
    '''
    This class reads and parses parsivel disdrometer data from ARM netcdf
    files.

    Use the read_arm_jwd_b1() function to interface with this.
    '''

    def __init__(self, filename):
        '''
        Handles setting up a reader.
        '''
        self.fields = {}
        self.info = {}
        config = configuration.Configuration()

        self.nc_dataset = Dataset(filename)
        self.filename = filename

        time = np.ma.array(self.nc_dataset.variables['time_offset'][:] + self.nc_dataset.variables['base_time'][:])
        self.time = self._get_epoch_time(time)

        rain_rate = np.ma.array(
                self.nc_dataset.variables['rain_rate'][:])
        self.diameter = np.ma.array(self.nc_dataset.variables['mean_diam_drop_class'][:])
        self.spread = np.ma.array(self.nc_dataset.variables['delta_diam'][:])

        self.bin_edges = config.fill_in_metadata("bin_edges", np.hstack((0, self.diameter + np.array(self.spread) / 2)))
        self.spread = config.fill_in_metadata("spread", self.spread)
        self.diameter = config.fill_in_metadata("diameter", self.diameter)
        self.fields['Nd'] = config.fill_in_metadata("Nd", self.nc_dataset.variables['nd'][:])
        self.fields['velocity'] = config.fill_in_metadata("velocity", self.nc_dataset.variables['fall_vel'][:])
        self.fields['rain_rate'] = config.fill_in_metadata("rain_rate", rain_rate)

        self.fields['md'] = common.var_to_dict(
                "Md", self.nc_dataset.variables['num_drop'][:], '#/Drop Class',
                "Number of Drops")

        self.fields['Dmax'] = config.fill_in_metadata("Dmax", self.nc_dataset.variables['d_max'][:])
        self.fields['liq_water'] = common.var_to_dict(
            "liq_water", self.nc_dataset.variables['liq_water'][:],
            "gm/m^3", "Liquid water content")

        self.fields['N0'] = config.fill_in_metadata("N0", self.nc_dataset.variables['n_0'][:])

        self.fields['lambda'] = common.var_to_dict(
            "lambda", self.nc_dataset.variables['lambda'][:],
            "1/mm", "Distribution Slope")

        for key in self.nc_dataset.ncattrs():
            self.info[key] =self.nc_dataset.getncattr(key)

        self.extra_fields = {}
        for field in _extra_fields:
            self.extra_fields[field] = self.nc_dataset.variables[field]


    def _get_epoch_time(self, sample_times):
        """Convert time to epoch time and return a dictionary."""
        eptime = {'data': sample_times, 'units': common.EPOCH_UNITS,
                  'standard_name': 'Time', 'long_name': 'Time (UTC)'}
        return eptime

_extra_fields = ["qc_precip_dis", "qc_rain_rate", "Z", "ef", "qc_time" ]
