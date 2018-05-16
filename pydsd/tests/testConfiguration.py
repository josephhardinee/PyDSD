# -*- coding: utf-8 -*-

import numpy as np
import unittest
from ..utility import configuration

from .. import DropSizeDistribution


class testConfiguration(unittest.TestCase):
    """ Unit tests for Configuration Class"""

    def setUp(self):
        self.config = configuration.Configuration()

    def test_config_loads_and_has_keys(self):
        self.assertIsNotNone(self.config)
        self.assertTrue(len(self.config.metadata.keys()) > 0)
