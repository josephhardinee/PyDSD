# -*- coding: utf-8 -*-
import numpy as np
import pytmatrix
from pytmatrix.tmatrix import Scatterer
from pytmatrix.psd import PSDIntegrator
from pytmatrix import orientation, radar, tmatrix_aux, refractive
import DSR
from expfit import expfit


class DropSizeDistribution(object):
    '''
    DropSizeDistribution class to hold DSD's and calculate parameters
    and relationships. Should be returned from the disdrometer*reader objects.
    '''

    def __init__(self, time, Nd, spread, rain_rate=None, velocity=None, Z=None,
                num_particles=None, bin_edges=None):
        self.time = time
        self.Nd = Nd
        self.spread = spread
        self.rain_rate = rain_rate
        self.velocity = velocity
        self.Z = Z
        self.num_particles = num_particles
        self.bin_edges = bin_edges

        lt = len(time)
        self.Zh = np.zeros(lt)
        self.Zdr = np.zeros(lt)
        self.Kdp = np.zeros(lt)
        self.Ai = np.zeros(lt)

    def calc_radar_parameters(self, wavelength=tmatrix_aux.wl_X):
        '''
        Calculates the radar parameters and stores them in the object.
        Defaults to X-Band,Beard and Chuang setup. 
        
        Sets object radar parameters:
            Zh, Zdr, Kdp, Ai

        Parameter:
            wavelength = tmatrix supported wavelength.
        '''
        self._setup_scattering(wavelength)

        for t in range(0, len(self.time)):
            BinnedDSD = pytmatrix.psd.BinnedPSD(self.bin_edges,  self.Nd[t])
            self.scatterer.psd = BinnedDSD
            self.scatterer.set_geometry(tmatrix_aux.geom_horiz_back)
            self.Zdr[t] = 10 * np.log10(radar.Zdr(self.scatterer))
            self.Zh[t] = 10 * np.log10(radar.refl(self.scatterer))
            self.scatterer.set_geometry(tmatrix_aux.geom_horiz_forw)
            self.Kdp[t] = radar.Kdp(self.scatterer)
            self.Ai[t] = radar.Ai(self.scatterer)

    def _setup_scattering(self, wavelength):
        self.scatterer = Scatterer(wavelength=wavelength,
                m=refractive.m_w_10C[wavelength])
        self.scatterer.psd_integrator = PSDIntegrator()
        self.scatterer.psd_integrator.axis_ratio_func = lambda D: 1.0 / DSR.bc(D)
        self.scatterer.psd_integrator.D_max = 10.0
        self.scatterer.psd_integrator.geometries = (
            tmatrix_aux.geom_horiz_back, tmatrix_aux.geom_horiz_forw)
        self.scatterer.or_pdf = orientation.gaussian_pdf(20.0)
        self.scatterer.orient = orientation.orient_averaged_fixed
        self.scatterer.psd_integrator.init_scatter_table(self.scatterer)

    def calc_R_kdp_relationship(self):
        '''
        calc_R_kdp_relationship calculates a power fit for the rainfall-kdp
        relationship based upon the calculated radar parameters(which should
        have already been run). It returns the scale and exponential
        parameter a and b in the first tuple, and the second returned argument
        gives the covariance matrix of the fit.
        '''

        popt, pcov = expfit(self.Kdp[self.rain_rate > 0],
                            self.rain_rate[self.rain_rate > 0])

        return popt, pcov

    def calc_R_Zh_relationship(self):
        '''
        calc_R_Zh_relationship calculates the power law fit for Zh based
        upon scattered radar parameters. It returns the scale and exponential
        parameter a and b in the first tuple, and the second returned argument
        gives the covariance matrix of the fit.
        '''

        popt, pcov = expfit(np.power(10, 0.1*self.Zh[self.rain_rate > 0]),
                            self.rain_rate[self.rain_rate > 0])
        return popt, pcov
