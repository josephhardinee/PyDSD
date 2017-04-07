import numpy as np
import unittest

import pydisdrometer.fit.ua98 as ua98
from ..fit import ua98

class TestDSDFits(unittest.TestCase):
    """ Test the various dsd fit functions ported from pyparticle probe. This
    needs some more extensive testing for correctness."""

    def test_ua98_eta_ratio_gives_correct_value(self):
        M2 = 2
        M4 = 2
        M6 = 2

        expected_eta = 1

        eta = ua98.eta_ratio(M2, M4, M6)
        self.assertTrue(np.isclose(eta,expected_eta),
                        "eta_ratio in ua98.returned an incorrect value for case (2,2,2):1")

    def test_ua98_shape_gives_correct_value(self):
        M2 = 1.0
        M4 = 2.0
        M6 = 3.0


        expected_shape =  -18.4462219947
        shape = ua98.shape(M2, M4, M6)
        self.assertTrue(np.isclose(shape,expected_shape),
                        "shape in ua98.returned an incorrect value for case (1,2,3)")

    def test_ua98_slope_gives_correct_value(self):
        M2 = 1.0
        M4 = 2.0
        mu = 3.0

        expected_slope = 4.582575694
        slope = ua98.slope(M2, M4, mu)
        self.assertTrue(np.isclose(slope,expected_slope, rtol=1e-5, atol=1e-5),
                        "slope in ua98.returned an incorrect value for case (1,2,3)")

    def test_ua98_intercept_gives_correct_value(self):
        M6 = 1.0
        mu = 3.0
        Lambda = 2.0

        expected_intercept = 0.00282186
        intercept = ua98.intercept(M6, mu, Lambda)
        self.assertTrue(np.isclose(intercept, expected_intercept, rtol=1e-5, atol=1e-5),
                        "intercept in ua98.returned an incorrect value for case (1,3,2)")

    def test_ua98_d0_gives_correct_value(self):
        mu = 3.0
        Lambda = 2.0

        expected_d0 = 3.335
        d0 = ua98.mom_d0(mu, Lambda)
        self.assertTrue(np.isclose(d0, expected_d0 ),
                        "mom_d0 in ua98.returned an incorrect value for case (3,2)")

    def test_ua98_zr_a_gives_correct_value(self):
        mu = 3.0
        N0 = 1e4

        expected_a = 80323.3609808
        a = ua98.zr_a(mu, N0)
        self.assertTrue(np.isclose(a, expected_a ),
                        "zr_a in ua98.returned an incorrect value for case (3,1e4)")

    def test_ua98_zr_b_gives_correct_value(self):
        mu = 3.0

        expected_b = 1.303780964797914
        b = ua98.zr_b(mu)
        self.assertTrue(np.isclose(b, expected_b ),
                        "zr_b in ua98.returned an incorrect value for case (3)")

    def test_ua98_norm_intercept_gives_correct_value(self):
        LWC = 1000
        Dm = 1.5

        expected_intercept =0.016096262886528476 

        intercept = ua98.norm_intercept(LWC, Dm)
        self.assertTrue(np.isclose(intercept, expected_intercept),
                        "norm_intercept in ua98.returned an incorrect value for case (1000,1.5)")


if __name__ == '__main__':
    unittest.main()
