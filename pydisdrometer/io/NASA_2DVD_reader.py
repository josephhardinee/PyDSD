# -*- coding: utf-8 -*-
import numpy as np
from ..DropSizeDistribution import DropSizeDistribution

import scipy.io


def read_2dvd_sav_nasa_gv(filename, campaign='ifloods'):
    '''
    Takes a filename pointing to a 2D-Video Disdrometer NASA Field Campaign
    file and returns a drop size distribution object.

    This reader processes the .sav files generated.

    Usage:
    dsd = read_2dvd_sav_nasa_gv(filename, campaign='ifloods')

    Current Options for campaign are:

    'ifloods'

    Returns:
    DropSizeDistrometer object

    '''

    reader = NASA_2DVD_sav_reader(filename, campaign)

    if reader:
        dsd = DropSizeDistribution(reader.time, reader.Nd, reader.spread,
                                   velocity=reader.velocity,
                                   diameter=reader.diameter,
                                   bin_edges=reader.bin_edges,
                                   rain_rate=reader.rain_rate)
        return dsd

    else:
        return None

    del(reader)


def read_2dvd_dsd_nasa_gv(filename, campaign='mc3e'):
    '''
    Takes a filename pointing to a 2D-Video Disdrometer NASA Field Campaign
     _dsd file and returns a drop size distribution object.

    This reader processes the _dsd files generated.

    Usage:
    dsd = read_2dvd_dsd_nasa_gv(filename, campaign='mc3e')

    Current Options for campaign are:

    'mc3e'

    Returns:
    DropSizeDistrometer object

    '''

    reader = NASA_2DVD_dsd_reader(filename, campaign)

    if reader:
        dsd = DropSizeDistribution(reader.time, reader.Nd, reader.spread,
                                   velocity=reader.velocity,
                                   diameter=reader.diameter,
                                   bin_edges=reader.bin_edges)
        return dsd

    else:
        return None

    del(reader)


class NASA_2DVD_sav_reader(object):

    '''
    This class reads and parses 2dvd disdrometer data from nasa ground
    campaigns.

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


class NASA_2DVD_dsd_reader(object):

    '''
    This class reads and parses 2dvd disdrometer data from NASA ground
    campaigns. It works with the _dropCounts files from IFloodS.

    Use the read_2dvd_dsd_nasa_gv() function to interface with this.
    '''

    def __init__(self, filename, campaign):
        '''
        Handles setting up a NASA 2DVD Reader  Reader
        '''
        MIN_IN_DAY = 1440
        self.time = np.arange(MIN_IN_DAY)  # Time in minutes
        self.Nd = np.zeros((MIN_IN_DAY, 50))
        self.notes = []

        if not campaign in self.supported_campaigns:
            print('Campaign not supported')
            return

        with open(filename) as input:
            for line in input:
                data_array = line.split()
                time_min = int(data_array[2])*60 + int(data_array[3])
                self.Nd[time_min, :] = [float(value) for value in data_array[4:]]

        self.diameter = np.arange(0.1, 10.1, .2)
        self.velocity =[0.248, 1.144, 2.018, 2.858, 3.649, 4.349, 4.916, 5.424, 5.892, 6.324,
                        6.721, 7.084, 7.411, 7.703, 7.961, 8.187, 8.382, 8.548, 8.688, 8.805,
                        8.900, 8.977, 9.038, 9.084, 9.118, 9.143, 9.159, 9.169, 9.174, 9.175,
                        9.385, 9.415, 9.442, 9.465, 9.486, 9.505, 9.521, 9.536, 9.549, 9.560,
                        9.570, 9.570, 9.570, 9.570, 9.570, 9.570, 9.570, 9.570, 9.570, 9.570]

        self.bin_edges = np.array(range(0, 51)) * 0.2

        self.spread = np.array([0.2]*50)

    supported_campaigns = ['mc3e', 'ifloods']
