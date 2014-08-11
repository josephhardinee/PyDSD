import numpy as np
from scipy.optimize import curve_fit


def expfit(x, y):
    '''
    expfit calculates an exponential power law fit based upon levenburg-marquardt minimization.
    Note: There are some stability issues if bad data is passed into it.
    '''

    expfunc = lambda x, a, b: a * np.power(x, b)
    popt, pcov = curve_fit(expfunc, x, y)
    return popt, pcov


def expfit2(x, y):
    '''
    Exponential Fitting for 2 parameters.
    Note: There are some stability issues if bad data is pased into it.
    '''

    expfunc = lambda x, a, b, c: a * np.power(x[0], b) * np.power(x[1], c)
    popt, pcov = curve_fit(expfunc, x, y)
    return popt, pcov
