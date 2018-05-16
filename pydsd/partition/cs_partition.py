import numpy as np
from ..utility import ts_utility


def cs_partition_bringi_2010(
    Nw, D0, slope=-1.65, intercept=6.5, c_thresh=0.1, s_thresh=-0.1
):
    """Methodology put forth in Bringi et al. (JAOT 2009)[1], discussed in 
    Thurai et al (JAOT 2010).

    This techniques separates convective and stratiform based upon 
    Normalized gamma intercept parameter - Mean Drop Diameter, 
     log10(Nw)-D0 space.
    This technique calculates an index: Index = log10(NwData) - log10(NwLine).
    A fit line is found in the form log10(Nw) = C1 * D0 + C2.
    Values in a range about the fit line, specified by thresholds are 
    considered transition, while outside these thresholds are either 
    convective or stratiform as below.
                            
    Values above log10(Nw)+Cthresh are considered convective.
    Values below log10(Nw)-Sthresh are considered stratiform.

    Parameters:
    -----------
    Nw: array_like
        Normalized intercept parameter, linear scale.
    D0: array_like
        Median drop diameter.
    slope: optional, float
        Slope C1 constant as defined above.
    intercept: optional, float 
        Intercept C2 parameter as defined above.
    c_thresh: optional, float
        Threshold added to fit line, above which considered convective.
    s_thresh: optional, float
        Threshold added to fit line, below which considered stratiform.

    Returns:
    --------

    classification: array_like
        Convective stratiform classification. 0-unclassified, 1-Stratiform, 2-convective, 3-transition.

    References:
    -----------
    [1]Bringi et al. (JAOT 2009)
    """

    nPts = len(Nw)
    classification = np.zeros_like(Nw)

    Nw_D0_index = np.ma.log10(Nw) - (slope * np.array(D0) + intercept)

    classification[Nw_D0_index <= s_thresh] = 1

    classification[Nw_D0_index >= c_thresh] = 2

    # We could probably remove this line by initializing to 3?
    classification[np.logical_and(Nw_D0_index > s_thresh, Nw_D0_index < c_thresh)] = 3
    return classification


def cs_partition_islam_2012(rain_rate, r_thresh=10.0, sd_thresh=1.5, window=4):
    """Convective stratiform partitioning from Islam et al (Atmos Res 2012). The method
    combines Testud et al. 2011, and Bringi et al. 2003. 

    Parameters:
    -----------
    rain_rate: array_like
        rain rate in mm/hr
    r_thresh: optional, float
        rain rate threshold for which above is convective
    sd_thresh: optional, float
        standard deviation of rain rate threshold above which is convective
    window: optional, int
        Window size for calculating standard deviation.

    Returns:
    --------
    classification: array_like
        Convective stratiform classification. 0-unclassified, 1-stratiform, 2-convective.

    References:
    [1]: Tested et al. 2011
    [2]: Bringi et al. 2003
    """

    classification = np.zeros_like(rain_rate)
    classification[:] = 2  # Defaults to convective for now.
    padded_rain_rate = np.pad(rain_rate, int(window / 2), "reflect")

    n_pts = len(rain_rate)

    thresh_left = padded_rain_rate < r_thresh

    windowed_thresh = ts_utility.rolling_window(thresh_left, window)
    windowed_std = np.std(ts_utility.rolling_window(padded_rain_rate, window), 1)

    rain_thresh_mask = list(map(np.all, windowed_thresh))
    std_thresh_mask = windowed_std < sd_thresh
    convective_mask = np.logical_and(rain_thresh_mask, std_thresh_mask)

    classification[convective_mask] = 1

    return classification


def cs_partition_atlas_2000(vertical_velocity, w_thresh=1.0):
    """ Convective stratiform partitioning from Atlas et al. (JGR 2000).
    Convective stratiform partitioning based upon vertical velocity. This study was
    based on aircraft instrumentation. If used on non-aerial data, great care should
    be taken.

    Parameters:
    -----------
    vertical_velocity: array_like
        vertical velocity of hydrometers.
    w_thresh: optional, float
        Vertical velocity threshold above which hydrometeors are classified convective.

    Returns:
    --------
    classification: array_like
        Convective stratiform classification. 0-unclassified, 1-stratiform, 2-convective.

    References:
    [1] Atlas et al. (JGR 2000)
    """

    classification = np.zeros_like(vertical_velocity)

    classification[np.array(vertical_velocity) > w_thresh] = 2
    classification[np.array(vertical_velocity) < w_thresh] = 1

    return classification
