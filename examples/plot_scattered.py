"""
Scattering Example
--------------

This reads in a OTT Parsivel file in ARM .b1 format. It then calculates DSD parameters and plots those.
Author: Joseph C. Hardin
"""

import numpy as np
import matplotlib.pyplot as plt

import pydsd

filename = '../testdata/acxpars2S1.b1.20150124.000000.cdf'
dsd = pydsd.read_parsivel_arm_netcdf(filename)
dsd.calculate_dsd_parameterization()


f, axarr = plt.subplots(3, sharex=True)
pydsd.plot.plot_ts(dsd, 'D0', fig=f, ax=axarr[0], x_min_tick_format='hour')
pydsd.plot.plot_ts(dsd, 'Nw', fig=f, ax=axarr[1], x_min_tick_format='hour')
pydsd.plot.plot_ts(dsd, 'W', fig=f, ax=axarr[2], x_min_tick_format='hour')

plt.show()