from ..utility import expfit
from unittest import TestCase
import numpy as np


class Test_expfit(TestCase):
    ''' Tests for the expfit module. '''

    def test_expfit_returns_correct_relationship(self):
        '''
        Test whether or not expfit can model a simple one variable exponential relationship.
        '''

        a = 2
        b = 3
        x = [1, 2, 3]
        y = a * np.power(x, b)
        fit = expfit.expfit(x, y)[0]
        self.assertAlmostEqual(fit[0], a, 7,
                               "Fit of Scale Parameter Failed for expfit")
        self.assertAlmostEqual(fit[1], b, 7,
                               "Fit of Exponent Parameter Failed for expfit")

    def test_expfit_handles_nan(self):
        ''' Test whether expfit correctly handles not a number in input array.'''

        a = 2
        b = 3
        x = [1, 2, 3, np.nan]
        y = a * np.power(x, b)
        fit = expfit.expfit(x, y)[0]
        self.assertAlmostEqual(
            fit[0], a, 7,
            "Fit of Scale Parameter Failed for expfit with nan data")
        self.assertAlmostEqual(
            fit[1], b, 7,
            "Fit of Exponent Parameter Failed for expfit with nan data")

    def test_expfit2_returns_correct_relationship(self):
        '''
        Test whether or not expfit2 can model a simple two variable exponential relationship.
        '''

        a = 1.5
        b = 2.5
        c = 3.5
        x1 = np.array([1, 2, 3, 4, 5])
        x2 = 2 * np.array([1, 3, 5, 7, 9])
        y = a * np.power(x1, b) * np.power(x2, c)
        fit = expfit.expfit2([x1, x2], y)[0]
        self.assertAlmostEqual(fit[0], a, 7,
                               "Fit of Scale Parameter Failed for expfit")
        self.assertAlmostEqual(
            fit[1], b, 7, "Fit of First Exponent Parameter Failed for expfit2")
        self.assertAlmostEqual(
            fit[2], c, 7,
            "Fit of Second Exponent Parameter Failed for expfit2")

    def test_expfit2_handles_nan(self):
        '''
        Test whether or not expfit2 can model a simple two variable exponential relationship in
        the presence of nans.
        '''
        a = 1.5
        b = 2.5
        c = 3.5
        x1 = np.array([1, 2, 3, np.nan, 5, 7, 9, 11, 12])
        x2 = 2 * np.array([1, 3, 5, 7, np.nan, 9, 11, 12, 1])
        y = a * np.power(x1, b) * np.power(x2, c)
        fit = expfit.expfit2([x1, x2], y)[0]
        self.assertAlmostEqual(fit[0], a, 7,
                               "Fit of Scale Parameter Failed for expfit")
        self.assertAlmostEqual(
            fit[1], b, 7, "Fit of First Exponent Parameter Failed for expfit2")
        self.assertAlmostEqual(
            fit[2], c, 7,
            "Fit of Second Exponent Parameter Failed for expfit2")
