import numpy as np
from unittest import TestCase

from .. import read_noaa_aoml_netcdf, read_ucsc_netcdf


class TestUCSCReader(TestCase):
    """ Test class for USCS Reader
    """

    def setUp(self):
        self.dsd = read_ucsc_netcdf('testdata/noaa_p3_pip_test.20170101.nc')

    def test_read_did_not_return_none(self):
        self.assertIsNotNone(self.dsd, "UCSC Reader returned a none object")

    def test_time_has_units_string(self):
        self.assertTrue('units' in self.dsd.time.keys())


class TestNOAAAOMLReader(TestCase):
    """ Test class for NOAA AOML Reader
    """

    def setUp(self):
        self.dsd = read_noaa_aoml_netcdf('testdata/aoml_pip_test.nc')

    def test_read_did_not_return_none(self):
        self.assertIsNotNone(self.dsd, "AOML Pip Reader Returned a None Object")

    def test_dsd_has_3_entries(self):
        self.assertTrue(len(self.dsd.Nd['data']) == 3)
