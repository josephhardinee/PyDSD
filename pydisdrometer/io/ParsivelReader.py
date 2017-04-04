# -*- coding: utf-8 -*-
import io
import numpy as np
from netCDF4 import num2date, date2num
from datetime import datetime, timedelta

from ..DropSizeDistribution import DropSizeDistribution
from . import common


def read_parsivel(filename):
    '''
    Takes a filename pointing to a parsivel raw file and returns
    a drop size distribution object.

    Usage:
    dsd = read_parsivel(filename)

    Returns:
    DropSizeDistrometer object

    '''
    reader = ParsivelReader(filename)
    dsd = DropSizeDistribution(reader)

    return dsd


class ParsivelReader(object):

    """
    ParsivelReader class takes takes a filename as it's only argument(for now).
    This should be a parsivel raw datafile(output from the parsivel).

    """
    def __init__(self, filename):
        self.filename = filename
        self.rain_rate = []
        self.Z = []
        self.num_particles = []
        self._base_time = []

        self.nd = []
        self.vd = []
        self.raw = []
        self.code = []
        self.time = []

        self.ndt = []

        self.pcm = np.reshape(self.pcm_matrix, (32, 32))

        self._read_file()
        self._prep_data()

        self.bin_edges = np.hstack(
            (0, self.diameter['data'] + np.array(self.spread['data']) / 2))

        self.bin_edges = common.var_to_dict(
            'bin_edges',
            self.bin_edges,
            'mm', 'Bin Edges')

        self._apply_pcm_matrix()

    def _read_file(self):
        """  Read the Parsivel Data file and store it in internal structure.
        Returns: None

        """
        with io.open(self.filename, encoding='latin-1' ) as f:
            for line in f:
                line = line.rstrip('\n\r;')
                code = line.split(':')[0]
                if code == '01':  # Rain Rate
                    self.rain_rate.append(
                        float(line.split(':')[1]))
                elif code == '07':  # Reflectivity
                    self.Z.append(float(line.split(':')[1]))
                elif code == '11':  # Num Particles
                    self.num_particles.append(
                        int(line.split(':')[1]))
                elif code == '20':  # Time string
                    self.time.append(
                        self.get_sec(line.split(':')[1:4]))
                elif code == '21':  # Date string
                    date_tuple = line.split(':')[1].split('.')
                    self._base_time.append(datetime(year=int(date_tuple[2]),
                                                    month=int(date_tuple[1]),
                                                    day=int(date_tuple[0])))
                elif code == '90':  # Nd
                    self.nd.append(
                        np.power(10, list(map(float, line.split(':')[1].split(';')))))
                elif code == '91':  # Vd
                    self.vd.append(
                        list(map(float, line.split(':')[1].rstrip(';\r').split(';'))))
                elif code == '93':  # md
                    self.raw.append(
                        list(map(int, line.split(':')[1].split(';'))))

    def _apply_pcm_matrix(self):
        """ Apply Data Quality matrix from Ali Tokay
        Returns: None

        """
        self.filtered_raw_matrix = np.ndarray(shape=(len(self.raw),
                                                     32, 32), dtype=float)
        for i in range(len(self.raw)):
            self.filtered_raw_matrix[i] = np.multiply(
                self.pcm, np.reshape(self.raw[i], (32, 32)))

    def _prep_data(self):
        self.fields = {}

        self.fields['rain_rate'] = common.var_to_dict(
            'Rain rate', np.ma.array(self.rain_rate), 'mm/h', 'Rain rate')
        self.fields['reflectivity'] = common.var_to_dict(
            'Reflectivity', np.ma.masked_equal(self.Z, -9.999), 'dBZ',
            'Equivalent reflectivity factor')
        self.fields['Nd'] = common.var_to_dict(
            'Nd', np.ma.masked_equal(self.nd, np.power(10, -9.999)), 'm^-3 mm^-1',
            'Liquid water particle concentration')
        self.fields['Nd']['data'].set_fill_value(0)

        self.fields['num_particles'] = common.var_to_dict(
            'Number of Particles', np.ma.array(self.num_particles),
            '', 'Number of particles')
        self.fields['terminal_velocity'] = common.var_to_dict(
            'Terminal Fall Velocity', self.vd,  # np.ndarray(self.vd),
            'm/s', 'Terminal fall velocity for each bin')

        try:
            self.time = self._get_epoch_time()
        except:
            self.time = {'data': np.array(self.time), 'units': None,
                         'title': 'Time', 'full_name': 'Native file time'}
            print("Conversion to Epoch Time did not work.")

    def get_sec(self, s):
        return int(s[0]) * 3600 + int(s[1]) * 60 + int(s[2])

    def _get_epoch_time(self):
        """
        Convert the time to an Epoch time using package standard.
        """
        time_unaware = np.array([self._base_time[i] + timedelta(seconds=self.time[i]) for i in range(0, len(self.time))])
        epoch = datetime.utcfromtimestamp(0)
        time_secs = [(timestamp-epoch).total_seconds() for timestamp in time_unaware]

        eptime = {'data': time_secs, 'units': common.EPOCH_UNITS,
                  'title': 'Time', 'long_name': 'time'}
        return eptime

    diameter = common.var_to_dict(
        'diameter',
        np.array(
            [0.06, 0.19, 0.32, 0.45, 0.58, 0.71, 0.84, 0.96, 1.09, 1.22, 1.42, 1.67,
             1.93, 2.19, 2.45, 2.83, 3.35, 3.86, 4.38, 4.89, 5.66,
             6.7, 7.72, 8.76, 9.78, 11.33, 13.39, 15.45, 17.51, 19.57, 22.15, 25.24]),
        'mm', 'Particle diameter of bins')

    spread = common.var_to_dict(
        'spread',
        [
        0.129, 0.129, 0.129, 0.129, 0.129, 0.129, 0.129, 0.129, 0.129, 0.129, 0.257,
        0.257, 0.257, 0.257, 0.257, 0.515, 0.515, 0.515, 0.515, 0.515, 1.030, 1.030,
        1.030, 1.030, 1.030, 2.060, 2.060, 2.060, 2.060, 2.060, 3.090, 3.090],
        'mm', 'Bin size spread of bins')

    velocity = common.var_to_dict(
        'velocity',
        np.array(
            [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 1.1, 1.3, 1.5, 1.7, 1.9,
             2.2, 2.6, 3, 3.4, 3.8, 4.4, 5.2, 6.0, 6.8, 7.6, 8.8, 10.4, 12.0, 13.6, 15.2,
             17.6, 20.8]),
        'm s^-1', 'Terminal fall velocity for each bin')

    v_spread = [.1, .1, .1, .1, .1, .1, .1, .1, .1, .1, .2, .2, .2, .2, .2, .4,
                .4, .4, .4, .4, .8, .8, .8, .8, .8, 1.6, 1.6, 1.6, 1.6, 1.6, 3.2, 3.2]

    pcm_matrix = (
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
