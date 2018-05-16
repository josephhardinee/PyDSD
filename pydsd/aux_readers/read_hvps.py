# -*- coding: utf-8 -*-


import csv
import datetime
import itertools
import numpy as np
import numpy.ma as ma
import scipy.optimize

from pytmatrix.psd import GammaPSD
from ..DropSizeDistribution import DropSizeDistribution
from ..io import common


def read_hvps(filename):
    """ Read a airborne HVPS Cloud Probe File into a DropSizeDistribution Object.

    Takes a filename pointing to a HVPS Horizontal G1 Aircraft file and returns a drop size distribution object.

    Parameters:
    -----------
    filename: string
       HVPS Cloud Probe Filename

    Usage:
    ------
    dsd = read_hvps(filename)

    Returns:
    --------
    dsd: `DropSizeDistribution`
        `DropSizeDistribution` object

    Note:
    -----
    No rain rate in the raw file.
    """

    reader = HVPSReader(filename)

    if reader:
        return DropSizeDistribution(reader)

    else:
        return None

    del (reader)


class HVPSReader(object):
    """
    This class reads and parses data from 2DS data files.
    Use the read_2ds_h() function to interface with this.
    """

    def __init__(self, filename):  # , campaign)
        """
        Handles settuping up a 2DS H reader
        """
        self.fields = {}
        time = []
        Nd = []
        bin_edges = np.array(
            [
                75,
                225,
                375,
                525,
                675,
                825,
                975,
                1125,
                1275,
                1425,
                1575,
                1725,
                1875,
                2025,
                2175,
                2325,
                2475,
                2625,
                2775,
                2925,
                3075,
                3375,
                3675,
                3975,
                4275,
                4575,
                4875,
                5175,
                5475,
                5775,
                6075,
                6375,
                6675,
                6975,
                7275,
                7575,
                8325,
                9075,
                9825,
                10575,
                11325,
                12075,
                12825,
                13575,
                14325,
                15075,
                16575,
                18075,
                19575,
                21075,
                22575,
                24075,
                25575,
                27075,
                28575,
                30075,
                33075,
                36075,
                39075,
                42075,
                45075,
                48075,
            ]
        )

        self.f = open(filename, "rU")
        reader = csv.reader(self.f)

        # Remove Header lines
        next(self.f)
        next(self.f)
        next(self.f)
        next(self.f)

        for row in reader:
            time.append(float(row[0].split()[0]))
            Nd.append(list(map(float, row[10:71])))

        Nd = np.ma.array(Nd)

        time = np.ma.array(time)

        # spread
        spread = np.diff(bin_edges)

        diameter = bin_edges[:-1] + spread / 2.0

        # NEED TO GRAB DATE FROM FILE
        yyyy = os.path.basename(self.filename).split(".")[1][0:4]
        mm = os.path.basename(self.filename).split(".")[1][4:6]
        dd = os.path.basename(self.filename).split(".")[1][6:8]
        t_units = "seconds since " + "-".join([yyyy, mm, dd]) + "T00:00:00"
        # Return a common epoch time dictionary
        self.time = _get_epoch_time(time, t_units)

        self.bin_edges = common.var_to_dict(
            "bin_edges", bin_edges / 1000., "mm", "Boundaries of bin sizes"
        )
        self.spread = common.var_to_dict(
            "spread", spread / 1000., "mm", "Bin size spread of bins"
        )
        self.diameter = common.var_to_dict(
            "diameter", diameter / 1000., "mm", "Particle diameter of bins"
        )
        # #/L/micrometer to #/m^3/mm
        self.fields["Nd"] = common.var_to_dict(
            "Nd",
            np.ma.array(Nd * 1000. * 1000.),
            "m^-3 mm^-1",
            "Liquid water particle concentration",
        )

    def _get_epoch_time(sample_times, t_units):
        """Convert time to epoch time and return a dictionary."""
        # Convert the time array into a datetime instance
        dts = num2date(sample_times, t_units)
        # Now convert this datetime instance into a number of seconds since Epoch
        timesec = date2num(dts, common.EPOCH_UNITS)
        # Now once again convert this data into a datetime instance
        time_unaware = num2date(timesec, common.EPOCH_UNITS)
        eptime = {
            "data": time_unaware,
            "units": common.EPOCH_UNITS,
            "standard_name": "Time",
            "long_name": "Time (UTC)",
        }
