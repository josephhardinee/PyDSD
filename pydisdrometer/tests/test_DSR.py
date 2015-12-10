import pydisdrometer

def test_tb():
    assert pydisdrometer.utility.DSR.tb(2) > 0
