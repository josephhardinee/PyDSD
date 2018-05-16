# -*- coding: utf-8 -*-
"""
The calc_dsd module contains various fitting functions to calculate dsd parameters
based on measured drop size distributions. Many of these (all currently) were ported from the 
pyparticleprobe package. 
"""

from __future__ import print_function, division

import numpy as np
import scipy.special as scifunct

from ..utility import configuration

"""

A grouping of functions to calculate parameters of a drop size distribution
 using the methodology of  Ulbrich and Atlas (JAM 1998, JAMC 2007).
That study assumes a gamma distribution
 (using the complete gamma function) of the DSD
      N(D) = N0 * D^mu * exp(-Lambda*D)

 and uses the method of moments, with the nth moment expressed:
                               Gamma(n + mu + 1)
      Mn = D^n*N(D)*dD = N0 * -------------------
                              Lambda^(n + mu + 1)

 where N0 is the intercept parameter (mm^(-1-m) m^-3), mu is the shape
  parameter (unitless) and Lambda is the slope paramter (m).

            (7-11eta) - [(7-11eta)^2 -4(eta-1)(30eta-12)]^(1/2)
      mu =  -----------------------------------------------------
                                 2(eta-1)
 where
               M4^2
      eta = -----------
             M2 * M6

 and
               ( (4+mu)(3+mu)M2 )^(1/2)
      Lambda =  (----------------)
               (       M4       )


 and N0 can be found using the 6th moment (M6 or Ze) and solving for N0
           M6 * Lambda^(7+mu)
      N0 = -----------------
              Gamma(7+mu)

Adapted by Nick Guy.

"""

# Define various constants that may be used for calculations
rho0 = 1.2  # reference density at the surface [kg m^-3]
rhoL = 1000.  # density of water [kg m^-3]


def eta_ratio(M2, M4, M6):
    """Compute the ratio eta using the method of moments

    Ulbrich and Atlas (JAM 1998), Eqn 8

    Parameters
    ----------
    M2: float
        Second moment of the DSD [m^-1]
    M4: float
        Fourth moment of the DSD [m]
    M6: float
        Sixth moment of the DSD [m^3]

    Returns
    -------
    Eta: float
        Ratio of M4^2/(M2*M6) [unitless]

    Notes
    -----
    This particular methodology uses the 2nd, 4th, and 6th moments.
    """

    Eta = M4 ** 2 / (M2 * M6)
    return Eta


def shape(M2, M4, M6):
    """Compute the shape parameter mu using the method of moments

    Ulbrich and Atlas (JAM 1998), Eqns 8 and 9

    Parameters
    ----------
    M2: float
        Second moment of the DSD [m^-1]
    M4: float
        Fourth moment of the DSD [m]
    M6: float
        Sixth moment of the DSD [m^3]

    Returns
    -------
    mu: float
        Shape parameter of gamma DSD model [unitless]
    Notes
    -----

  This particular methodology uses the 2nd, 4th, and 6th moments.
  First the 3rd moment normalized by Dm (M4/M3) is calculated.
  Next the shape paramter is computed.
  The denominator [2*(Eta-1)] values are filtered between -1E-1 and +1E-1
  to ensure that unrealistically large shape parameter values 
  are not calculated.
    """
    # Calculate the eta ratio [eq. 8]
    eta = eta_ratio(M2, M4, M6)

    # Now calculate the shape parameter [eq. 3]
    muNumer = (7.0 - 11.0 * eta) - np.sqrt(
        (7.0 - 11.0 * eta) ** 2.0 - 4.0 * (eta - 1.0) * (30. * eta - 12.0)
    )
    muDenom = 2.0 * (eta - 1.0)

    # Mask any zero or unrealistically low values in denominator
    muDenom = np.ma.masked_inside(muDenom, -1E-1, 1E-1)

    mu = muNumer / muDenom

    return mu


def slope(M2, M4, mu):
    """Compute the slope (Lambda) using the method of moments

    Ulbrich and Atlas (JAM 1998), Eqn 10
    Parameters
    ----------
    M2: float
        Second moment of the DSD [m^-1]
    M4: float
        Fourth moment of the DSD [m]
    mu: float
        Shape parameter of gamma DSD model [unitless]

    Returns
    -------
    Lambda: float
        Slope [m^-1]
    Notes:
    ------
    This particular methodology uses the 3rd and 4th moments and shape
    paramter to compute the slope is computed.
    """
    Lambda = np.ma.sqrt((4 + mu) * (3 + mu) * M2 / M4)

    return Lambda


