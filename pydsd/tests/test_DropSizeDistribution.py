import pytest
import os.path

from ..aux_readers import ARM_Vdis_Reader
from ..io.NetCDFWriter import write_netcdf
from .. import DropSizeDistribution


@pytest.fixture
def two_dvd_open_test_file(tmpdir):
    filename_in = "testdata/arm_vdis_b1.cdf"
    filename_out = tmpdir + "test_2dvd.nc"
    dsd = ARM_Vdis_Reader.read_arm_vdis_b1(filename_in)
    return dsd


class TestNetCDFWriter(object):
    """
    Test module for the ARM_Vdis_Reader"
    """

    @classmethod
    def setup_method(self, test_method):
        filename = "testdata/arm_vdis_b1.cdf"
        self.dsd = ARM_Vdis_Reader.read_arm_vdis_b1(filename)

    def test_changing_canting_angle_updates_value(self, two_dvd_open_test_file):
        two_dvd_open_test_file.set_canting_angle(15)
        assert two_dvd_open_test_file.scattering_params["canting_angle"] == 15

    def test_canting_angle_has_default_value(self, two_dvd_open_test_file):
        assert "canting_angle" in two_dvd_open_test_file.scattering_params.keys()
