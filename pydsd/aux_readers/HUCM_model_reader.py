# -*- coding: utf-8 -*-
import numpy as np
import datetime

import scipy.io
from netCDF4 import num2date, date2num

from ..DropSizeDistribution import DropSizeDistribution
from ..io import common
from ..utility.configuration import Configuration


def read_hucm(data,dates,bins):
    """
    Takes a filename pointing to a 2D-Video Disdrometer NASA Field Campaign
     _dsd file and returns a drop size distribution object.
    This reader processes the _dsd files generated.
    Usage:
    dsd = read_2dvd_dsd_nasa_gv(filename)
    Returns:
    DropSizeDistrometer object
    """
    reader = HUCM_dsd_reader(data,dates,bins)
 
    if reader:
        return DropSizeDistribution(reader)




class HUCM_dsd_reader(object):

    """
    This class reads and parses data from a HUCM model simulation.
    """

    def __init__(self, data,dates,bins):
        """
        Handles setting up a model  Reader
        """
        self.config = Configuration()

        num_samples =len(np.ravel(data[0,:,:]))
        
        nbins = len(data[:,0,0])
        shp = np.shape(data[0,:,:])
        data1d = np.reshape(data,[nbins,num_samples])
        self.Nd = np.ma.zeros((num_samples, nbins))
        self.notes = []
        self.shp = shp
        self.fields = {}

        # This part is troubling because time strings change in nasa files. So we'll go with what our e
        # example files have.
        dt = []
        for idx, line in enumerate(data1d[0,:]):
             self.Nd[idx, :] = data1d[:,idx]
             dt.append(dates)
        self.Nd = np.ma.array(self.Nd)
        self.time = np.array(dt)

        velocity = np.array([
            5.00E-02,
            7.80E-02,
            1.20E-01,
            1.90E-01,
            3.10E-01,
            4.90E-01,
            7.70E-01,
            1.20E+00,
            1.90E+00,
            3.00E+00,
            4.80E+00,
            7.40E+00,
            1.10E+01,
            1.70E+01,
            2.60E+01,
            3.70E+01,
            5.20E+01,
            7.10E+01,
            9.40E+01,
            1.20E+02,
            1.60E+02,
            2.10E+02,
            2.60E+02,
            3.30E+02,
            4.10E+02,
            4.80E+02,
            5.70E+02,
            6.60E+02,
            7.50E+02,
            8.20E+02,
            8.80E+02,
            9.00E+02,
            9.00E+02,
        ])/10.

        self.velocity = self.config.fill_in_metadata("velocity", velocity)
#         self.bin_edges = self.config.fill_in_metadata(
#             "bin_edges", np.ma.array(np.array(list(range(0, nbins))) * 0.2)
#         )
        self.spread = self.config.fill_in_metadata("spread", np.diff(np.insert(bins,0,0)))
        self.diameter = self.config.fill_in_metadata(
            "diameter", np.ma.array(bins)
        )

        self.bin_edges = np.hstack(
            (0, self.diameter["data"] + np.array(self.spread["data"]) / 2)
        )

        self.fields["Nd"] = self.config.fill_in_metadata("Nd", self.Nd)
        self.time = self.config.fill_in_metadata("time", np.ma.array(self.time))



