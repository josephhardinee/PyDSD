import pytest
import os.path

from ..aux_readers import ARM_Vdis_Reader
from ..io.NetCDFWriter import write_netCDF

@pytest.fixture
def two_dvd_file(tmpdir):
    filename_in = "testdata/arm_vdis_b1.cdf"
    filename_out = tmpdir + "test_2dvd.nc"
    dsd = ARM_Vdis_Reader.read_arm_vdis_b1(filename_in)
    write_netCDF(dsd, filename_out)
    return filename_out


class TestNetCDFWriter(object):
    """
    Test module for the ARM_Vdis_Reader"
    """

    @classmethod
    def setup_method(self, test_method):
        filename = "testdata/arm_vdis_b1.cdf"
        self.dsd = ARM_Vdis_Reader.read_arm_vdis_b1(filename)

    def test_opens_file(self, two_dvd_file):
        assert os.path.isfile(two_dvd_file)

    # def test_desktop_write(self):
    #     filename_in = "testdata/arm_vdis_b1.cdf"
    #     filename_out = '/Users/hard505/' + "test_2dvd.nc"
    #     dsd = ARM_Vdis_Reader.read_arm_vdis_b1(filename_in)
    #     dsd.calculate_dsd_parameterization()
    #     write_netCDF(dsd, filename_out)



