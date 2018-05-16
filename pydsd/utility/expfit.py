import numpy as np
from scipy.optimize import curve_fit


def expfit(x, y):
    """
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

    """

    x_array = np.array(x)
    y_array = np.array(y)

    x_finite_index = np.isfinite(x_array)
    y_finite_index = np.isfinite(y_array)

    mask = np.logical_and(x_finite_index, y_finite_index)

    expfunc = lambda x, a, b: a * np.power(x, b)
    popt, pcov = curve_fit(expfunc, x_array[mask], y_array[mask])
    return popt, pcov


def expfit2(x, y):
    """
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
    """

    x1_array = np.array(x[0])
    x2_array = np.array(x[1])
    y_array = np.array(y)

    x1_finite_index = np.isfinite(x1_array)
    x2_finite_index = np.isfinite(x2_array)
    y_finite_index = np.isfinite(y_array)

    mask = np.logical_and(
        x2_finite_index, np.logical_and(x1_finite_index, y_finite_index)
    )

    expfunc = lambda x, a, b, c: a * np.power(x[0], b) * np.power(x[1], c)
    popt, pcov = curve_fit(expfunc, [x1_array[mask], x2_array[mask]], y_array[mask])
    return popt, pcov
