import numpy as np
import pytest

from molsysmt import pyunitwizard as puw
from molsysmt._private.arg_digestion.argument.C_terminal import digest_C_terminal
from molsysmt._private.arg_digestion.argument.N_terminal import digest_N_terminal
from molsysmt._private.arg_digestion.argument.alignment_index import digest_alignment_index
from molsysmt._private.arg_digestion.argument.angles import digest_angles
from molsysmt._private.arg_digestion.argument.copy_if_None import digest_copy_if_None
from molsysmt._private.arg_digestion.argument.copy_if_all import digest_copy_if_all
from molsysmt._private.arg_digestion.argument.occupancy import digest_occupancy
from molsysmt._private.arg_digestion.argument.weights import digest_weights
from molsysmt._private.arg_digestion.argument.weights_2 import digest_weights_2
from molsysmt._private.smonitor import ArgumentError


def test_terminal_and_optional_digesters():
    assert digest_C_terminal(None) is None
    assert digest_C_terminal('NME') == 'NME'
    assert digest_N_terminal(None) is None
    assert digest_N_terminal('ACE') == 'ACE'
    assert digest_alignment_index(3) == 3
    angles = digest_angles(puw.quantity([0.0, 1.0], 'radians'))
    assert angles.shape == (1, 2)
    assert digest_copy_if_None(True) is True
    assert digest_copy_if_all(False) is False
    assert digest_occupancy([1.0, 0.5]).shape == (1, 2)
    assert digest_occupancy(True, caller='molsysmt.basic.get.get') is True
    assert digest_weights('masses') == 'masses'
    assert digest_weights([1.0, 2.0]) == [1.0, 2.0]
    assert digest_weights_2([1.0, 2.0]) == [1.0, 2.0]

    with pytest.raises(ArgumentError):
        digest_C_terminal(1)
    with pytest.raises(ArgumentError):
        digest_alignment_index('3')
    with pytest.raises(ArgumentError):
        digest_occupancy('bad')
