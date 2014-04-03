import numpy as np
from scipy.optimize import curve_fit


def expfit(x,y):
    '''
    expfit calculates an exponential power law fit.
    Note: There are some stability issues if bad data is passed into it.
    '''

    expfunc = lambda x,a,b: a*np.power(x,b)
    popt, pcov = curve_fit(expfunc, x, y)
    return popt, pcov
