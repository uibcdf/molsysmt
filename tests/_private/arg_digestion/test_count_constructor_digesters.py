import pytest

from molsysmt._private.argdigest.argument.n_atoms import digest_n_atoms
from molsysmt._private.argdigest.argument.n_groups import digest_n_groups
from molsysmt._private.argdigest.argument.n_neighbors import digest_n_neighbors
from molsysmt._private.smonitor import ArgumentError


def test_count_constructor_digesters():
    assert digest_n_atoms(True, caller='molsysmt.basic.get.get') is True
    assert digest_n_atoms(4, caller='molsysmt.native.topology.__init__') == 4
    assert digest_n_groups(True, caller='molsysmt.basic.get.get') is True
    assert digest_n_groups(2, caller='molsysmt.native.topology.__init__') == 2
    assert digest_n_neighbors(None) is None
    assert digest_n_neighbors(6) == 6

    with pytest.raises(ArgumentError):
        digest_n_atoms(4)
    with pytest.raises(ArgumentError):
        digest_n_groups(2)
