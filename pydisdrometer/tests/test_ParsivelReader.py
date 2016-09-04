import numpy as np
import unittest

from ..io import ParsivelReader

class TestParsivelReader(unittest.TestCase):
    'Test module for the ParsivelReader class in pydisdrometer.io.ParsivelReader'

    def setUp(self):
        filename = 'testdata/parsivel_telegraph_testfile.mis'
        self.dsd = ParsivelReader.read_parsivel(filename)

    def test_can_read_sample_file(self):
        self.assertIsNotNone(self.dsd, 'File did not read in correctly, returned None')

    def test_dsd_nd_exists(self):
        self.assertIsNotNone(self.dsd.fields['Nd'], 'DSD Object has no Nd field')

    def test_dsd_nd_is_dict(self):
        self.assertIsInstance(self.dsd.fields['Nd'], dict, 'Nd was not a dictionary.')

    def test_RR_works_on_Parsivel(self):
        self.dsd.calculate_RR()
        self.assertIsNotNone(self.dsd.fields['rain_rate'], 'Rain Rate is not in fields after calculate_RR()')
        self.assertEqual(len(self.dsd.fields['rain_rate']['data']), 6, 'Wrong number of time samples in rain rate')

    def test_can_run_calc_dsd_params(self):
        self.dsd.calculate_dsd_parameterization()
        self.assertIsNotNone(self.dsd.fields['D0'], 'The Field D0 did not exist after dsd_parameterization check')
        self.assertEqual(len(self.dsd.fields['D0']['data']), 6, 'Wrong number of samples in D0')

    def test_time_same_length_as_Nd(self):
        self.assertEqual(len(self.dsd.time['data']), self.dsd.fields['Nd']['data'].shape[0])


