# -*- coding: utf-8 -*-
'''
Plotting routines for different aspects of the drop size distribution class.
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from pylab import cm


def plot_dsd(dsd, range=None, log_scale=True, tighten=True, ax=None, fig=None):
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
    ax =  parse_ax(ax)
    fig = parse_ax(fig)

    colors = [('white')] + [(cm.jet(i)) for i in range(1, 256)]
    new_map = matplotlib.colors.LinearSegmentedColormap.from_list('new_map',
                                                                colors, N=256)

    if log_scale:
        data = np.log10(dsd.Nd.T)
    else:
        data = dsd.Nd.T
    plt.pcolor(dsd.time, dsd.diameter, data, vmin=0.0,
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
    return fig


def plot_NwD0(dsd, col='k',msize=20, edgcolors='none', title=None,
              ax=None, fig=None, **kwargs):
    """
    Create Normalized Intercept Parameter- median volume diameter scatterplot.

    Convenience function calls scatter plot.

    Parameters
    ----------
    dsd : dict
        PyDSD dictionary.
    col : str
    msize : int
    title : str
    ax : Matplotlib Axis instance
    fig : Matplotlib Figure instance
    **kwargs : Dictionary to pass to matplotlib
    """
    ax =  parse_ax(ax)
    fig = parse_ax(fig)

    xlab = r'D$_0$ (mm)'
    ylab = r'log$_{10}$[N$_w$] (mm$^{-1}$ m$^{-3}$)'
    fig, ax = scatter(dsd['Nw'], dsd['D0'], col=col, msize=msize,
                      edgecolors=edgecolors, title=title, ax=ax, fig=fig,
                      **kwargs)
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    return fig, ax


def plot_ZR(dsd, log_scale=False, col='k',msize=20, edgcolors='none',
            title=None, ax=None, fig=None, **kwargs):
    """
    Create reflectivity - rainfall rate scatterplot.

    Convenience function calls scatter plot.

    Parameters
    ----------
    dsd : dict
        PyDSD dictionary.
    log_scale : str
        True for log, Fale for 'linear' variables.
    col : str
    msize : int
    title : str
    ax : Matplotlib Axis instance
    fig : Matplotlib Figure instance
    **kwargs : Dictionary to pass to matplotlib
    """
    ax =  parse_ax(ax)
    fig = parse_ax(fig)

    if log_scale:
        z = dsd['reflectivity']
        rr = np.log10(dsd['rain_rate'])
        xlab = r'Reflectivity (dBZ)'
        ylab = r'log$_{10}$(Rainfall Rate (mm h$^{-1}$))'
    else:
        z = 10.**(dsd['reflectivity']/10.)
        rr = dsd['rain_rate']
        xlab = r'Reflectivity (mm$^{6}$ m$^{-3}$)'
        ylab = r'Rainfall Rate (mm h$^{-1}$)'

    fig, ax = scatter(z, rr, col=col,
                      msize=msize, edgecolors=edgecolors, title=title,
                      ax=ax, fig=fig, **kwargs)
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    return fig, ax


def plot_ZR_hist2d(dsd, log_scale=False, bins=(80,60), ranges=None, norm=None,
                   xlims=None, ylims=None, title=None,
                   add_colorbar=True, clabel='Normalized Counts',
                   ax=None, fig=None, **kwargs):
    """
    Create reflectivity - rainfall rate scatterplot.

    Convenience function calls scatter plot.

    Parameters
    ----------
    dsd : dict
        PyDSD dictionary.
    log_scale : str
        True for log, Fale for 'linear' variables.
    bins : tuple, (x,y) bin size
    norm : bool Normalize output
    xlims : 2-tuple (Xmin, Xmax)
    ylims : 2-tuple (Ymin, Ymax)
    title : str
    add_colorbar : bool
    clabel: colorbar label
    ax : Matplotlib Axis instance
    fig : Matplotlib Figure instance
    kwargs : Keyword arguments to pass to pcolormesh
    """
    ax =  parse_ax(ax)
    fig = parse_ax(fig)

    if log_scale:
        z = dsd['reflectivity']
        rr = np.log10(dsd['rain_rate'])
        xlab = r'Reflectivity (dBZ)'
        ylab = r'log$_{10}$(Rainfall Rate (mm h$^{-1}$))'
    else:
        z = 10.**(dsd['reflectivity']/10.)
        rr = dsd['rain_rate']
        xlab = r'Reflectivity (mm$^{6}$ m$^{-3}$)'
        ylab = r'Rainfall Rate (mm h$^{-1}$)'

    fig, ax = plot_hist2d(z, rr, bins=bins, ranges=ranges, norm=norm,
                          xlims=xlims, ylims=ylims, title=title,
                          add_colorbar=add_colorbar,
                          clabel=clabel,
                          ax=ax, fig=fig, **kwargs)

    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    return fig, ax


def scatter(xvar, yvar, col='k',msize=20, edgecolors='none', title=None,
            ax=None, fig=None, **kwargs):
    """
    Create a scatterplot two variables.

    Parameters
    ----------
    xvar : array
    yvar : array
    col : str
    msize : int
    title : str
    ax : Matplotlib Axis instance
    fig : Matplotlib Figure instance
    **kwargs : Dictionary to pass to matplotlib
    """
    ax =  parse_ax(ax)
    fig = parse_ax(fig)

    ax.scatter(xvar, yvar, c=col, s=msize, edgecolors=edgecolors, **kwargs)

    if title is not None:
        ax.set_title(title)
    return fig, ax


def plot_hist2d(xvar, yvar, bins=(80,60), ranges=None, norm=None,
                xlims=None, ylims=None, title=None, colorbar=True,
                clabel='Normalized Counts', ax=None, fig=None, **kwargs):
    """
    2-D histogram plot.

    Parameters
    ----------
    xvar : array
    yvar : array
    bins : tuple, (x,y) bin size
    norm : bool Normalize output
    xlims : 2-tuple (Xmin, Xmax)
    ylims : 2-tuple (Ymin, Ymax)
    title : str
    colorbar : bool
    clabel: colorbar label
    ax : Matplotlib Axis instance
    fig : Matplotlib Figure instance
    kwargs : Keyword arguments to pass to pcolormesh
    """
    ax =  parse_ax(ax)
    fig = parse_ax(fig)

    if xlims is None:
        xlims = (np.nanmin(xvar), np.nanmax(xvar))
    if ylims is None:
        ylims = (np.nanmin(yvar), np.nanmax(yvar))

    hist2d, xedges, yedges = get_masked_hist2d(
        xvar, yvar, bins=bins, ranges=(ylims, xlims), norm=norm)

    # Replace any zero values with missing data for nice plots
    hist2d = np.ma.masked_equal(hist2d, 0)

    # Flip and rotate the 2D Histogram
    hist2d = np.rot90(hist2d)
    hist2d = np.flipud(hist2d)

    # Create 2D arrays from xedges, yedges
    x2d, y2d = np.meshgrid(xedges, yedges)

    # Plot the data using colormesh
    ax.pcolormesh(x2d, y2d, hist2d, **kwargs)

    if title is not None:
        ax.set_title(title)

    if colorbar:
        cb = fig.colorbar(shrink=0.85)
        cb.set_label(clabel)
    return fig, ax


def plot_ts(dsd, varname, date_format='%H:%M', tz=None, xMinTicker='minute',
            title=None, ax=None, fig=None, **kwargs):
    """
    Time series plot of variable.

    Parameters
    ----------
    dsd : dict
        PyDSD dictionary.
    varname : str or list
        Variable name(s) to plot.
    date_format : str
        Timestring format characters.
    tz : str
        Time zone to uses, see datetime module.
    xMinTicker : str
        Minor tick formatting, 'second','minute','hour','day' supported
    title : str
    ax : Matplotlib Axis instance
    fig : Matplotlib Figure instance
    kwkargs : Keyword arguments to pass to pcolormesh
    """
    ax =  parse_ax(ax)
    fig = parse_ax(fig)

    xFmt = DateFormatter(date_format, tz=tz)

    ax.plot_date(dsd.time['data'], dsd[varname]['data'], **kwargs)

    ax.xaxis.set_major_formatter(xFmt)
    if xMinTicker == 'second':
        from  matplotlib.dates import SecondLocator
        ax.xaxis.set_minor_locator(SecondLocator())
    elif xMinTicker == 'minute':
        from  matplotlib.dates import MinuteLocator
        ax.xaxis.set_minor_locator(MinuteLocator())
    elif xMinTicker == 'hour':
        from  matplotlib.dates import HourLocator
        ax.xaxis.set_minor_locator(HourLocator())
    elif xMinTicker == 'day':
        from  matplotlib.dates import DayLocator
        ax.xaxis.set_minor_locator(DayLocator())

    if title is not None:
        ax.set_title(title)
    return fig, ax


def plotHov(dsd, xvar, datavar, log_scale=False,
            date_format='%H:%M', tz=None,
            clevs=7, vmin=None, vmax=None,
            title=None, set_major_locator='minute',
            colorbar=True, cbor='vertical', clabel=' ',cmap='jet'):
    """
    Hovmoeller plot with time on Y-axis.

    Parameters
    ----------
    dsd : dict
        PyDSD dictionary.
    xvar : str
        Variable name for x-axis.
    datavar : str
        Variable name(s) to plot.
    log_scale : str
        True for log, Fale for 'linear' variables.
    date_format : str
        Timestring format characters.
    tz : str
        Time zone to uses, see datetime module.
    clevs : int
        Number of contour levels.
    vmin : float
        Minimum contour value to display.
    vmax : float
        Maximum contour value to display.
    title : str
    set_major_locator : str
        Minor tick formatting, 'second','minute','hour','day' supported.
    colorbar : bool
        True to include colorbar.
    cbor : str
        Colorbar orientation 'vertical' or 'horizontal'.
    cblab : str
        Colorbar label.
    cmap : Colormap name or instance
    ax : Matplotlib Axis instance
    fig : Matplotlib Figure instance
    kwkargs : Keyword arguments to pass to pcolormesh
    """
    ax =  parse_ax(ax)
    fig = parse_ax(fig)

    yFmt = DateFormatter(date_format, tz=tz)

    if vmin is None:
        vmin = np.nanmin(dsd[varname]['data'])
    if vmax is None:
        vmax = np.nanmax(dsd[varname]['data'])
    clevels = np.logspace(vmin,vmax,clevs)

    if log_scale:
        data = np.log10(dsd[datavar]['data'])
        norm=LogNorm()
    else:
        data = dsd[datavar]['data']
        norm=None
    cs = ax.contourf(dsd[xvarname]['data'], dsd.time['data'], data,
                     clevels, norm=norm, cmap=cmap)

    plt.xscale('log') # Make X-axis logarithmic

    ax.yaxis.set_major_formatter(yFmt) # Set the date format
    if yMajTicker == 'second':
        from  matplotlib.dates import SecondLocator
        ax.yaxis.set_major_locator(SecondLocator())
    elif yMajTicker == 'minute':
        from  matplotlib.dates import MinuteLocator
        ax.yaxis.set_major_locator(MinuteLocator())
    elif yMajTicker == 'hour':
        from  matplotlib.dates import HourLocator,MinuteLocator
        ax.yaxis.set_major_locator(HourLocator())
        ax.yaxis.set_minor_locator(MinuteLocator(interval=10))
    elif yMajTicker == 'day':
        from  matplotlib.dates import DayLocator
        ax.yaxis.set_major_locator(DayLocator())

    if title is not None:
        ax.set_title(title)

    if colorbar:
        if log_scale:
            l_f = mtic.LogFormatter(10, labelOnlyBase=False)
        if cbor == 'vertical':
            frac = 0.05
            shrink = 0.6
        cb = plt.colorbar(cs, orientation=cbor, fraction=frac, pad=.05)
        cb.set_label(clabel)
    return fig, ax

def plot_hexbin(xvar, yvar, grid=(80,60), min_count=0.01, title=None,
                reduce_function=np.sum, add_colorbar=True,
                clabel='Normalized Counts', ax=None, fig=None):
    """
    Density scatterplot using the hex bin method.

    The color marker is based upon density of value population.

    Parameters
    ----------
    xvar : array
    yvar : array
    grid : tuple, (x,y) bin size
    min_count : float, display minimum
    title : str
    reduce_function : func
    add_colorbar : bool
    clabel: colorbar label
    ax : Matplotlib Axis instance
    fig : Matplotlib Figure instance
    """
    if ax is None:
        ax =  parse_ax(ax)
    if fig is None:
        fig = parse_ax(fig)

    # This will plot a hex bin plot (density scatter plot)
    # Establish an array from 0-100 to show colors as density
    c = np.ones_like(xvar) * 100 / len(Z)

    # Create the hex plot
    ax.hexbin(xvar, yvar, C=c, gridsize=grid, mincnt=min_count,
                   reduce_C_function=reduce_function)

    if title is not None:
        ax.set_title(title)

    # Add colorbar
    if add_colorbar:
        cb = fig.colorbar(shrink=0.85)
        cb.set_label(clabel)
    return fig, ax


def get_masked_hist2d(xvar, yvar, bins=(25,25), ranges=None, norm=False):
    """
    Calculate a 2D histogram.

    Remove missing values and calculate a numpy histogram.

    Parameters
    ----------
    xvar : array
    yvar : array
    bins : 2-tuple
    ranges : array [Xmin, Xmax, Ymin, Ymax]
    norm : bool Whether to normalize the output
    """
    # Apply existing masks if possible
    qx = Var1.copy()
    qy = Var2.copy()
    qx = np.ma.masked_where(np.ma.getmask(qy), qx).compressed()
    qy = np.ma.masked_where(np.ma.getmask(qx), qy).compressed()

    if ranges is None:
        ranges = ([qx.min(),qx.max()],[qy.min(),qy.max()])

    hist2d, xedges, yedges = np.histogram2d(
        qx, qy, bins=bins, range=ranges, normed=norm)
    return hist2d, xedges, yedges

def set_ax_limits(xlim=None, ylim=None, ax=None):
    """Convenience function to set x, y limits."""
    ax = parse_ax(ax)
    if ylim is not None:
        ax.set_ylim(ylim)
    if xlim is not None:
        ax.set_xlim(xlim)


def set_minor_ticks(x=None, y=None, ax=None):
    """Convenience function to adjust minor tick spacing."""
    ax = parse_ax(ax)
    try:
        ax.xaxis.set_minor_locator(mtic.MultipleLocator(x))
    except:
        pass
    try:
        ax.yaxis.set_minor_locator(mtic.MultipleLocator(y))
    except:
        pass


def set_major_ticks(x=None, y=None, ax=None):
    """Convenience function to adjust major tick spacing."""
    ax = parse_ax(ax)
    try:
        ax.xaxis.set_major_locator(mtic.MultipleLocator(x))
    except:
        pass
    try:
        ax.yaxis.set_major_locator(mtic.MultipleLocator(y))
    except:
        pass


def set_xlabel(label, pad=None, fontsize=None, ax=None):
    """Convenience function to adjust x-axis label."""
    ax = parse_ax(ax)
    ax.set_xlabel(label, labelpad=pad, fontsize=fonstize)


def set_ylabel(label, pad=None, fontsize=None, ax=None):
    """Convenience function to adjust x-axis label."""
    ax = parse_ax(ax)
    ax.set_ylabel(label, labelpad=pad, fontsize=fonstize)


def turn_ticks_out(ax=None):
    """Convenience function to turn ticks outward."""
    ax = parse_ax(ax)
    ax.tick_params(which='both', direction='out')


def parse_ax(ax):
    """ Parse and return ax instance. """
    if ax is None:
        ax = plt.gca()
    return ax


def parse_fig(fig):
    """ Parse and return fig instance. """
    if fig is None:
        fig = plt.gcf()
    return fig
