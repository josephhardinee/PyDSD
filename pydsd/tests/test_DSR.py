from ..DSR import tb, pb, bc, brandes
import numpy as np


def test_tb():
    assert tb(2) > 0


def test_brandes_is_positive_up_to_8mm():
    """ Test that the brandes DSR only returns positive values through all realistic drop sizes."""
    assert np.all(brandes(np.arange(0, 8, .1)) > 0)


def test_tb_is_positive_up_to_8mm():
    """ Test that the tb DSR only returns positive values through all realistic drop sizes."""
    assert np.all(tb(np.arange(0, 8, .1)) > 0)


def test_bc_is_positive_up_to_8mm():
    """ Test that the bc DSR only returns positive values through all realistic drop sizes."""
    assert np.all(bc(np.arange(0, 8, .1)) > 0)


def test_pb_is_positive_up_to_8mm():
    """ Test that the pb DSR only returns positive values through all realistic drop sizes."""
    assert np.all(pb(np.arange(0, 8, .1)) > 0)


def test_brandes_takes_singleton():
    """ Test  that brandes DSR can handle a single value"""
    assert brandes(1) > 0


def test_pb_takes_singleton():
    """ Test  that pb DSR can handle a single value"""
    assert pb(1) > 0


def test_bc_takes_singleton():
    """ Test  that bc DSR can handle a single value"""
    assert bc(1) > 0


def test_tb_takes_singleton():
    """ Test  that tb DSR can handle a single value"""
    assert tb(1) > 0
