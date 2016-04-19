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


