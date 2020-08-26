import numpy as np
import unittest

from ..io import ARM_vdisdrops_reader


class TestArmVdisdrops_reader(unittest.TestCase):
    """
    Test module for the ARM_Vdis_drops_Reader"
    """

    def setUp(self):
        filename = "testdata/corvdisdropsM1.b1.20181214.020816.cdf"
        self.dsd = ARM_vdisdrops_reader.read_arm_vdisdrops_netcdf(filename)

    def test_can_read_sample_file(self):
        self.assertIsNotNone(self.dsd, "File did not read in correctly, returned None")

    def test_dsd_nd_exists(self):
        self.assertIsNotNone(self.dsd.fields["Nd"], "DSD Object has no Nd field")

    def test_dsd_nd_is_dict(self):
        self.assertIsInstance(self.dsd.fields["Nd"], dict, "Nd was not a dictionary.")

    def test_RR_works(self):
        self.dsd.calculate_RR()
        self.assertIsNotNone(
            self.dsd.fields["rain_rate"],
            "Rain Rate is not in fields after calculate_RR()",
        )


    def test_can_run_calc_dsd_params(self):
        self.dsd.calculate_dsd_parameterization()
        self.assertIsNotNone(
            self.dsd.fields["D0"],
            "The Field D0 did not exist after dsd_parameterization check",
        )

    def test_time_same_length_as_Nd(self):
        self.assertEqual(
            len(self.dsd.time["data"]),
            self.dsd.fields["Nd"]["data"].shape[0],
            "Different number of samples for time and Nd",
        )

    def test_spread_has_same_dimension_as_bins(self):
        """
        This is a regression test to determine if spread is correctly being
        set to the same size as the bins dimension of the Nd variable.
        """
        assert (
            self.dsd.spread["data"].shape[0] == self.dsd.fields["Nd"]["data"].shape[1]
        )
