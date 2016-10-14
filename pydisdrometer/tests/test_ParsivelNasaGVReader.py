import numpy as np
from unittest import TestCase
import pydisdrometer

from .. import read_parsivel_nasa_gv
import datetime

import os


class TestParsivelNASAGVReader(TestCase):

    def setUp(self):
        self.dsd = read_parsivel_nasa_gv('testdata/apu_nasa_mc3e_dsd.txt')

    def test_read_file(self):
        ''' Test file apu_nasa_mc3e_dsd.txt reads in and returns non None object.
        '''
        print(type(self.dsd))

        self.assertIsNotNone(self.dsd, 'reader returned a None object')

    def test_number_entries(self):
        """ Number of entries in apu_nasa_mc3e_dsd.txt file is 5 and consistent.
        """
        self.assertTrue(len(self.dsd.Nd['data'])) == 5
