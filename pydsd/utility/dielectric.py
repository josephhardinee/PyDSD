from __future__ import division
import numpy as np


# Dielectric model from Turner et. al. 2016

a = [8.111e01, 2.025]
b = [4.434e-3, 1.073e-2]
c = [1.302e-13, 1.012e-14]
d = [6.627e02, 6.089e02]
tc = 1.342e2
s = [8.7914e1, -4.044e-1, 9.5873e-4, -1.3280e-6]


def get_refractivity(freq, temp):
    """ Get complex refractivity index

    Parameters
    ----------
    freq: float
        Frequency of transmitted wave.
    temp: float
        Temperature of hydrometeor.

    Returns:
    m_w: complex
        Complex refractivity index.
    """

    es = s[0] + s[1] * temp + s[2] * temp ** 2 + s[3] * temp ** 3
    ep = es - (2 * np.pi * freq) ** 2 * (A_i(0, temp, freq) + A_i(1, temp, freq))
    epp = 2 * np.pi * freq * (B_i(0, temp, freq) + B_i(1, temp, freq))

    return np.sqrt(ep + 1j * epp)


def A_i(i, temp, freq):
    """Get A_i term in double debye model
    """

    delta = a[i] * np.exp(-1 * b[i] * temp)
    tau = c[i] * np.exp(d[i] / (temp + tc))

    return (tau ** 2 * delta) / (1 + (2 * np.pi * freq * tau) ** 2)


def B_i(i, temp, freq):
    """Get B_i term in double debye model
    """

    delta = a[i] * np.exp(-1 * b[i] * temp)
    tau = c[i] * np.exp(d[i] / (temp + tc))

    return (tau * delta) / (1 + (2 * np.pi * freq * tau) ** 2)
