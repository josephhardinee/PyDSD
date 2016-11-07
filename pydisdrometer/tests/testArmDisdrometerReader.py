import unittest

from ..aux_readers.ArmDisdrometerReader import read_disdrometer_arm_netcdf


class testArmDisdrometerReader(unittest.TestCase):

    test_filename = 'testdata/arm_disdrometer_b1.cdf'

    def setUp(self):
        self.dsd = read_disdrometer_arm_netcdf(self.test_filename)

    def test_read_test_file_worked(self):
        self.assertIsNotNone(self.dsd)

    def test_ArmDisdrometerDsdEstimationWorks(self):
        self.dsd.calculate_dsd_parameterization()
        self.assertTrue("D0" in self.dsd.fields.keys())

if __name__ == '__main__':
    unittest.main()
