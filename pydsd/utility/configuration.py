import json
from copy import copy
import os


class Configuration(object):
    """ Class to store PyDisdrometer configuration options

    Attributes:
    -----------

    """
    config_dir = os.path.dirname(os.path.abspath(__file__))
    metadata_config_file = os.path.join(config_dir, "metadata.json")

    def __init__(self):
        self.metadata = self.load_metadata_config()

    def load_metadata_config(self):
        """ Load the metadata configuration file and return the dictionary"""
        return json.load(open(self.metadata_config_file))

    def fill_in_metadata(self, field, data):
        metadata = self.metadata[field].copy()
        metadata["data"] = copy(data)
        return metadata
