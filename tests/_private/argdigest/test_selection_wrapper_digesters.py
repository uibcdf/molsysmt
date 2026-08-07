import pytest

from molsysmt._private.argdigest.argument.selection import digest_selection
from molsysmt._private.argdigest.argument.selection_2 import digest_selection_2
from molsysmt._private.argdigest.argument.syntax import digest_syntax
from molsysmt._private.smonitor import ArgumentError


def test_selection_wrapper_digesters():
    assert digest_selection('atom_index<4') == 'atom_index<4'
    assert digest_selection([0, 1, 2]) == [0, 1, 2]
    assert digest_selection_2('atom_index==0') == 'atom_index==0'
    assert digest_syntax('MolSysMT') == 'MolSysMT'

    with pytest.raises(ArgumentError):
        digest_selection_2(object())
    with pytest.raises(ArgumentError):
        digest_syntax('bad-syntax')
