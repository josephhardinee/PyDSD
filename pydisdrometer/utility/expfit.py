import numpy as np
from scipy.optimize import curve_fit


def expfit(x, y):
    '''
    expfit calculates an exponential power law fit based upon levenburg-marquardt minimization. Fits
    are of the form. y = ax**b
    Parameters:
    -----------
    x: array_like
        independent variable
    y: array_like
        dependent variable

    Returns:
    --------
    popt : tuple
        Scale and exponential parameters a & b
    pcov: tuple
        Covariance of the fit


    Notes:
    ------
    There are some stability issues if bad data is passed into it.

    '''

    expfunc = lambda x, a, b: a * np.power(x, b)
    popt, pcov = curve_fit(expfunc, x, y)
    return popt, pcov


def expfit2(x, y):
    '''
    expfit2 calculates an exponential power law fit based upon levenburg-marquardt minimization. Fits
    are of the form. y = a(x[0]**b)(x[1]**c)
    Parameters:
    -----------
    x: array_like
        independent variables packed. x[0] is first independent variable tuple, x[1] the second.
    y: array_like
        dependent variable

    Returns:
    --------
    popt : tuple
        Scale and exponential parameters a & b
    pcov: tuple
        Covariance of the fit


    Notes:
    ------
    There are some stability issues if bad data is passed into it.

    '''

    expfunc = lambda x, a, b, c: a * np.power(x[0], b) * np.power(x[1], c)
    popt, pcov = curve_fit(expfunc, x, y)
    return popt, pcov
