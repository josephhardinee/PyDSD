import numpy as np
from unittest import TestCase
import pydsd

from .. import read_parsivel_arm_netcdf
import datetime

import os


class testARMParsivelReader(TestCase):

    def setUp(self):
        filename = 'testdata/acxpars2S1.b1.20150124.000000.cdf'
        self.dsd = read_parsivel_arm_netcdf(filename)

    def test_read_file_does_not_return_none(self):
        ''' Test file acxpars2S1.b1.20150124.000000.cdf reads in and returns non None object.
        '''
        self.assertIsNotNone(self.dsd, 'reader returned a None object')

    def test_number_entries(self):
        """ Number of entries in acxpars2S1.b1.20150124.000000.cdf file is 1440 and consistent.
        """
        self.assertTrue(len(self.dsd.fields['Nd']['data']) == 1440)

    def test_has_1440_time_entries(self):
        self.assertTrue(len(self.dsd.time['data']) == 1440, "Test ARM APU File for ARMParsivelReader did not have 1440 time entries")
