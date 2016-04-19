import numpy as np
from unittest import TestCase

from .. import read_parsivel_nasa_gv
import datetime

import os

class testParsivelNASAGVReader(TestCase):

    def test_read_file(self):
        ''' Test whether this function can read in the apu_nasa_mc3e_dsd.txt file in testdata.
        '''

        dsd = read_parsivel_nasa_gv('testdata/apu_nasa_mc3e_dsd.txt')
        self.assertIsNotNone(dsd, 'reader returned a None object')


    def test_reader_reads_in_time(self):
        ''' Test ParsivelNasaGVReader time handling capability. '''
        time_entries=3
        first_time_entry = datetime.datetime(2011,5,20,8,28)

        dsd = read_parsivel_nasa_gv('testdata/apu_nasa_mc3e_dsd.txt')
        self.assertEquals(time_entries, len(dsd.time['data']), "Incorrect number of time entries read in.")
        print(dsd.time['data'][0])

        self.assertEquals(first_time_entry, dsd.time['data'][0], "Initial time was incorrect")

