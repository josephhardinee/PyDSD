# -*- coding: utf-8 -*-

from netCDF4 import Dataset, num2date, date2num


def write_netcdf(dsd, filename):
    """ Write DropSizeDistribution to a netCDF4 file.

    Write a DropSizeDistribution object to a netCDF4 file.

    Note this is still very much a work in progress.

    Parameters
    ----------
    dsd: `DropSizeDistribution`
        DropSizeDistribution object.
    """

    rootgrp = Dataset(filename, "w", format="NETCDF4")

    # Create Dimensions
    d_time = rootgrp.createDimension("time", None)
    d_diameter = rootgrp.createDimension("diameter", len(dsd.diameter["data"][:]))

    # Create Coordinate variables
    v_time = rootgrp.createVariable("time", "f8", ("time",))
    v_time.units = "seconds since 1970-1-1 0:00:00 0:00"
    v_time.long_name = "Time in epoch time"
    v_time[:] = dsd.time["data"]

    v_time_offset = rootgrp.createVariable("time_offset", "f8", ("time",))
    v_time_offset.long_name = "Time offset from base_time"
    v_time_offset.units = "s"
    v_time_offset[:] = dsd.time["data"][:] - dsd.time["data"][0]

    v_base_time = rootgrp.createVariable("base_time", "i")
    v_base_time.long_name = "Base time in Epoch"
    v_base_time.units = "seconds since 1970-1-1 0:00:00 0:00"
    v_base_time[:] = dsd.time["data"][0]

    v_diameter = rootgrp.createVariable("diameter", "f8", ("diameter",))
    v_diameter.long_name = "Center diameter of bins"
    v_diameter.units = "mm"
    v_diameter[:] = dsd.diameter["data"]

    #  Create Variables

    for variable in dsd.fields.keys():
        if variable == "Nd":
            var_name = rootgrp.createVariable(
                variable, "f8", ("time", "diameter"), fill_value=-9999
            )
        else:
            var_name = rootgrp.createVariable(
                variable, "f8", ("time",), fill_value=-9999
            )

        var_name.units = dsd.fields[variable]["units"]
        var_name.long_name = dsd.fields[variable]["long_name"]
        var_name.standard_name = dsd.fields[variable]["standard_name"]
        var_name[:] = dsd.fields[variable]["data"]

    #  Create Attributes

    rootgrp.source = "Created using PyDSD"

    rootgrp.close()
