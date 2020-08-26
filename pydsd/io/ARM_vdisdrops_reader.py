# -*- coding: utf-8 -*-
import numpy as np
import numpy.ma as ma
import itertools
import scipy.optimize
from pytmatrix.psd import GammaPSD
import csv
from datetime import datetime
import os
from netCDF4 import Dataset, num2date

from ..DropSizeDistribution import DropSizeDistribution
from ..io import common


def read_arm_vdisdrops_netcdf(filename, sampling_interval=60):
    """
    Takes a filename pointing to an ARM vdisdrops  netcdf file and returns
    a drop size distribution object. 

    Note we've had to make a few opinionated choices for the processing. We may add these as options later on.
    
    1. The first is to retain the original 2DVD drop size and velocity bins. 
    2. We use the collection area - 0.5 * diameter relation for measurement area. 

    Usage:
    dsd = read_arm_vdisdrops_netcdf(filename)

    Parameters
    ----------
    filename: path
        Filename to read in, corresponds to an ARM vdisdrops file format. 
    sampling_interval: float, optional
        Sampling interval to collect drops into in seconds. Default 60s

    Returns
    -------
    DropSizeDistrometer object
    """

    reader = ARM_vdisdrops_reader(filename, sampling_interval)

    if reader:
        return DropSizeDistribution(reader)
    else:
        return None


class ARM_vdisdrops_reader(object):
    """
    This class reads and parses parsivel disdrometer data from ARM netcdf
    files. These conform to document (Need Document).

    Use the read_parsivel_arm_netcdf() function to interface with this.
    """

    def __init__(self, filename, sampling_interval=60):
        """
        Handles setting up a vdisdrops Reader.
        """

        self.fields = {}


        self.filename = filename
        self.nc_dataset = Dataset(filename)

        time = self.nc_dataset['time'][:]
        time_length = time[-1] - time[0]
        first_time = np.floor(time[0]/60.0)*60.0
        diameter = self.nc_dataset['equivolumetric_sphere_diameter'][:]
        fall_speed = self.nc_dataset['fall_speed'][:]
        # measurement_area = self.nc_dataset['area'][:]

        diameter_bins = np.arange(0.1, 10.1, .2) # Maybe make this able to be passed in? 
        velocity_bins = np.arange(0.2, 10.1, .2)
        spread = np.ones(50) * 0.2
        mean_measurement_area = (100-0.5*diameter_bins)**2

        num_spectra = int(np.ceil(time_length/sampling_interval))
        integration_time_step = first_time + np.arange(0, num_spectra)*sampling_interval 

        drop_spectra = np.zeros((num_spectra, len(diameter_bins), len(velocity_bins)))

        qc_fall_speed = self.nc_dataset['qc_fall_speed'][:]
        qc_diameter = self.nc_dataset['qc_equivolumetric_sphere_diameter'][:]

        i=0
        for idx, itime in enumerate(time):
            if qc_fall_speed[idx] >0 or qc_diameter[idx]>0:
                continue
        #     if np.abs(velocity[idx]-terminal_velocity(diameter[idx]))>0.4*terminal_velocity(diameter[idx]):
        #         continue
            while itime > integration_time_step[i]+sampling_interval:
                i=i+1 
            diameter_bin = min(len(diameter_bins)-1, int(np.round((diameter[idx]-.1)/.2)))
            velocity_bin = min(len(velocity_bins)-1, int(np.round((fall_speed[idx]-.1)/.2)))
            drop_spectra[i, diameter_bin, velocity_bin]+= 1

        Nd  = 1e6 * np.dot(drop_spectra, 1 / velocity_bins) / (mean_measurement_area * spread * sampling_interval )
        # Return a common epoch time dictionary
        self.time = {
            "data": integration_time_step,
            "units": self.nc_dataset["time"].units,
            "standard_name": "Time",
            "long_name": "Time (UTC)",
        }
        # self.time = self._get_epoch_time(time, t_units)

        Nd = np.ma.array(Nd)

        raw_spectrum = np.ma.array(drop_spectra)

        self.diameter = common.var_to_dict(
            "diameter",
            diameter_bins,
            "mm",
            "Particle diameter of bins",
        )
        self.spread = common.var_to_dict(
            "spread",
            spread,
            "mm",
            "Bin size spread of bins",
        )
        self.bin_edges = common.var_to_dict(
            "bin_edges",
            np.hstack((0, self.diameter["data"] + np.array(self.spread["data"]) / 2)),
            "mm",
            "Boundaries of bin sizes",
        )

        self.fields["Nd"] = common.var_to_dict(
            "Nd", Nd, "m^-3 mm^-1", "Liquid water particle concentration"
        )
        self.fields["velocity"] = common.var_to_dict(
            "velocity", velocity_bins, "m s^-1", "Terminal fall velocity for each bin"
        )
        self.fields["drop_spectrum"] = common.var_to_dict(
            "drop_sectrum", raw_spectrum, "m^-3 mm^-1", "Droplet Spectrum"
        )
        self.spectrum_fall_velocity = common.var_to_dict(
            "raw_spectrum_velocity", velocity_bins, "m^-3 mm^-1", "Spectrum Fall Velocity"
        )

def terminal_velocity(D):
    return 9.65-10.3 * np.exp(-.6 * D)