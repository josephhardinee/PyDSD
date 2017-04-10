import numpy as np
import unittest
import matplotlib.pyplot as plt

from ..plot import plot
from ..aux_readers import ARM_JWD_Reader


class TestPlot(unittest.TestCase):
    'Test module for the plot scripts'

    def setUp(self):
        filename = 'testdata/sgpdisdrometerC1.b1.20110427.000000_test_jwd_b1.cdf'
        self.dsd = ARM_JWD_Reader.read_arm_jwd_b1(filename)

    def test_plot_dsd(self):
        fig, ax = plot.plot_dsd(self.dsd)
        plt.close()

    def test_plot_NwD0(self):
        self.dsd.calculate_dsd_parameterization() # Bad form to rely on this, but not a better way right now.
        fig, ax = plot.plot_NwD0(self.dsd)
        plt.close()

    def test_plot_ZR(self):
        self.dsd.calculate_radar_parameters()
        fig, ax = plot.plot_ZR(self.dsd)
        plt.close()

    def test_plot_ZR_hist2d(self):
        self.dsd.calculate_radar_parameters()
        fig, ax = plot.plot_ZR_hist2d(self.dsd)
        plt.close()

    def test_scatter(self):
        x = self.dsd.fields['rain_rate']['data'] #Visually not the best example, but avoids call to dsd parameterization
        y = self.dsd.fields['rain_rate']['data']
        fig, ax = plot.scatter(x, y)
        plt.close()

    def test_plot_hist2d(self):
        x = self.dsd.fields['rain_rate']['data']
        y = self.dsd.fields['rain_rate']['data']
        fig, ax = plot.plot_hist2d(x, y)
        plt.close()

    def test_plot_ts(self):
        fig, ax = plot.plot_ts(self.dsd, 'Nd')
        plt.close()

    def test_plotHov(self):
        self.dsd.calculate_dsd_parameterization() # Bad form to rely on this, but not a better way right now.
        fig, ax = plot.plotHov(self.dsd, 'D0', 'Nd')
        plt.close()

    def test_plot_hexbin(self):
        self.dsd.calculate_dsd_parameterization() # Bad form to rely on this, but not a better way right now.
        x = self.dsd.fields['Nd']['data']
        y = self.dsd.fields['D0']['data']
        fig, ax = plot.plot_hexbin(x, y)
        plt.close()

    def test_methods(self):
        # Should we test every submethod?
        fig, ax = plot.plot_dsd(self.dsd)
        plot.set_ax_limits(xlim=(0, 100), ylim=(0, 100), ax=ax)
        plt.close()

