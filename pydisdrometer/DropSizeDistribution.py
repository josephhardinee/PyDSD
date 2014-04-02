# -*- coding: utf-8 -*-
import numpy as np
import numpy.ma as ma
import pytmatrix
import DSDProcessor
from pytmatrix.tmatrix import Scatterer
from pytmatrix.psd import PSDIntegrator
from pytmatrix import orientation, radar, tmatrix_aux, refractive

class DropSizeDistribution(object):
    '''
    DropSizeDistribution class to hold DSD's and calculate parameters
    and relationships. Should be returned from the disdrometer*reader objects.
    '''

    def __init__(self, time, Nd, spread, rain_rate=None):
        self.time = time
        self.Nd = Nd
        self.spread = spread
        if rain_rate:
            self.rain_rate = rain_rate
