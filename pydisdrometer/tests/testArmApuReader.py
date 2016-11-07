import unittest

from ..aux_readers.ArmApuReader import read_parsivel_arm_netcdf


class testArmApuReader(unittest.TestCase):

    acx_test_filename = 'testdata/acxpars2S1.b1.20150120.000000.cdf'

    def setUp(self):
        self.dsd = read_parsivel_arm_netcdf(self.acx_test_filename)

    def test_read_acx_file_worked(self):
        self.assertIsNotNone(self.dsd)

    def test_arm_apu_calculate_dsd(self):
        """
        Test whether we can calculate dsd parameters with the arm apu test file.

        """
        self.dsd.calculate_dsd_parameterization()


if __name__ == '__main__':
    unittest.main()
