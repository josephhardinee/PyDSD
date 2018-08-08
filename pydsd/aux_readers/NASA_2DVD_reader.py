# -*- coding: utf-8 -*-
import numpy as np
import datetime

import scipy.io
from netCDF4 import num2date, date2num

from ..DropSizeDistribution import DropSizeDistribution
from ..io import common
from ..utility.configuration import Configuration


def read_2dvd_sav_nasa_gv(filename, campaign="ifloods"):
    """
    Takes a filename pointing to a 2D-Video Disdrometer NASA Field Campaign
    file and returns a drop size distribution object.

    This reader processes the .sav files generated.

    Usage:
    dsd = read_2dvd_sav_nasa_gv(filename, campaign='ifloods')

    Current Options for campaign are:

    'ifloods'

    Returns:
    DropSizeDistrometer object

    """
    reader = NASA_2DVD_sav_reader(filename, campaign)

    if reader:
        return DropSizeDistribution(reader)
    else:
        return None


def read_2dvd_dsd_nasa_gv(filename, skip_header=None):
    """
    Takes a filename pointing to a 2D-Video Disdrometer NASA Field Campaign
     _dsd file and returns a drop size distribution object.

    This reader processes the _dsd files generated.

    Usage:
    dsd = read_2dvd_dsd_nasa_gv(filename)

    Returns:
    DropSizeDistrometer object

    """
    reader = NASA_2DVD_dsd_reader(filename, skip_header)

    if reader:
        return DropSizeDistribution(reader)
    else:
        return None


class NASA_2DVD_sav_reader(object):

    """
    This class reads and parses 2dvd disdrometer data from nasa ground
    campaigns.

    Use the read_2dvd_sav_nasa_gv() function to interface with this.
    """

    def __init__(self, filename, campaign):
        """
        Handles setting up a NASA 2DVD Reader.
        """
        self.fields = {}

        self.time = []  # Time in minutes from start of recording
        self.Nd = []
        self.rainrate = []  # If we want to use rainrate from the .sav
        self.lwc = []
        self.notes = []

        if not campaign in self.supported_campaigns:
            print("Campaign type not supported")
            return

        record = scipy.io.readsav(filename)["dsd_struct"]

        self.diameter = common.var_to_dict(
            "diameter", record.diam[0], "mm", "Particle diameter of bins"
        )
        self.velocity = 9.65 - 10.3 * np.exp(-0.6 * self.diameter)  # Atlas1973
        # The above equation not completely
        self.velocity = common.var_to_dict(
            "velocity", 0.808, "m s^-1", "Terminal fall velocity for each bin"
        )
        # stable so we use Atlas 1977
        self.notes.append("Velocities from formula, not disdrometer\n")

        time = self._parse_time(record)
        try:
            self.time = self._get_epoch_time(time)
        except:
            raise ValueError("Conversion to Epoch did not work!")
            self.time = {
                "data": np.array(time),
                "units": None,
                "title": "Time",
                "full_name": "Native file time",
            }

        self.fields["Nd"] = common.var_to_dict(
            "Nd", record.dsd[0].T, "m^-3 mm^-1", "Liquid water particle concentration"
        )

        self.bin_edges = common.var_to_dict(
            "bin_edges",
            np.array(list(range(0, 42))) * 0.2,
            "mm",
            "Boundaries of bin sizes",
        )
        self.fields["rain_rate"] = common.var_to_dict(
            "rain_rate", record.rain[0], "mm h^-1", "Rain rate"
        )

        self.spread = common.var_to_dict(
            "spread", np.array([0.2] * 42), "mm", "Bin size spread of bins"
        )

    def _parse_time(self, record):
        # For now we just drop the day stuff, Eventually we'll make this a
        # proper time
        hour = 60.0 * np.array([float(hr) for hr in record.hour[0]])
        minute = np.array([float(mn) for mn in record.minute[0]])
        return hour + minute

    def _get_epoch_time(self, sample_time):
        """
        Convert the time to an Epoch time using package standard.
        """
        # Convert the time array into a datetime instance
        # dt_units = 'minutes since ' + StartDate + '00:00:00+0:00'
        # dtMin = num2date(time, dt_units)
        # Convert this datetime instance into a number of seconds since Epoch
        # timesec = date2num(dtMin, common.EPOCH_UNITS)
        # Once again convert this data into a datetime instance
        time_unaware = num2date(sample_time, common.EPOCH_UNITS)
        eptime = {
            "data": time_unaware,
            "units": common.EPOCH_UNITS,
            "title": "Time",
            "full_name": "Time (UTC)",
        }
        return eptime

    supported_campaigns = ["ifloods"]


