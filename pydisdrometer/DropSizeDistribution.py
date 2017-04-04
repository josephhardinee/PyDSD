# -*- coding: utf-8 -*-
'''
The Drop Size Distribution model contains the DropSizeDistribution class.
This class represents drop size distributions returned from the various
readers in the io module. The class knows how to perform scattering
simulations on itself.
'''

import numpy as np
import pytmatrix
import scipy
from scipy.optimize import curve_fit

from pytmatrix.tmatrix import Scatterer
from pytmatrix.psd import PSDIntegrator
from pytmatrix import orientation, radar, tmatrix_aux, refractive
from datetime import date
from .utility.expfit import expfit, expfit2

from . import DSR
from .utility import dielectric
from .utility import configuration
SPEED_OF_LIGHT=299792458

class DropSizeDistribution(object):

    '''
    DropSizeDistribution class to hold DSD's and calculate parameters
    and relationships. Should be returned from the disdrometer*reader style
    functions.

    Attributes
    ----------
        time: array_like
            An array of times corresponding to the time each dsd was sampled in minutes relative to time_start.
        time_start: datetime
            A datetime object indicated start of disdrometer recording.
        fields: dictionary
            Dictionary of scattered components.
        Nd : 2d Array
            A list of drop size distributions
        spread: array_like
            Array giving the bin spread size for each size bin of the
            disdrometer.
        velocity: array_like
            Terminal Fall Velocity for each size bin. This is based on the
            disdrometer assumptions.
        Z: array_like
            The equivalent reflectivity factory from the disdrometer. Often
            taken as D**6.

        bin_edges: array_like
            N+1 sized array of the boundaries of each size bin. For 30 bins
            for instance, there will be 31 different bin boundaries.
        diameter: array_like
            The center size for each dsd bin.

    '''

    def __init__(self, reader, time_start = None, location=None):
        '''Initializer for the DropSizeDistribution class.

        The DropSizeDistribution class holds dsd's returned from the various
        readers in the io module.

        Parameters
        ----------
        reader: object
            Object returned by package readers.
        time_start: datetime
            Recording Start time.
        location: tuple
            (Latitude, Longitude) pair in decimal format.

        Returns
        -------
        dsd: `DropSizeDistribution` instance
            Drop Size Distribution instance.

        '''

        self.config = configuration.Configuration() 

        self.time = reader.time
        self.Nd = reader.fields['Nd']
        self.spread = reader.spread
        try:
            self.rain_rate = reader.fields['rain_rate']
        except:
            self.rain_rate = None
        try:
            self.velocity = reader.fields['terminal_velocity']
        except:
            self.velocity = None
        try:
            self.Z = reader.fields['reflectivity']
        except:
            self.Z = None
        try:
            self.num_particles = reader.fields['num_particles']
        except:
            self.num_particles = None
        try:
            self.bin_edges = reader.bin_edges
        except:
            self.bin_edges = None
        try:
            self.diameter = reader.diameter
        except:
            self.diameter = None
        self.fields = reader.fields
        self.time_start = time_start

        try:
            self.info = reader.info
        except:
            self.info = {}

        self.numt = len(reader.time['data'])
        location = {}

        if location:
            self.location = {'latitude': location[0], 'longitude': location[1]}

        self.set_scattering_temperature_and_frequency()

    def set_scattering_temperature_and_frequency(self, scattering_temp=10, scattering_freq = 9.7e9):
        ''' Change the scattering temperature. After use, re-run calculate_radar_parameters
        to see the effect this has on the parameters. Temperatures are in Celsius. Defaults to 10C X-band.

        Parameters
        ----------
        scattering_temp: optional, float
            Scattering temperature [C].
        scattering_freq: optional, float
            Scattering frequency [Hz].
        '''
        self.scattering_freq = scattering_freq
        self.scattering_temp = scattering_temp
        self.m_w = dielectric.get_refractivity(scattering_freq, scattering_temp)


    def calculate_radar_parameters(self, dsr_func = DSR.bc, scatter_time_range = None ):
        ''' Calculates radar parameters for the Drop Size Distribution.

        Calculates the radar parameters and stores them in the object.
        Defaults to X-Band,Beard and Chuang 10C setup.

        Sets the dictionary parameters in fields dictionary:
            Zh, Zdr, Kdp, Ai(Attenuation)

        Parameters:
        ----------
            wavelength: optional, pytmatrix wavelength
                Wavelength to calculate scattering coefficients at.
            dsr_func: optional, function
                Drop Shape Relationship function. Several are availab le in the `DSR` module.
                Defaults to Beard and Chuang
            scatter_time_range: optional, tuple
                Parameter to restrict the scattering to a time interval. The first element is the start time,
                while the second is the end time.
        '''
        self._setup_scattering(SPEED_OF_LIGHT/self.scattering_freq*1000.0, dsr_func)
        self._setup_empty_fields()

        if scatter_time_range is None:
            self.scatter_start_time = 0
            self.scatter_end_time = self.numt
        else:
            if scatter_time_range[0] < 0:
                print("Invalid Start time specified, aborting")
                return
            self.scatter_start_time = scatter_time_range[0]
            self.scatter_end_time = scatter_time_range[1]

            if scatter_time_range[1] > self.numt:
                print("End of Scatter time is greater than end of file. Scattering to end of included time.")
                self.scatter_end_time = self.numt

        self.scatterer.set_geometry(tmatrix_aux.geom_horiz_back) # We break up scattering to avoid regenerating table.

        for t in range(self.scatter_start_time, self.scatter_end_time):
            if np.sum(self.Nd['data'][t]) is 0:
                continue
            BinnedDSD = pytmatrix.psd.BinnedPSD(self.bin_edges['data'],  self.Nd['data'][t])
            self.scatterer.psd = BinnedDSD
            self.fields['Zh']['data'][t] = 10 * \
                np.log10(radar.refl(self.scatterer))
            self.fields['Zdr']['data'][t] = 10 * \
                np.log10(radar.Zdr(self.scatterer))

        self.scatterer.set_geometry(tmatrix_aux.geom_horiz_forw)

        for t in range(self.scatter_start_time, self.scatter_end_time):
            BinnedDSD = pytmatrix.psd.BinnedPSD(self.bin_edges['data'],  self.Nd['data'][t])
            self.scatterer.psd = BinnedDSD
            self.fields['Kdp']['data'][t] = radar.Kdp(self.scatterer)
            self.fields['Ai']['data'][t] = radar.Ai(self.scatterer)
            self.fields['Adr']['data'][t] = radar.Ai(self.scatterer) -radar.Ai(self.scatterer, h_pol=False)

    def _setup_empty_fields(self ):
        ''' Preallocate arrays of zeros for the radar moments
        '''
        params_list = ['Zh', 'Zdr', 'Kdp', 'Ai', 'Adr']

        for param in params_list:
            self.fields[param] = self.config.fill_in_metadata(param, np.ma.zeros(self.numt))

    def _setup_scattering(self, wavelength, dsr_func):
        ''' Internal Function to create scattering tables.

        This internal function sets up the scattering table. It takes a
        wavelength as an argument where wavelength is one of the pytmatrix
        accepted wavelengths.

        Parameters:
        -----------
            wavelength : tmatrix wavelength
                PyTmatrix wavelength.
            dsr_func : function
                Drop Shape Relationship function. Several built-in are available in the `DSR` module.

        '''
        self.scatterer = Scatterer(wavelength=wavelength,
                                   m=self.m_w)
        self.scatterer.psd_integrator = PSDIntegrator()
        self.scatterer.psd_integrator.axis_ratio_func = lambda D: 1.0 / \
            dsr_func(D)
        self.dsr_func = dsr_func
        self.scatterer.psd_integrator.D_max = 10.0
        self.scatterer.psd_integrator.geometries = (
            tmatrix_aux.geom_horiz_back, tmatrix_aux.geom_horiz_forw)
        self.scatterer.or_pdf = orientation.gaussian_pdf(20.0)
        self.scatterer.orient = orientation.orient_averaged_fixed
        self.scatterer.psd_integrator.init_scatter_table(self.scatterer)

    def _calc_mth_moment(self, m):
        '''Calculates the mth moment of the drop size distribution.

        Returns the mth moment of the drop size distribution E[D^m].

        Parameters:
        -----------
        m: float
            order of the moment
        '''

        if len(self.spread['data']) > 0:
            bin_width = self.spread['data']
        else:
            bin_width = [self.bin_edges['data'][i + 1] - self.bin_edges['data'][i]
                     for i in range(0, len(self.bin_edges['data']) - 1)]
        mth_moment = np.ma.zeros(self.numt)

        for t in range(0, self.numt):
            dmth = np.power(self.diameter['data'], m)
            mth_moment[t] = np.dot(np.multiply(dmth, self.Nd['data'][t]), bin_width)

        return mth_moment

    def calculate_dsd_parameterization(self, method='bringi'):
        '''Calculates DSD Parameterization.

        This calculates the dsd parameterization and stores the result in the fields dictionary.
        This includes the following parameters:
        Nt, W, D0, Nw, Dmax, Dm, N0, mu

        Parameters:
        -----------
        method: optional, string
            Method to use for DSD estimation


        Further Info:
        ------
        For D0 and Nw we use the method due to Bringi and Chandrasekar.

        '''

        params_list = ['D0', 'Dmax', 'Dm', 'Nt', 'Nw', 'N0', 'W', 'mu']

        for param in params_list:
            self.fields[param] = self.config.fill_in_metadata(param, np.ma.zeros(self.numt))

        rho_w = 1e-03  # grams per mm cubed Density of Water
        vol_constant = np.pi / 6.0 * rho_w
        self.fields['Dm']['data'] = np.divide(self._calc_mth_moment(4), self._calc_mth_moment(3))
        for t in range(0, self.numt):
            if np.sum(self.Nd['data'][t]) == 0:
                continue
            self.fields['Nt']['data'][t] = np.dot(self.spread['data'], self.Nd['data'][t])
            self.fields['W']['data'][t] = vol_constant * np.dot(np.multiply(self.Nd['data'][t], self.spread['data']),
                                                                np.array(self.diameter['data']) ** 3)
            self.fields['D0']['data'][t] = self._calculate_D0(self.Nd['data'][t])
            self.fields['Nw']['data'][t] =  256.0 / \
                (np.pi * rho_w) * np.divide(self.fields['W']['data'][t],
                                            self.fields['Dm']['data'][t] ** 4)

            self.fields['Dmax']['data'][t] = self.__get_last_nonzero(self.Nd['data'][t])

        self.fields['mu']['data'][:] = list(map(self._estimate_mu,
                                                list(range(0,self.numt))))

    def __get_last_nonzero(self, N):
        ''' Gets last nonzero entry in an array. Gets last non-zero entry in an array.

        Parameters
        ----------
        N: array_like
            Array to find nonzero entry in

        Returns
        -------
        max: int
            last nonzero entry in an array.
        '''

        if np.ma.count(N):
            return self.diameter['data'][np.max(N.nonzero())]
        else:
            return 0

    def _calculate_D0(self, N):
        ''' Calculate Median Drop diameter.

        Calculates the median drop diameter for the array N. This assumes diameter and bin widths in the
        dsd object have been properly set.

        Parameters:
        -----------
        N: array_like
            Array of drop counts for each size bin.

        Notes:
        ------
        This works by calculating the two bins where cumulative water content goes over 0.5, and then interpolates
        the correct D0 value between these two bins.
        '''

        rho_w = 1e-3
        W_const = rho_w * np.pi / 6.0

        if np.sum(N) == 0:
            return 0

        cum_W = W_const * \
            np.cumsum([N[k] * self.spread['data'][k] * (self.diameter['data'][k] ** 3)
                       for k in range(0, len(N))])
        cross_pt = list(cum_W < (cum_W[-1] * 0.5)).index(False) - 1
        slope = (cum_W[cross_pt + 1] - cum_W[cross_pt]) / \
            (self.diameter['data'][cross_pt + 1] - self.diameter['data'][cross_pt])
        run = (0.5 * cum_W[-1] - cum_W[cross_pt]) / slope
        return self.diameter['data'][cross_pt] + run

    def calculate_RR(self):
        '''Calculate instantaneous rain rate.

        This calculates instantaneous rain rate based on the flux of water.
        '''
        self.fields['rain_rate'] = {'data': np.ma.zeros(self.numt)}
        for t in range(0, self.numt):
            # self.rain_rate['data'][t] = 0.6*3.1415 * 10**(-3) * np.dot(np.multiply(self.rain_rate['data'],np.multiply(self.Nd['data'][t],self.spread['data'] )),
            #    np.array(self.diameter['data'])**3)
            velocity = 9.65 - 10.3 * np.exp(-0.6 * self.diameter['data'])
            velocity[0] = 0.5
            self.fields['rain_rate']['data'][t] = 0.6 * np.pi * 1e-03 * np.sum(self._mmultiply(
                velocity, self.Nd['data'][t], self.spread['data'], np.array(self.diameter['data']) ** 3))

    def calculate_R_Kdp_relationship(self):
        '''
        calculate_R_kdp_relationship calculates a power fit for the rainfall-kdp
        relationship based upon the calculated radar parameters(which should
        have already been run). It returns the scale and exponential
        parameter a and b in the first tuple, and the second returned argument
        gives the covariance matrix of the fit.
        '''

        if 'rain_rate' in list(self.fields.keys()):
            filt = np.logical_and(
                self.fields['Kdp']['data'] > 0, self.fields['rain_rate']['data'] > 0)
            popt, pcov = expfit(self.fields['Kdp']['data'][filt],
                                self.fields['rain_rate']['data'][filt])

            return popt, pcov
        else:
            print("Please run calculate_RR() function first.")
            return None

    def calculate_R_Zh_relationship(self):
        '''
        calculate_R_Zh_relationship calculates the power law fit for Zh based
        upon scattered radar parameters. It returns the scale and exponential
        parameter a and b in the first tuple, and the second returned argument
        gives the covariance matrix of the fit.

        Returns:
        --------
        popt: tuple
            a,b,c fits for relationship.
        pcov: array
            Covariance matrix of fits.
        '''

        popt, pcov = expfit(np.power(10, 0.1 * self.fields['Zh']['data'][self.rain_rate['data'] > 0]),
                            self.fields['rain_rate']['data'][self.fields['rain_rate']['data'] > 0])
        return popt, pcov

    def calculate_R_Zh_Zdr_relationship(self):
        '''
        calculate_R_Zh_Zdr_relationship calculates the power law fit for Zh,Zdr
        based upon scattered radar parameters. It returns the scale and
        exponential parameters a, b, and c in the first tuple, and the
        second returned argument gives the covariance matrix of the fit.
        Uses a set of filters to remove bad data:
        rain_rate > 0
        Zdr > 0
        Kdp > 0
        '''

        filt = np.logical_and(
            np.logical_and(self.fields['rain_rate']['data'] > 0, np.greater(self.fields['Zdr']['data'], 0)), self.fields['Kdp']['data'] > 0)
        popt, pcov = expfit2([self._idb(self.fields['Zh']['data'][filt]),
                              self._idb(self.fields['Zdr']['data'][filt])],
                             self.fields['rain_rate']['data'][filt])
        return popt, pcov

    def calculate_R_Zh_Kdp_relationship(self):
        '''
        calculate_R_Zh_Kdp_relationship calculates the power law fit for Zh,Kdp
        based upon scattered radar parameters. It returns the scale and
        exponential parameters a, b, and c in the first tuple, and the
        second returned argument gives the covariance matrix of the fit.
        rain_rate > 0
        Zdr > 0
        Kdp > 0
        '''

        filt = np.logical_and(
            np.logical_and(self.fields['rain_rate']['data'] > 0, self.fields['Zdr']['data'] > 0), self.fields['Kdp']['data'] > 0)
        popt, pcov = expfit2([self._idb(self.fields['Zh']['data'][filt]),
                              self.fields['Kdp']['data'][filt]],
                             self.fields['rain_rate']['data'][filt])
        return popt, pcov

    def calculate_R_Zdr_Kdp_relationship(self):
        '''
        calculate_R_Zdr_Kdp_relationship calculates the power law fit for Zdr,Kdp
        based upon scattered radar parameters. It returns the scale and
        exponential parameters a, b, and c in the first tuple, and the
        second returned argument gives the covariance matrix of the fit.
        rain_rate > 0
        Zdr > 0
        Kdp > 0
        '''

        filt = np.logical_and(np.logical_and(self.fields['rain_rate']['data'] > 0, self.fields['Zdr']['data'] > 0),
                              self.fields['Kdp']['data'] > 0)

        popt, pcov = expfit2([self._idb(self.fields['Zdr']['data'][filt]),
                              self.fields['Kdp']['data'][filt]],
                             self.fields['rain_rate']['data'][filt])
        return popt, pcov

    def _idb(self, db):
        '''
        Converts dB to linear scale.
        '''
        return np.power(10, np.multiply(0.1, db))

    def _mmultiply(self, *args):
        '''
        _mmultiply extends numpy multiply to arbitrary number of same
        sized matrices. Multiplication is elementwise.

        Parameters:
        -----------
        *args: matrices
            Matrices to multiply. Must be same shape.
        '''
        i_value = np.ones(len(args[0]))
        for i in args:
            i_value = np.multiply(i_value, i)

        return i_value

    def _estimate_mu(self, idx):
        """ Estimate $\mu$ for a single drop size distribution

        Estimate the shape parameter $\mu$ for the drop size distribution `Nd`. This uses the method
        due to Bringi and Chandrasekar. It is a minimization of the MSE error of a created gamma and
        measured DSD.

        Parameters
        ----------
        Nd : array_like
            A drop size distribution
        D0: optional, float
            Median drop diameter in mm. If none is given, it will be estimated.
        Nw: optional, float
            Normalized Intercept Parameter. If none is given, it will be estimated.

        Returns
        -------
        mu: integer
            Best estimate for DSD shape parameter $\mu$.
        """
        if np.sum(self.Nd['data'][idx]) == 0 :
            return np.nan
        res = scipy.optimize.minimize_scalar(self._mu_cost, bounds = (-10,20), args = (idx,), method='bounded')
        if self._mu_cost(res.x, idx) == np.nan or res.x > 20:
            return np.nan
        else:
            return res.x

    def _mu_cost(self, mu, idx):
        """ Cost function for goodness of fit of a distribution.

        Calculates the MSE cost comparison of two distributions to fit $\mu$.

        Parameters
        ----------
        idx: integer
            index into DSD field
        mu: float
            Potential Mu value
        """

        gdsd  = pytmatrix.psd.GammaPSD(self.fields['D0']['data'][idx], self.fields['Nw']['data'][idx],mu)
        return np.sqrt(np.nansum(np.power(np.abs(self.Nd['data'][idx] - gdsd(self.diameter['data'])),2)))


