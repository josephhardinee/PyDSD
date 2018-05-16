# -*- coding: utf-8 -*-
import numpy as np
from netCDF4 import num2date, date2num

from ..DropSizeDistribution import DropSizeDistribution
from . import common


def read_jwd(filename):
    """
    Takes a filename pointing to a Joss-WaldVogel file and returns
    a drop size distribution object.

    Usage:
    dsd = read_jwd(filename)

    Returns:
    DropSizeDistrometer object

    """
    reader = JWDReader(filename)
    return DropSizeDistribution(reader)


class JWDReader(object):

    """
    JWDReader class takes takes a filename as it's only argument(for now).
    This should be a Joss-Waldvogel datafile.
    """
    diameter = common.var_to_dict(
        "diameter",
        np.array(
            [
                0.359,
                0.455,
                0.551,
                0.656,
                0.771,
                0.913,
                1.116,
                1.331,
                1.506,
                1.665,
                1.912,
                2.259,
                2.584,
                2.869,
                3.198,
                3.544,
                3.916,
                4.350,
                4.859,
                5.373,
            ]
        ),
        "mm",
        "Particle diameter of bins",
    )

    spread = common.var_to_dict(
        "spread",
        np.array(
            [
                0.092,
                0.100,
                0.091,
                0.119,
                0.112,
                0.172,
                0.233,
                0.197,
                0.153,
                0.166,
                0.329,
                0.364,
                0.286,
                0.284,
                0.374,
                0.319,
                0.423,
                0.446,
                0.572,
                0.455,
            ]
        ),
        "mm",
        "Bin size spread of bins",
    )

    def __init__(self, filename):
        self.filename = filename
        self.rain_rate = []

        self.Nd = []
        self.time = []

        self._read_file()
        self._prep_data()

        self.bin_edges = common.var_to_dict(
            "bin_edges",
            np.hstack((0, self.diameter["data"] + np.array(self.spread["data"]) / 2))
            * 0.2,
            "mm",
            "Boundaries of bin sizes",
        )

    def getSec(self, s, start_hh, start_mm):
        l = s.split(":")
        if int(l[0]) < start_hh:
            return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2]) + 86400
        elif int(l[0]) == start_hh and int(l[1]) < start_mm:
            return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2]) + 86400
        else:
            return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])

    def conv_md_to_nd(self, Nd):
        F = 0.005
        t = 30.0
        v = 9.65 - 10.3 * np.exp(-0.6 * self.diameter)
        return np.divide(Nd, (F * t * np.multiply(v, self.spread)))

    def _read_file(self):
        with open(self.filename) as f:
            next(f)
            for i, line in enumerate(f):
                if i == 1:
                    start_time = line.split()[1]
                    t = start_time.split(":")
                    start_hh = int(t[0])
                    start_mm = int(t[1])
                    self.time.append(
                        float(self.getSec(line.split()[1], start_hh, start_mm))
                    )
                    md = line.split()[3:23]
                    md_float = np.array(list(map(float, md)))
                    self.Nd.append(self.conv_md_to_nd(md_float))
                    self.rain_rate.append(float(line.split()[24]))
                elif i > 1:
                    start_time = line.split()[1]
                    t = start_time.split(":")
                    start_hh = int(t[0])
                    start_mm = int(t[1])
                    self.time.append(
                        float(self.getSec(line.split()[1], start_hh, start_mm))
                    )
                    md = line.split()[3:23]
                    md_float = np.array(list(map(float, md)))
                    self.Nd.append(self.conv_md_to_nd(md_float))
                    self.rain_rate.append(float(line.split()[24]))

    def _get_epoch_time(self):
        """
        Convert the time to an Epoch time using package standard.
        """
        # Convert the time array into a datetime instance
        dt_units = "seconds since " + StartDate + "00:00:00+0:00"
        dt_minutes = num2date(self.time, dt_units)
        # Convert this datetime instance into a number of seconds since Epoch
        timesec = date2num(dt_minutes, common.EPOCH_UNITS)
        # Once again convert this data into a datetime instance
        time_unaware = num2date(timesec, common.EPOCH_UNITS)
        eptime = {
            "data": time_unaware,
            "units": common.EPOCH_UNITS,
            "title": "Time",
            "full_name": "Time (UTC)",
        }
        return eptime

    def _prep_data(self):
        fields = {}
        self.time = np.ma.array(self.time)
        self.time = self.time - self.time[0]

        self.fields["Nd"] = common.var_to_dict(
            "Nd",
            np.ma.array(self.Nd),
            "m^-3 mm^-1",
            "Liquid water particle concentration",
        )
        self.fields["rain_rate"] = common.var_to_dict(
            "Rain rate", np.ma.array(self.rain_rate), "mm/h", "Rain rate"
        )

        try:
            self.time = self._get_epoch_time()
        except:
            raise ValueError("Conversion to Epoch did not work!")
            self.time = {
                "data": np.array(self.time),
                "units": None,
                "title": "Time",
                "full_name": "Native file time",
            }
