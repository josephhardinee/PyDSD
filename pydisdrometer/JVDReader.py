# -*- coding: utf-8 -*-
import numpy as np
import numpy.ma as ma
from DropSizeDistribution import DropSizeDistribution


def read_jvd(filename):
    '''
    Takes a filename pointing to a parsivel raw file and returns
    a drop size distribution object.

    Usage:
    dsd = read_parsivel(filename)

    Returns:
    DropSizeDistrometer object

    '''

    reader = JVDReader(filename)
    dsd = DropSizeDistribution(reader.time, reader.Nd, spread = reader.spread, 				       diameter=reader.diameter, rain_rate = reader.rain_rate, bin_edges = reader.bin_edges)
    return dsd

   

'''
    dsd = DropSizeDistribution(reader.time, reader.Nd, reader.spread,
                               rain_rate=reader.rain_rate, velocity=reader.velocity,
                               Z=reader.Z, num_particles=reader.num_particles,
                               bin_edges=reader.bin_edges, diameter=reader.diameter)
'''

    #dsd.raw_matrix = reader.raw
    #dsd.filtered_raw_matrix = reader.filtered_raw_matrix
    #return dsd


class JVDReader(object):

    '''
    JVDReader class takes takes a filename as it's only argument(for now).
    This should be a jvd raw datafile.

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
        self.Z = []
        self.num_particles = []

        self.nd = []
	self.Nd = []
        self.vd = []
        self.raw = []
        self.code = []
        self.time = []
	
        self.ndt = []

        #pcm_matrix_file = open('parsivel_conditional_matrix.txt')
        #self.pcm = np.reshape(self.pcm_matrix, (20, 20))

        self._read_file()
        self._prep_data()

        self.bin_edges = np.hstack(
            (0, self.diameter + np.array(self.spread) / 2))
        #self._apply_pcm_matrix()

    def getSec(self,s):
    	l = s.split(':')
    	if int(l[0])<=15 and int(l[1])<37:
        	return int(l[0])*3600 + int(l[1])*60 + int(l[2])+86400
    	else:
        	return int(l[0])*3600 + int(l[1])*60 + int(l[2])

    def conv_md_to_nd(self, Nd):
        F = 0.005
	t = 30.0
        v = 9.65-10.3*np.exp(-0.6*self.diameter)
	return np.divide(Nd,(F*t*np.multiply(v,self.spread)))

    def _read_file(self):
        with open(self.filename) as f:
	    header = next(f)
	    for line in f:
	   	#time_hms = line.split()[1]
        	#time_s = self.getSec(time_hms)
        	#self.time.append(float(time_s))
		self.time.append(
			float(self.getSec(line.split()[1])))
        	md = line.split()[3:23]
        	md_float = np.array(map(float, md))
        	#n1ton20_float = np.array(n1ton20_float)
 		self.Nd.append(
			self.conv_md_to_nd(md_float))     
    		#rain_intensity = line.split()[24]
		#self.rain_rate.append(float(rain_intensity))
		self.rain_rate.append(
			float(line.split()[24]))


    def _apply_pcm_matrix(self):
        self.filtered_raw_matrix = np.ndarray(shape=(len(self.raw),
                                                     20, 20), dtype=float)
        for i in range(len(self.raw)):
            self.filtered_raw_matrix[i] = np.multiply(
                self.pcm, np.reshape(self.raw[i], (20, 20)))

    def _prep_data(self):
	self.Nd = np.array(self.Nd)
	self.time = np.array(self.time) 
	self.time = self.time-self.time[0]
        self.rain_rate = np.array(self.rain_rate)
        #self.Z = ma.masked_equal(self.Z, -9.999)
        #self.nd = np.array(self.nd)
        #self.nd[self.nd == -9.999] = 0
        #self.Nd = np.array(self.nd)
        #self.num_particles = np.array(self.num_particles)
        #self.time = np.array(self.time)
        #self.velocity = self.vd  # np.ndarray(self.vd)
        #self.raw = np.power(10, np.ndarray(self.raw))

    #def get_sec(self, s):
       # return int(s[0]) * 3600 + int(s[1]) * 60 + int(s[2])


    def bc(D_eq):
        return 1.0048 + 5.7 * 10 ** (-4) - 2.628 * 10 ** (-2) * D_eq * D_eq ** 2 +\
            3.682 * 10 ** (-3) * D_eq ** 3 - 1.677 * 10 ** -4 * D_eq ** 4

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





