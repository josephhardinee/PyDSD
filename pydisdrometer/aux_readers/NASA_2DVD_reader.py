# -*- coding: utf-8 -*-
import numpy as np
from ..DropSizeDistribution import DropSizeDistribution

import csv
import scipy.io


def read_2dvd_sav_nasa_gv(filename, campaign='ifloods'):
    '''
    Takes a filename pointing to a 2D-Video Disdrometer NASA Field Campaign
    file and returns a drop size distribution object.

    This reader processes the .sav files generated.

    Usage:
    dsd = read_2dvd_sav_nasa_gv(filename, campaign='MC3E_dsd')

    Current Options for campaign are:

    'ifloods'

    Returns:
    DropSizeDistrometer object

    '''

    reader = NASA_2DVD_reader(filename, campaign)

    if reader:
        dsd = DropSizeDistribution(reader.time, reader.Nd, reader.spread,
                                   velocity=reader.velocity, diameter=reader.diameter,
                                   bin_edges=reader.bin_edges, rain_rate=reader.rain_rate)
        return dsd

    else:
        return None

    del(reader)


class NASA_2DVD_reader(object):

    '''
    This class reads and parses 2dvd disdrometer data from nasa ground campaigns. 
    Use the read_2dvd_sav_nasa_gv() function to interface with this.
    '''

    def __init__(self, filename, campaign):
        '''
        Handles setting up a NASA 2DVD Reader  Reader
        '''

        self.time = []  # Time in minutes from start of recording
        self.Nd = []
        self.rainrate = []  # If we want to use rainrate from the .sav
        self.lwc = []
        self.notes = []

        if not campaign in self.supported_campaigns:
            print('Campaign type not supported')
            return

        record = scipy.io.readsav(filename)['dsd_struct']

        self.diameter = record.diam[0]
        self.velocity = 9.65 - 10.3*np.exp(-0.6*self.diameter)  # Atlas1973
        self.velocity = 0.808  # The above equation not completely
                               # stable so we use Atlas 1977
        self.notes.append('Velocities from formula, not disdrometer\n')

        self.time = self._parse_time(record)
        self.Nd = record.dsd[0].T

        self.bin_edges = np.array(range(0, 42)) * 0.2
        self.rain_rate = record.rain[0]

        self.spread = np.array([0.2]*42)

    def _parse_time(self, record):
        # For now we just drop the day stuff, Eventually we'll make this a
        # proper time
        hour = 60.0*np.array([float(hr) for hr in record.hour[0]])
        minute = np.array([float(mn) for mn in record.minute[0]])
        return hour + minute



    supported_campaigns = ['ifloods']
