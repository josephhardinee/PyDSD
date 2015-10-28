import pydisdrometer

def test_tb():
    assert pydisdrometer.DSR.tb(2) > 0
