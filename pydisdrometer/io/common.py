# -*- coding: utf-8 -*-
import numpy as np
from netCDF4 import num2date, date2num

def _var_to_dict(standard_name, data, units, long_name):
    """
    Convert variable information to a dictionary.
    """
    d = {}
    d['data'] = data[:]
    d['units'] = units
    d['long_name'] = long_name
    d['standard_name'] = standard_name
    return d

def _ncvar_to_dict(ncvar):
    """
    Convert a NetCDF Dataset variable to a dictionary.
    Appropriated from Py-Art package.
    """
    d = dict((k, getattr(ncvar, k)) for k in ncvar.ncattrs())
    d['data'] = ncvar[:]
    if np.isscalar(d['data']):
        # netCDF4 1.1.0+ returns a scalar for 0-dim array, we always want
        # 1-dim+ arrays with a valid shape.
        d['data'] = np.array(d['data'][:])
        d['data'].shape = (1, )
    return d

def _get_epoch_units():
    """Set common time units for AWOT. Using Epoch."""
    return 'seconds since 1970-1-1 00:00:00+0:00'

def _get_epoch_time(times, t_units):
    """Convert time to epoch time and return a dictionary."""
    # Convert the time array into a datetime instance
    dts = num2date(times, t_units)
    # Now convert this datetime instance into a number of seconds since Epoch
    TimeSec = date2num(dts, _get_epoch_units())
    # Now once again convert this data into a datetime instance
    Time_unaware = num2date(TimeSec, _get_epoch_units())
    eptime = {'data': Time_unaware, 'units': _get_epoch_units(),
              'standard_name': 'Time', 'long_name': 'Time (UTC)'}
    return eptime