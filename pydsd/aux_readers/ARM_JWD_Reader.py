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
import os


def read_arm_jwd_b1(filename):
    """
    Takes a filename pointing to an ARM Parsivel netcdf file and returns
    a drop size distribution object.

    Usage:
    dsd = read_parsivel_parsivel_netcdf(filename)

    Returns:
    DropSizeDistrometer object

    """

    reader = ArmJwdReader(filename)

    if reader:
        return DropSizeDistribution(reader)
    else:
        return None

    del (reader)


class ArmJwdReader(object):
    """
    This class reads and parses parsivel disdrometer data from ARM netcdf
    files. These conform to document (Need Document).

    Use the read_arm_jwd_b1() function to interface with this.
    """

    def __init__(self, filename):
        """
        Handles setting up a reader.
        """
        self.fields = {}
        self.info = {}

        self.nc_dataset = Dataset(filename)
        self.filename = filename

        time = np.ma.array(
            self.nc_dataset.variables["time_offset"][:]
            + self.nc_dataset.variables["base_time"][:]
        )
        self.time = self._get_epoch_time(time)

        Nd = np.ma.array(self.nc_dataset.variables["nd"][:])
        velocity = np.ma.array(self.nc_dataset.variables["fall_vel"][:])
        rain_rate = np.ma.array(self.nc_dataset.variables["rain_rate"][:])
        self.diameter = np.ma.array(
            self.nc_dataset.variables["mean_diam_drop_class"][:]
        )
        self.spread = np.ma.array(self.nc_dataset.variables["delta_diam"][:])

        # TODO: Move this to new metadata utility, and just add information from raw netcdf where appropriate
        self.bin_edges = common.var_to_dict(
            "bin_edges",
            np.hstack((0, self.diameter + np.array(self.spread) / 2)),
            "mm",
            "Boundaries of bin sizes",
        )
        self.spread = common.var_to_dict(
            "spread", self.spread, "mm", "Bin size spread of bins"
        )
        self.diameter = common.var_to_dict(
            "diameter", self.diameter, "mm", "Particle diameter of bins"
        )

        self.fields["Nd"] = common.var_to_dict(
            "Nd", Nd, "m^-3 mm^-1", "Liquid water particle concentration"
        )
        self.fields["velocity"] = common.var_to_dict(
            "velocity", velocity, "m s^-1", "Terminal fall velocity for each bin"
        )
        self.fields["rain_rate"] = common.var_to_dict(
            "rain_rate", rain_rate, "mm h^-1", "Rain rate"
        )

        self.fields["num_drop"] = common.var_to_dict(
            "num_drop", self.nc_dataset.variables["num_drop"][:], "#", "Number of Drops"
        )

        self.fields["d_max"] = common.var_to_dict(
            "d_max",
            self.nc_dataset.variables["d_max"][:],
            "mm",
            "Diameter of largest drop",
        )
        self.fields["liq_water"] = common.var_to_dict(
            "liq_water",
            self.nc_dataset.variables["liq_water"][:],
            "gm/m^3",
            "Liquid water content",
        )

        self.fields["n_0"] = common.var_to_dict(
            "n_0",
            self.nc_dataset.variables["n_0"][:],
            "1/(m^3-mm)",
            "Distribution Intercept",
        )
        self.fields["lambda"] = common.var_to_dict(
            "lambda",
            self.nc_dataset.variables["lambda"][:],
            "1/mm",
            "Distribution Slope",
        )

        for key in self.nc_dataset.ncattrs():
            self.info[key] = self.nc_dataset.getncattr(key)

    def _get_epoch_time(self, sample_times):
        """Convert time to epoch time and return a dictionary."""
        eptime = {
            "data": sample_times,
            "units": common.EPOCH_UNITS,
            "standard_name": "Time",
            "long_name": "Time (UTC)",
        }
        return eptime
