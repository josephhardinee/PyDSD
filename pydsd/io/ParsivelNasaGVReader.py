# -*- coding: utf-8 -*-
import numpy as np
import itertools
import scipy.optimize
from pytmatrix.psd import GammaPSD
import csv
import datetime
import time
from netCDF4 import num2date, date2num
from ..utility.configuration import Configuration

from ..DropSizeDistribution import DropSizeDistribution
from . import common


def read_parsivel_nasa_gv(filename, campaign="ifloods", skip_header=None):
    """
    Parameters
    ----------
    filename: str
        Data file name.
    campaign: str
        Campaign identifier that reads file based upon the format used
        to produce that data.
    skip_header: int
        A number of header lines to skip when reading the file.

    Takes a filename pointing to a Parsivel NASA Field Campaign file and returns
    a drop size distribution object.

    Usage:
    dsd = read_parsivel_nasa_gv(filename, campaign='MC3E_dsd')

    Current Options for campaign are:

    'ifloods'
    'mc3e_dsd'
    'mc3e_raw'

    Returns:
    DropSizeDistrometer object

    Note: NASA's processing strips out rain rate so we have to
    recalculate it based upon a fall speed relationship.
    """

    reader = NASA_APU_reader(filename, campaign, skip_header)

    if reader:
        return DropSizeDistribution(reader)

    else:
        return None


class NASA_APU_reader(object):

    """
    This class reads and parses parsivel disdrometer data from NASA ground
    validation campaigns. These conform to document ???

    Use the read_parsivel_nasa_gv() function to interface with this.
    """
    # Nt      = []
    # T       = []
    # W       = []
    # D0      = []
    # Nw      = []
    # mu      = []
    # rho_w = 1

    def __init__(self, filename, campaign, skip_header):
        """
        Handles setting up a NASA APU Reader
        """

        self.time = []  # Time in minutes from start of recording
        self.Nd = []
        self.config = Configuration()

        if not campaign in self.supported_campaigns:
            print("Campaign type not supported")
            return

        self.f = open(filename, "r")
        reader = csv.reader(self.f)

        if skip_header is not None:
            next(reader, None)

        for row in reader:
            self.time.append(self._parse_time(list(map(int, (row[0].split()[0:4])))))
            self.Nd.append([float(x) for x in row[0].split()[4:]])

        self._prep_data()

        self.bin_edges = self.config.fill_in_metadata(
            "bin_edges",
            np.hstack((0, self.diameter["data"] + np.array(self.spread["data"]) / 2)),
        )
        self.time["data"] = np.ma.array(self._datetime_to_epoch_time(self.time["data"]))

        self.f.close()

    def _prep_data(self):
        self.fields = {}

        self.fields["Nd"] = self.config.fill_in_metadata("Nd", np.ma.array(self.Nd))

        try:
            time_dict = self._get_epoch_time(self.time)
        except:
            time_dict = {
                "data": np.array(self.time),
                "units": None,
                "title": "Time",
                "full_name": "Native file time",
            }

        self.time = time_dict

    def _parse_time(self, time_vector):
        epoch_time = datetime.datetime(time_vector[0], 1, 1) + datetime.timedelta(
            days=time_vector[1] - 1, hours=time_vector[2], minutes=time_vector[3]
        )
        return time.mktime(epoch_time.timetuple())

    def _get_epoch_time(self, sample_time):
        """
        Convert the time to an Epoch time using package standard.
        """
        # Convert the time array into a datetime instance
        time_unaware = num2date(sample_time, common.EPOCH_UNITS)
        eptime = {
            "data": time_unaware,
            "units": common.EPOCH_UNITS,
            "title": "Time",
            "full_name": "Time (UTC)",
        }
        return eptime

    def _datetime_to_epoch_time(self, time_array):
        """
        Convert the time to an Epoch time using package standard.
        """
        epoch = datetime.datetime.utcfromtimestamp(0)
        time_secs = [(timestamp - epoch).total_seconds() for timestamp in time_array]

        return time_secs

    spread = common.var_to_dict(
        "spread",
        np.array(
            [
                0.129,
                0.129,
                0.129,
                0.129,
                0.129,
                0.129,
                0.129,
                0.129,
                0.129,
                0.129,
                0.257,
                0.257,
                0.257,
                0.257,
                0.257,
                0.515,
                0.515,
                0.515,
                0.515,
                0.515,
                1.030,
                1.030,
                1.030,
                1.030,
                1.030,
                2.060,
                2.060,
                2.060,
                2.060,
                2.060,
                3.090,
                3.090,
            ]
        ),
        "mm",
        "Bin size spread of bins",
    )

    supported_campaigns = ["ifloods", "mc3e_dsd", "mc3e_raw"]

    diameter = common.var_to_dict(
        "diameter",
        np.array(
            [
                0.06,
                0.19,
                0.32,
                0.45,
                0.58,
                0.71,
                0.84,
                0.96,
                1.09,
                1.22,
                1.42,
                1.67,
                1.93,
                2.19,
                2.45,
                2.83,
                3.35,
                3.86,
                4.38,
                4.89,
                5.66,
                6.70,
                7.72,
                8.76,
                9.78,
                11.33,
                13.39,
                15.45,
                17.51,
                19.57,
                22.15,
                25.24,
            ]
        ),
        "mm",
        "Particle diameter of bins",
    )

    velocity = common.var_to_dict(
        "velocity",
        np.array(
            [
                0.05,
                0.15,
                0.25,
                0.35,
                0.45,
                0.55,
                0.65,
                0.75,
                0.85,
                0.96,
                1.13,
                1.35,
                1.59,
                1.83,
                2.08,
                2.40,
                2.78,
                3.15,
                3.50,
                3.84,
                4.40,
                5.20,
                6.00,
                6.80,
                7.60,
                8.80,
                10.40,
                12.00,
                13.60,
                15.20,
                17.60,
                20.80,
            ]
        ),
        "m s^-1",
        "Terminal fall velocity for each bin",
    )
