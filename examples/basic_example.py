'''
A simple example using PyDisdrometer. This example reads in a OTT APU Disdrometer file, calculates the radar variables, and plots a few of them.
Author: Joseph C. Hardin
'''

import numpy as np
import matplotlib.pyplot as plt

import pydisdrometer as pyd 
import pytmatrix as pyt


filename = '../testdata/20110909.mis'

#Read in the Parsivel File
dsd = pyd.read_parsivel(filename)

dsd.calculate_radar_parameters(wavelength=pyt.tmatrix_aux.wl_Ku)



