import numpy as np
import unittest

from ..aux_readers import NASA_2DVD_reader

class TestNasa2DvdReaderMc3eSubcase(unittest.TestCase):
    'Test module for the NASA_2DVD_reader class in pydsd.aux_io.NASA_2DVD_reader for mc3e files'

    def setUp(self):
        filename = 'testdata/nasa_gv_mc3e_2dvd_test.txt'
        self.dsd = NASA_2DVD_reader.read_2dvd_dsd_nasa_gv(filename )

    def test_can_read_sample_file(self):
        self.assertIsNotNone(self.dsd, 'File did not read in correctly, returned None')

    def test_dsd_nd_exists(self):
        self.assertIsNotNone(self.dsd.fields['Nd'], 'DSD Object has no Nd field')

    def test_dsd_nd_is_dict(self):
        self.assertIsInstance(self.dsd.fields['Nd'], dict, 'Nd was not a dictionary.')

    def test_RR_works(self):
        self.dsd.calculate_RR()
        self.assertIsNotNone(self.dsd.fields['rain_rate'], 'Rain Rate is not in fields after calculate_RR()')
        self.assertEqual(len(self.dsd.fields['rain_rate']['data']), 5, 'Wrong number of time samples in rain rate')

    def test_can_run_calc_dsd_params(self):
        self.dsd.calculate_dsd_parameterization()
        self.assertIsNotNone(self.dsd.fields['D0'], 'The Field D0 did not exist after dsd_parameterization check')
        self.assertEqual(len(self.dsd.fields['D0']['data']), 5, 'Wrong number of samples in D0')

    def test_time_same_length_as_Nd(self):
        self.assertEqual(len(self.dsd.time['data']), self.dsd.fields['Nd']['data'].shape[0], 'Different number of samples for time and Nd')


