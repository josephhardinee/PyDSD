# -*- coding: utf-8 -*-
import numpy as np
import datetime
import scipy.io

from ..DropSizeDistribution import DropSizeDistribution
from ..io import common



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
        return DropSizeDistribution(reader)
    else:
        return None

    del(reader)


def read_2dvd_dsd_nasa_gv(filename, campaign='mc3e', skip_header=None):
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
    reader = NASA_2DVD_dsd_reader(filename, campaign, skip_header)

    if reader:
        return DropSizeDistribution(reader)
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
        Handles setting up a NASA 2DVD Reader.
        '''
        self.fields = {}

        self.time = []  # Time in minutes from start of recording
        self.Nd = []
        self.rainrate = []  # If we want to use rainrate from the .sav
        self.lwc = []
        self.notes = []

        if not campaign in self.supported_campaigns:
            print('Campaign type not supported')
            return

        record = scipy.io.readsav(filename)['dsd_struct']

        self.diameter = common.var_to_dict(
            'diameter', record.diam[0], 'mm', 'Particle diameter of bins')
        self.velocity = 9.65 - 10.3 * np.exp(-0.6 * self.diameter)  # Atlas1973
        # The above equation not completely
        self.velocity = common.var_to_dict(
            'velocity', 0.808, 'm s^-1', 'Terminal fall velocity for each bin')
                               # stable so we use Atlas 1977
        self.notes.append('Velocities from formula, not disdrometer\n')

        time = self._parse_time(record)
        try:
            self.time = self._get_epoch_time(time)
        except:
            raise ValueError('Conversion to Epoch did not work!')
            self.time = {'data': np.array(time), 'units': None,
                         'title': 'Time', 'full_name': 'Native file time'}

        self.fields['Nd'] = common.var_to_dict(
            'Nd', record.dsd[0].T, 'm^-3 mm^-1',
            'Liquid water particle concentration')

        self.bin_edges = common.var_to_dict(
            'bin_edges', np.array(range(0, 42)) * 0.2, 'mm',
            'Boundaries of bin sizes')
        self.fields['rain_rate'] = common.var_to_dict(
            'rain_rate', record.rain[0], 'mm h^-1', 'Rain rate')

        self.spread = common.var_to_dict(
            'spread', np.array([0.2]*42), 'mm', 'Bin size spread of bins')

    def _parse_time(self, record):
        # For now we just drop the day stuff, Eventually we'll make this a
        # proper time
        hour = 60.0 * np.array([float(hr) for hr in record.hour[0]])
        minute = np.array([float(mn) for mn in record.minute[0]])
        return hour + minute

    def _get_epoch_time(self, sample_time):
        '''
        Convert the time to an Epoch time using package standard.
        '''
        # Convert the time array into a datetime instance
        #dt_units = 'minutes since ' + StartDate + '00:00:00+0:00'
        #dtMin = num2date(time, dt_units)
        # Convert this datetime instance into a number of seconds since Epoch
        #timesec = date2num(dtMin, common.EPOCH_UNITS)
        # Once again convert this data into a datetime instance
        time_unaware = num2date(sample_time, common.EPOCH_UNITS)
        eptime = {'data': time_unaware, 'units': common.EPOCH_UNITS,
                  'title': 'Time', 'full_name': 'Time (UTC)'}
        return eptime

    supported_campaigns = ['ifloods']


class NASA_2DVD_dsd_reader(object):

    '''
    This class reads and parses 2dvd disdrometer data from NASA ground
    campaigns. It works with the _dropCounts files from IFloodS.

    Use the read_2dvd_dsd_nasa_gv() function to interface with this.
    '''

    def __init__(self, filename, campaign, skip_header):
        '''
        Handles setting up a NASA 2DVD Reader  Reader
        '''
        MIN_IN_DAY = 1440
#        self.time = np.arange(MIN_IN_DAY)  # Time in minutes
        Nd = np.ma.zeros((MIN_IN_DAY, 50))
        self.notes = []

        if not campaign in self.supported_campaigns:
            print('Campaign not supported')
            return

        dt = []
        with open(filename) as input:
            if skip_header is not None:
                for num in range(0, skip_header):
                    input.readline()
            for line in input:
                data_array = line.split()
                dt.append(datetime.datetime(
                    int(data_array[0]), int(data_array[1]),
                    int(data_array[2]), int(data_array[3])))
                time_min = int(data_array[2])*60 + int(data_array[3])
                self.Nd[time_min, :] = [float(value) for value in data_array[4:]]


        self.fields['Nd'] = common.var_to_dict(
            'Nd', Nd, 'm^-3 mm^-1',
            'Liquid water particle concentration')
        self.time = self._get_epoch_time(dt)
        velocity =[0.248, 1.144, 2.018, 2.858, 3.649, 4.349, 4.916, 5.424, 5.892, 6.324,
                        6.721, 7.084, 7.411, 7.703, 7.961, 8.187, 8.382, 8.548, 8.688, 8.805,
                        8.900, 8.977, 9.038, 9.084, 9.118, 9.143, 9.159, 9.169, 9.174, 9.175,
                        9.385, 9.415, 9.442, 9.465, 9.486, 9.505, 9.521, 9.536, 9.549, 9.560,
                        9.570, 9.570, 9.570, 9.570, 9.570, 9.570, 9.570, 9.570, 9.570, 9.570]
        self.velocity = common.var_to_dict(
            'velocity', velocity, 'm s^-1', 'Terminal fall velocity for each bin')

        self.bin_edges = common.var_to_dict(
            'bin_edges', np.array(range(0, 51)) * 0.2, 'mm',
            'Boundaries of bin sizes')

        self.spread = common.var_to_dict(
            'spread', np.array([0.2] * 50), 'mm',
            'Bin size spread of bins')

        self.diameter = common.var_to_dict(
            'diameter', np.arange(0.1, 10.1, .2), 'mm', 'Particle diameter of bins')

    def _get_epoch_time(self, datetime):
        '''
        Convert the time to an Epoch time using package standard.
        '''
        # Convert this datetime instance into a number of seconds since Epoch
        timesec = date2num(dtMin, common.EPOCH_UNITS)
        # Once again convert this data into a datetime instance
        time_unaware = num2date(timesec, common.EPOCH_UNITS)
        eptime = {'data': time_unaware, 'units': common.EPOCH_UNITS,
                'title': 'Time', 'full_name': 'Time (UTC)'}
        return etpime

    supported_campaigns = ['mc3e', 'ifloods']
