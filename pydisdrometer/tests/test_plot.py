import numpy as np
import unittest

from ..plot import plot


class TestPlot(unittest.TestCase):
    'Test module for the plot scripts'

    def setUp(self):
        filename = 'testdata/sgpdisdrometerC1.b1.20110427.000000_test_jwd_b1.cdf'
        self.dsd = ARM_JWD_Reader.read_arm_jwd_b1(filename)

    def test_plot_dsd(self):
        fig, ax = plot.plot_dsd(self.dsd)
        plt.close()

    def test_plot_NwD0(self):
        fig, ax = plot.plot_NwD0(self.dsd)
        plt.close()

    def test_plot_ZR(self):
        fig, ax = plot.plot_ZR(self.dsd)
        plt.close()

    def test_plot_ZR_hist2d(self):
        fig, ax = plot.plot_ZR_hist2d(self.dsd)
        plt.close()

    def test_scatter(self):
        x = self.dsd['Nd']['data']
        y = self.dsd['D0']['data']
        fig, ax = plot.scatter(x, y)
        plt.close()

    def test_plot_hist2d(self):
        x = self.dsd['Nd']['data']
        y = self.dsd['D0']['data']
        fig, ax = plot.plot_hist2d(x, y)
        plt.close()

    def test_plot_ts(self):
        fig, ax = plot.plot_ts(self.dsd, 'Nd')
        plt.close()

    def test_plotHov(self):
        fig, ax = plot.plotHov(self.dsd, 'D0', 'Nd')
        plt.close()

    def test_plot_hexbin(self):
        x = self.dsd['Nd']['data']
        y = self.dsd['D0']['data']
        fig, ax = plot.plot_hexbin(x, y)
        plt.close()

    def test_methods(self):
        # Should we test every submethod?
        fig, ax = plot.plot_dsd(self.dsd)
        plot.set_ax_limits(xlim=(0, 100), ylim=(0, 100), ax=ax)
        plt.close()

