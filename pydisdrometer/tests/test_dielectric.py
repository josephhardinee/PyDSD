import numpy as np
import unittest

from ..utility import dielectric


class TestDielectricMethods(unittest.TestCase):

    def test_dielectric_is_roughly_093_at_S_water(self):
        perm = dielectric.get_refractivity(2.9e9,0)
        km = (perm**2-1)/(perm**2+2)
        d_c = np.abs(km)**2
        self.assertTrue(d_c-0.93 < 0.01)

if __name__ == '__main__':
    unittest.main()
