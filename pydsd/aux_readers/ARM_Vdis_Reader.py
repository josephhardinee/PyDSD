# -*- coding: utf-8 -*-
import numpy as np
import numpy.ma as ma
import itertools
import scipy.optimize
from pytmatrix.psd import GammaPSD
from netCDF4 import Dataset

from ..DropSizeDistribution import DropSizeDistribution
from ..io import common
from ..utility.configuration import Configuration


def read_arm_vdis_b1(filename):
    """
    Takes a filename pointing to an ARM vdis netcdf file and returns
    a drop size distribution object. Tested on MC3E data. 

    Usage:
    dsd = read_parsivel_parsivel_netcdf(filename)

    Returns:
    DropSizeDistrometer object

    """

    reader = ArmVdisReader(filename)

    if reader:
        return DropSizeDistribution(reader)
    else:
        return None


class ArmVdisReader(object):
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
        config = Configuration()

        time = np.ma.array(
            self.nc_dataset.variables["time_offset"][:]
            + self.nc_dataset.variables["base_time"][:]
        )
        self.time = self._get_epoch_time(time)

        Nd = np.ma.array(self.nc_dataset.variables["num_density"][:])
        rain_rate = np.ma.array(self.nc_dataset.variables["rain_rate"][:])

        # Sometimes the spread is stored as a bin_width attribute
        self.diameter = np.ma.array(self.nc_dataset.variables["drop_diameter"][:])
        try:
            self.spread = np.ma.array(self.nc_dataset.variables["delta_diam"][:])
        except KeyError:
            width_str = self.nc_dataset.bin_width.split(" ")
            units = width_str[1]
            if units == "mm":
                conv_factor = 1
            elif units == "cm":
                conv_factor = 10
            elif units == "um":
                conv_factor = 1e-3
            elif units == "m":
                conv_factor = 1e3
            self.spread = np.array([float(width_str[0]) * conv_factor])

        #  Sometimes spread is a singleton.
        #  In which case we expand it to the array as 2DVD are fixed size bins.
        if len(self.spread) != Nd.shape[1]:
            self.spread = np.full(Nd.shape[1], self.spread[0])

        self.bin_edges = config.fill_in_metadata(
            "bin_edges", np.hstack((0, self.diameter + np.array(self.spread) / 2))
        )
        self.spread = config.fill_in_metadata("spread", self.spread)
        self.diameter = config.fill_in_metadata("diameter", self.diameter)
        self.fields["Nd"] = config.fill_in_metadata("Nd", Nd)
        self.fields["rain_rate"] = config.fill_in_metadata("rain_rate", rain_rate)

        self.fields["N0"] = config.fill_in_metadata(
            "N0", self.nc_dataset.variables["intercept_parameter"][:]
        )
        self.fields["lambda"] = config.fill_in_metadata(
            "lambda", self.nc_dataset.variables["slope_parameter"][:]
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
