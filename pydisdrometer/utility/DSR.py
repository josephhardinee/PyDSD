'''
The DSR module contains different drop shape relationships used in
pydisdrometer for the scattering calculations.
'''

import numpy as np


def tb(D_eq):
    '''Thurai and Bringi Drop Shape relationship model.

    Implementation of the Thurai and Bringi Drop Shape model given in [1]
    . This gives the ratio of the major to minor axis.

    Parameters
    -----------
    D_eq: float
        Volume Equivalent Drop Diameter

    Returns
    -------
    axis_ratio: float
        The ratio of the major to minor axis.

    See Also
    --------
    pb : Pruppacher and Beard DSR
    bc : Beard and Chuang DSR

    References
    ----------
    .. [1]  Thurai, Merhala, V. N. Bringi, "Drop axis ratios from a 2D
       video disdrometer." J. Atmos. Oceanic Technol., 22, 966 - 978. 2005

    '''
    if D_eq < 0.7:
        return 1.0
    elif D_eq < 1.5:
        return 1.173 - 0.5165 * D_eq + 0.4698 * D_eq ** 2 - 0.1317 * \
            D_eq ** 3 - 8.5e-3 * D_eq ** 4
    else:
        return 1.065 - 6.25e-2 * D_eq - 3.99e-3 * D_eq ** 2 + 7.66e-4 * \
            D_eq ** 3 - 4.095e-5 * D_eq ** 4


def pb(D_eq):
    '''Pruppacher and Beard Drop Shape relationship model.

    Implementation of the Pruppacher and Beard Drop Shape model given in [1]
    . This gives the ratio of the major to minor axis.

    Parameters
    -----------
    D_eq: float
        Volume Equivalent Drop Diameter

    Returns
    -------
    axis_ratio: float
        The ratio of the major to minor axis.

    See Also
    --------
    tb : Thurai and Bringi DSR
    bc : Beard and Chuang DSR

    References
    ----------
    ..[1] Pruppacher, H. R. and Beard, K. V. (1970), A wind tunnel
      investigation of the internal circulation and shape of water drops
      falling at terminal velocity in air. Q.J.R. Meteorol. Soc., 96:
      247-256
    '''

    return 1.03 - 0.062 * D_eq


def bc(D_eq):
    '''Beard and Chuang Drop Shape relationship model.

    Implementation of the Beard and Chuang Drop Shape model given in [1]
    . This gives the ratio of the major to minor axis.

    Parameters
    -----------
    D_eq: float
        Volume Equivalent Drop Diameter

    Returns
    -------
    axis_ratio: float
        The ratio of the major to minor axis.

    See Also
    --------
    tb : Thurai and Bringi DSR
    pb : Pruppacher and Beard DSR

    References
    ----------
    ..[1]  Beard, Kenneth V., Catherine Chuang, 1987: A New Model for the
    Equilibrium Shape of Raindrops. J. Atmos. Sci., 44, 1509-1524.
    '''

    return 1.0048 + 5.7e-04 * np.power(D_eq, 1) - \
        2.628e-02 * np.power(D_eq, 2) + 3.682e-03 * np.power(D_eq, 3) - \
        1.677e-04 * np.power(D_eq, 4)