def intercept(M6, mu, Lambda):
    """Compute the intercept parameter (N0) using the method of moments 

    Ulbrich and Atlas (JAM 1998), Eqn 6 solved for N0

    Parameters
    ----------
    M6: float
        Sixth moment of the DSD [m^3]
    mu: float
        Shape parameter of gamma DSD model [unitless]
    Lambda: float
        Slope [m^-1]
    Returns
    -------
    N0: float
        Intercept parameter [m^(-1-shape) m^-3]

    Notes
    -----
    The exponents work out in the following way:
    M6*Lambda^(7+mu) = m^-3*m^-1(7+mu) = m^-3*m^-7*m^-mu = m^(-1-mu) * m^-3
    """

    # Calculate numerator
    IntNumer = M6 * Lambda ** (7. + mu)

    # Calculate denominator
    # Mask values near 0., otherwise gamma function returns "inf"
    mucopy = np.ma.masked_inside(mu, -1E-1, 1E-1)
    IntDenom = scifunct.gamma(7 + mucopy)
    # Mask any invalid values
    np.ma.masked_invalid(IntDenom)

    # Mask any zero values from Denom (-999. a problem)
    IntDenom = np.ma.masked_equal(IntDenom, 0.)
    # print(mu(:,0)+"  "+Lambda(:,0)+"  "+IntNumer(:,0)+"  "+IntDenom(:,0))

    # Calculate N0
    N0 = IntNumer / IntDenom

    return N0


def mom_d0(mu, Lambda):
    """Compute the median volume diameter (D0) using the method of moments.

    Ulbrich and Atlas (JAM 1998), Eqn 11

    Parameters
    ----------
    mu: float
        Shape parameter of gamma DSD model [unitless]
    Lambda: float
        Slope paramter of gamma DSD model [m^-1]

    Returns
    -------
    D0: float
        Median volume diameter [m]
    """

    D0 = (3.67 + mu) / Lambda
    return D0


def zr_a(mu, N0):
    """Assuming a rainfall parameter relationship of Z=AR^b,
    Compute the A prefactor using gamma distribution.

    Ulbrich and Atlas (JAMC 2007), Eqn T5

    Parameters
    ----------
    mu: float
        Shape parameter of gamma DSD model [unitless]
    N0: float
        Intercept parameter [m^(-1-shape) m^-3]

    Returns
    -------
    A: float
        Z-R prefactor (see description)
    """

    # Mask 0. values, otherwise gamma function returns "inf"
    mucopy = np.ma.masked_equal(mu, 0.)

    # gamma_fix is a patch for versions earlier than NCL v6.2,
    # which cannot handle missing data in the gamma function
    ANumer = 10E6 * scifunct.gamma(7 + mucopy) * N0 ** (-2.33 / (4.67 + mu))
    ADenom = (33.31 * scifunct.gamma(4.67 + mucopy)) ** ((7 + mu) / (4.67 + mu))

    # Mask any zero values from Denom
    ADenom = np.ma.masked_equal(ADenom, 0.)

    A = ANumer / ADenom

    return A


def zr_b(mu):
    """Assuming a rainfall parameter relationship of Z=AR^b,
    Compute the b exponent using gamma distribution.  

    Ulbrich and Atlas (JAMC 2007), Eqn T5
    Parameters
    ----------
    mu: float
        Shape parameter of gamma DSD model [unitless]

    Returns
    -------
    b: float
        Z-R prefactor (see description)
    """

    b = (7 + mu) / (4.67 + mu)
    return b


def norm_intercept(LWC, Dm):
    """Calculates the normalized intercept parameter, which
    is more physically meaningful than N0.

    Ulbrich and Atlas (JAMC 2007), Eqn T9

    Parameters
    ----------
    LWC: float
        Liquid water content [g m^-3]
    Dm: float
        Volume weigthed mean diameter [m]

    Returns
    -------
    Nw: float
        Normalized intercept parameter
    """
    # The factor of 1000 converts the water density from kg/m^3 to g/m^3
    Nw = (256 / (np.pi * rhoL * 1000.)) * (LWC / Dm ** 4)

    return Nw
