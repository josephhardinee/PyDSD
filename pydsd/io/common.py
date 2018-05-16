# -*- coding: utf-8 -*-
import netCDF4
import numpy as np
from netCDF4 import num2date, date2num

EPOCH_UNITS = "seconds since 1970-1-1 00:00:00+0:00"


def var_to_dict(standard_name, data, units, long_name):
    """
    Convert variable information to a dictionary.
    """
    d = {}
    d["data"] = data[:]
    d["units"] = units
    d["long_name"] = long_name
    d["standard_name"] = standard_name
    return d


def ncvar_to_dict(ncvar):
    """
    Convert a NetCDF Dataset variable to a dictionary.
    Appropriated from Py-Art package.
    """
    d = dict((k, getattr(ncvar, k)) for k in ncvar.ncattrs())
    d["data"] = ncvar[:]
    if np.isscalar(d["data"]):
        # netCDF4 1.1.0+ returns a scalar for 0-dim array, we always want
        # 1-dim+ arrays with a valid shape.
        d["data"] = np.array(d["data"][:])
        d["data"].shape = (1,)
    return d


def get_epoch_time(sample_times, t_units):
    """Convert time to epoch time and return a dictionary."""
    # Convert the time array into a datetime instance
    dts = netCDF4.num2date(sample_times, t_units)
    # Now convert this datetime instance into a number of seconds since Epoch
    timesec = netCDF4.date2num(dts, EPOCH_UNITS)
    # Now once again convert this data into a datetime instance
    time_unaware = netCDF4.num2date(timesec, EPOCH_UNITS)
    # eptime = {'data': time_unaware, 'units': EPOCH_UNITS,
    #           'standard_name': 'Time', 'long_name': 'Time (UTC)'}

    eptime = {
        "data": timesec,
        "units": EPOCH_UNITS,
        "standard_name": "Time",
        "long_name": "Time (UTC)",
    }
    return eptime
