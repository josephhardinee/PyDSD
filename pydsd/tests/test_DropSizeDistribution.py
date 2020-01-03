import pytest
import os.path
import numpy as np
import copy

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
    Test module for the DropSizeDistribution"
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

    def test_calculating_D0_with_nan_actually_works(self, two_dvd_open_test_file):
        two_dvd_open_test_file.fields["Nd"]["data"][0, 0] = np.nan  # Force a nan error
        two_dvd_open_test_file.fields["Nd"]["data"][0, 1] = 5

        two_dvd_open_test_file.calculate_dsd_parameterization()
        assert two_dvd_open_test_file.fields["D0"]["data"][0] != np.nan
        assert (
            two_dvd_open_test_file.fields["D0"]["data"][0]
            == two_dvd_open_test_file.diameter["data"][1]
        )

    def test_calculating_D0_returns_correct_values(self, two_dvd_open_test_file):
        two_dvd_open_test_file.fields["Nd"]["data"][0, 0] = 1  # Force a nan error
        two_dvd_open_test_file.fields["Nd"]["data"][0, 1] = 2
        two_dvd_open_test_file.calculate_dsd_parameterization()
        assert np.isclose(
            two_dvd_open_test_file.fields["D0"]["data"][0], .198, rtol=.01
        )  # One percent tolerance is closer than my hand calcs.

    @pytest.mark.dependency()
    def test_saving_of_scatter_table(self, two_dvd_open_test_file, tmpdir):
        two_dvd_open_test_file.calculate_radar_parameters()
        two_dvd_open_test_file.save_scattering_table(tmpdir+'/test_scatter.scatter')
        assert os.path.isfile(tmpdir+'/test_scatter.scatter')


    @pytest.mark.dependency(depends=['test_saving_of_scatter_table'])
    def test_reading_of_scatter_table(self, two_dvd_open_test_file, tmpdir):
        dsd_2 = copy.copy(two_dvd_open_test_file)
        dsd_2.calculate_radar_parameters()
        dsd_2.save_scattering_table(tmpdir+'/test_scatter.scatter')
        two_dvd_open_test_file.calculate_radar_parameters(scatter_table_filename = tmpdir+'/test_scatter.scatter')

