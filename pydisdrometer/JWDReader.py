# -*- coding: utf-8 -*-
import numpy as np
from DropSizeDistribution import DropSizeDistribution


def read_jwd(filename):
    '''
    Takes a filename pointing to a Joss-WaldVogel file and returns
    a drop size distribution object.

    Usage:
    dsd = read_jwd(filename)

    Returns:
    DropSizeDistrometer object

    '''

    reader = JWDReader(filename)
    dsd = DropSizeDistribution(reader.time, reader.Nd, spread=reader.spread,
                               diameter=reader.diameter, rain_rate=reader.rain_rate,
                               bin_edges=reader.bin_edges)
    return dsd


class JWDReader(object):

    '''
    JWDReader class takes takes a filename as it's only argument(for now).
    This should be a Joss-Waldvogel datafile.
    '''
    diameter = np.array([
        0.359, 0.455, 0.551, 0.656, 0.771, 0.913, 1.116, 1.331, 1.506, 1.665,
        1.912, 2.259, 2.584, 2.869, 3.198, 3.544, 3.916, 4.350, 4.859, 5.373])

    spread = np.array([
        0.092, 0.100, 0.091, 0.119, 0.112, 0.172, 0.233, 0.197, 0.153, 0.166,
        0.329, 0.364, 0.286, 0.284, 0.374, 0.319, 0.423, 0.446, 0.572, 0.455])

    def __init__(self, filename):
        self.filename = filename
        self.rain_rate = []

        self.Nd = []
        self.time = []

        self._read_file()
        self._prep_data()

        self.bin_edges = np.hstack(
            (0, self.diameter + np.array(self.spread) / 2))

    def getSec(self, s):
        l = s.split(':')
        if int(l[0]) <= 15 and int(l[1]) < 37:
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
            for line in f:
                self.time.append(
                    float(self.getSec(line.split()[1])))
                md = line.split()[3:23]
                md_float = np.array(map(float, md))
                self.Nd.append(
                    self.conv_md_to_nd(md_float))
                self.rain_rate.append(
                    float(line.split()[24]))

    def _prep_data(self):
        self.Nd = np.array(self.Nd)
        self.time = np.array(self.time)
        self.time = self.time - self.time[0]
        self.rain_rate = np.array(self.rain_rate)
