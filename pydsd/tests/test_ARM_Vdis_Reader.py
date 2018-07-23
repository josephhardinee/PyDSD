import numpy as np
import unittest

from ..aux_readers import ARM_Vdis_Reader


class TestArmJwdReader(unittest.TestCase):
    """
    Test module for the ARM_Vdis_Reader"
    """

    def setUp(self):
        filename = "testdata/arm_vdis_b1.cdf"
        self.dsd = ARM_Vdis_Reader.read_arm_vdis_b1(filename)

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
        self.assertEqual(
            len(self.dsd.fields["rain_rate"]["data"]),
            1440,
            "Wrong number of time samples in rain rate",
        )

    def test_can_run_calc_dsd_params(self):
        self.dsd.calculate_dsd_parameterization()
        self.assertIsNotNone(
            self.dsd.fields["D0"],
            "The Field D0 did not exist after dsd_parameterization check",
        )
        self.assertEqual(
            len(self.dsd.fields["D0"]["data"]), 1440, "Wrong number of samples in D0"
        )

    def test_time_same_length_as_Nd(self):
        self.assertEqual(
            len(self.dsd.time["data"]),
            self.dsd.fields["Nd"]["data"].shape[0],
            "Different number of samples for time and Nd",
        )

    def test_time_is_in_epoch(self):
        self.assertEqual(
            self.dsd.time["data"][0], 1305590400
        )  # Basetime + first start time

    def test_spread_has_same_dimension_as_bins(self):
        """
        This is a regression test to determine if spread is correctly being
        set to the same size as the bins dimension of the Nd variable.
        """
        assert (
            self.dsd.spread["data"].shape[0] == self.dsd.fields["Nd"]["data"].shape[1]
        )
