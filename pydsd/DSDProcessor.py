from __future__ import division
import numpy as np
from pytmatrix.tmatrix import Scatterer
from pytmatrix.psd import PSDIntegrator, GammaPSD
from pytmatrix import orientation, radar, tmatrix_aux, refractive
from . import DSR


class DSDProcessor:

    def calcParameters(self, D0, Nw, mu):
        self.moments = {}
        self.scatterer.psd = GammaPSD(D0=D0, Nw=10 ** (Nw), mu=mu)
        self.scatterer.set_geometry(tmatrix_aux.geom_horiz_back)
        self.moments["Zh"] = 10 * np.log10(radar.refl(self.scatterer))
        self.moments["Zdr"] = 10 * np.log10(radar.Zdr(self.scatterer))
        self.moments["delta_hv"] = radar.delta_hv(self.scatterer)
        self.moments["ldr_h"] = radar.ldr(self.scatterer)
        self.moments["ldr_v"] = radar.ldr(self.scatterer, h_pol=False)

        self.scatterer.set_geometry(tmatrix_aux.geom_horiz_forw)
        self.moments["Kdp"] = radar.Kdp(self.scatterer)
        self.moments["Ah"] = radar.Ai(self.scatterer)
        self.moments["Adr"] = self.moments["Ah"] - radar.Ai(self.scatterer, h_pol=False)
        return self.moments

    def __init__(self, wl=tmatrix_aux.wl_X, dr=1, shape="bc"):
        DSR_list = {"tb": DSR.tb, "bc": DSR.bc, "pb": DSR.pb}

        self.scatterer = Scatterer(wavelength=wl, m=refractive.m_w_10C[wl])
        self.scatterer.psd_integrator = PSDIntegrator()
        self.scatterer.psd_integrator.axis_ratio_func = lambda D: 1.0 / DSR_list[shape](
            D
        )
        self.scatterer.psd_integrator.D_max = 10.0
        self.scatterer.psd_integrator.geometries = (
            tmatrix_aux.geom_horiz_back, tmatrix_aux.geom_horiz_forw
        )
        self.scatterer.or_pdf = orientation.gaussian_pdf(20.0)
        self.scatterer.orient = orientation.orient_averaged_fixed
        self.scatterer.psd_integrator.init_scatter_table(self.scatterer)
        self.dr = dr
