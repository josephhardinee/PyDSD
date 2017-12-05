"""
Simple Example
--------------

This reads in a OTT Parsivel file in ARM .b1 format. It then plots the DSD.
Author: Joseph C. Hardin
"""

import numpy as np
import matplotlib.pyplot as plt

import pydsd

filename = '../testdata/acxpars2S1.b1.20150124.000000.cdf'
dsd = pydsd.read_parsivel_arm_netcdf(filename)

fig, ax = pydsd.plot.plot_dsd(dsd, cmap='viridis')
plt.title('Drop Size Distribution')

plt.show()
