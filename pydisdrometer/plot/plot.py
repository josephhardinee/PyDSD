# -*- coding: utf-8 -*-
'''
Plotting routines for different aspects of the drop size distribution class.
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from pylab import cm


def plot_dsd(dsd, range=None, log_scale=True, tighten=True):
    '''Plotting function for drop size distribution Nd

    plot_dsd creates a pcolormesh based plot for a drop size distribution object's
    `Nd` field.

    Parameters
    ----------
    dsd: DropSizeDistribution
        Drop Size Distribution instance containing a `Nd`.
    range: tuple
        A tuple containing the range to be plotted in form
        (x_begin,x_end,y_begin,y_end)
    log_scale: boolean
        Whether to plot on a log scale, or a linear scale.
    tighten: True
        Whether to restrict plot to areas with data.

    Returns
    -------
    fig_handle: Figure Handle

    '''

    fig_handle = plt.figure()

    colors = [('white')] + [(cm.jet(i)) for i in xrange(1, 256)]
    new_map = matplotlib.colors.LinearSegmentedColormap.from_list('new_map',
                                                                colors, N=256)

    plt.pcolor(dsd.time, dsd.diameter, np.log10(dsd.Nd.T), vmin=0.0,
                figure=fig_handle, cmap=new_map)

    plt.axis('tight')

    if range:
        plt.axis(range)
    else:
        plt.axis((0, dsd.time[-1], 0, dsd.diameter[-1]))

    if tighten:
        max_diameter = dsd.diameter[len(dsd.diameter) -
                            np.argmax(np.nansum(dsd.Nd, axis=0)[::-1] > 0)]
        plt.ylim(0, max_diameter)

    plt.colorbar()
    plt.xlabel('Time(m)')
    plt.ylabel('Diameter(mm)')
    return fig_handle
