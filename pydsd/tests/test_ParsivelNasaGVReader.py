import numpy as np
from unittest import TestCase
import pydsd

from .. import read_parsivel_nasa_gv
import datetime

import os


class TestParsivelNASAGVReader(TestCase):

    def setUp(self):
        self.dsd = read_parsivel_nasa_gv('testdata/apu_nasa_mc3e_dsd.txt')

    def test_read_file_does_not_return_none(self):
        ''' Test file apu_nasa_mc3e_dsd.txt reads in and returns non None object.
        '''
        self.assertIsNotNone(self.dsd, 'reader returned a None object')

    def test_number_entries(self):
        """ Number of entries in apu_nasa_mc3e_dsd.txt file is 5 and consistent.
        """
        self.assertTrue(len(self.dsd.Nd['data'])) == 3

    def test_has_10_time_entries(self):
        self.assertTrue(len(self.dsd.time['data']) == 3, "Test MC3E File for ParsivelNASAGVReader did not have 3 time entries")


class TestParsivelNASAGVReader_ifloods(TestCase):

    def setUp(self):
        self.dsd = read_parsivel_nasa_gv('testdata/nasa_gv_ifloods_apu_test.txt')

    def test_read_file_does_not_return_none(self):
        ''' Test file apu_nasa_mc3e_dsd.txt reads in and returns non None object.
        '''
        self.assertIsNotNone(self.dsd, 'reader returned a None object')

    def test_number_entries(self):
        """ Number of entries in apu_nasa_mc3e_dsd.txt file is 10 and consistent.
        """
        self.assertTrue(len(self.dsd.Nd['data'])) == 10

    def test_has_10_time_entries(self):
        self.assertTrue(len(self.dsd.time['data']) == 10, "Test ifloods File for ParsivelNASAGVReader did not have 10 time entries")


