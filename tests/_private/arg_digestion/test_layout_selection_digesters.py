import numpy as np
import pytest

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.arg_digestion.argument.acceptors import digest_acceptors
from molsysmt._private.arg_digestion.argument.donors import digest_donors
from molsysmt._private.arg_digestion.argument.attribute import digest_attribute
from molsysmt._private.arg_digestion.argument.blocks import digest_blocks
from molsysmt._private.arg_digestion.argument.chunk import digest_chunk
from molsysmt._private.arg_digestion.argument.start import digest_start
from molsysmt._private.arg_digestion.argument.stop import digest_stop
from molsysmt._private.arg_digestion.argument.top import digest_top
from molsysmt._private.arg_digestion.argument.bottom import digest_bottom


def test_acceptors_and_donors_accept_selection_like_inputs():
    assert digest_acceptors('name == "O"') == 'name == "O"'
    assert digest_acceptors([0, 2]) == [0, 2]
    np.testing.assert_array_equal(digest_acceptors([0, 2], syntax='NGLView'), np.array([0, 2], dtype='int64'))
    assert digest_donors('name == "N"') == 'name == "N"'
    assert digest_donors(range(2)) == [0, 1]
    with pytest.raises(ArgumentError):
        digest_acceptors(object())


def test_blocks_and_window_digesters_accept_expected_inputs():
    blocks = digest_blocks([[0, 1], np.array([2, 3])])
    assert len(blocks) == 2
    assert digest_chunk(4) == 4
    assert digest_start(0) == 0
    assert digest_stop(None) is None
    assert digest_stop(10) == 10
    with pytest.raises(ArgumentError):
        digest_blocks([0, 1, 2])


def test_top_and_bottom_accept_coordinates_and_selection_for_nglview_helpers():
    caller = 'molsysmt.third_party.nglview.add_cylinders.add_cylinders'
    xyz = puw.quantity(np.array([0.0, 0.0, 1.0]), 'nm')
    top = digest_top(xyz, caller=caller)
    bottom = digest_bottom('index == 0', caller=caller)
    assert puw.get_value(top).shape == (1, 1, 3)
    assert bottom == 'index == 0'
    assert digest_bottom(None, caller=caller) is None
    with pytest.raises(ArgumentError):
        digest_top(True, caller=caller)
