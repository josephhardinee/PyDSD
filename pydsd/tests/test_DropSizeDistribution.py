import numpy as np
import pytest

from ..aux_readers import ARM_Vdis_Reader

@pytest.fixture
def two_dvd_test_file(tmpdir):
    filename_in = "testdata/arm_vdis_b1.cdf"
    filename_out = tmpdir + "test_2dvd.nc"
    dsd = ARM_Vdis_Reader.read_arm_vdis_b1(filename_in)
    return dsd


class TestDropSizeDistribution(object):
    """
    Test module for the ARM_Vdis_Reader"
    """

    def test_scattering_creates_fields_entries(self, two_dvd_test_file):
        params_list = ["Zh", "Zdr", "Kdp", "Ai", "Adr", "delta_hv", "rho_hv"]
        two_dvd_test_file.calculate_radar_parameters()
        for param in params_list:
            assert param in two_dvd_test_file.fields.keys()