class NASA_2DVD_dsd_reader(object):

    """
    This class reads and parses 2dvd disdrometer data from NASA ground
    campaigns. It works with the _dropCounts files from IFloodS.

    Use the read_2dvd_dsd_nasa_gv() function to interface with this.
    """

    def __init__(self, filename, skip_header):
        """
        Handles setting up a NASA 2DVD Reader  Reader
        """
        self.config = Configuration()

        num_samples = self._get_number_of_samples(filename, skip_header)

        self.Nd = np.ma.zeros((num_samples, 50))
        self.notes = []
        self.fields = {}

        # This part is troubling because time strings change in nasa files. So we'll go with what our e
        # example files have.
        dt = []
        with open(filename) as input:
            if skip_header is not None:
                for num in range(0, skip_header):
                    input.readline()
            for idx, line in enumerate(input):
                data_array = line.split()
                year = int(data_array[0])
                DOY = int(data_array[1])
                hour = int(data_array[2])
                minute = float(data_array[3])

                # TODO: Make this match time handling(units) from other readers.
                dt.append(
                    datetime.datetime(year, 1, 1)
                    + datetime.timedelta(DOY - 1, hours=hour, minutes=minute)
                )
                self.Nd[idx, :] = [float(value) for value in data_array[4:]]
        self.Nd = np.ma.array(self.Nd)

        epoch = datetime.datetime(1970, 1, 1, 0, 0, 0)

        self.time = [(x - epoch).total_seconds() for x in dt]
        velocity = [
            0.248,
            1.144,
            2.018,
            2.858,
            3.649,
            4.349,
            4.916,
            5.424,
            5.892,
            6.324,
            6.721,
            7.084,
            7.411,
            7.703,
            7.961,
            8.187,
            8.382,
            8.548,
            8.688,
            8.805,
            8.900,
            8.977,
            9.038,
            9.084,
            9.118,
            9.143,
            9.159,
            9.169,
            9.174,
            9.175,
            9.385,
            9.415,
            9.442,
            9.465,
            9.486,
            9.505,
            9.521,
            9.536,
            9.549,
            9.560,
            9.570,
            9.570,
            9.570,
            9.570,
            9.570,
            9.570,
            9.570,
            9.570,
            9.570,
            9.570,
        ]

        self.velocity = self.config.fill_in_metadata("velocity", velocity)
        self.bin_edges = self.config.fill_in_metadata(
            "bin_edges", np.ma.array(np.array(list(range(0, 51))) * 0.2)
        )
        self.spread = self.config.fill_in_metadata("spread", np.array([0.2] * 50))
        self.diameter = self.config.fill_in_metadata(
            "diameter", np.ma.array(np.arange(0.1, 10.1, .2))
        )
        self.fields["Nd"] = self.config.fill_in_metadata("Nd", self.Nd)
        self.time = self.config.fill_in_metadata("time", np.ma.array(self.time))

    def _get_number_of_samples(self, filename, skip_header):
        """ Loop through file counting number of lines to calculate number of samples."""
        num_samples = 0

        with open(filename) as input:
            if skip_header is not None:
                for num in range(0, skip_header):
                    input.readline()

            for line in input:
                num_samples += 1

        return num_samples

    supported_campaigns = ["mc3e", "ifloods"]
