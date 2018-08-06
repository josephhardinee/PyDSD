# -*- coding: utf-8 -*-

import numpy as np
from netCDF4 import Dataset


def write_netCDF(dsd, filename):
    """ Write DropSizeDistribution to a netCDF4 file.

    Write a DropSizeDistribution object to a netCDF4 file.

    Parameters
    ----------
    dsd: `DropSizeDistribution`
        DropSizeDistribution object.
    """

    rootgrp = Dataset(filename, 'w', format="NETCDF4")


    # Create Dimensions
    time = rootgrp.createDimension("time", None)


    #Create Variables


    # Create Attributes
