import numpy as np
import pytest

from molsysmt._private.argdigest.argument.acceptors import digest_acceptors
from molsysmt._private.argdigest.argument.acceptors_2 import digest_acceptors_2
from molsysmt._private.argdigest.argument.donors import digest_donors
from molsysmt._private.argdigest.argument.anion import digest_anion
from molsysmt._private.argdigest.argument.cation import digest_cation
from molsysmt._private.argdigest.argument.hydrogens import digest_hydrogens
from molsysmt._private.argdigest.argument.disulfide_bonds import digest_disulfide_bonds
from molsysmt._private.argdigest.argument.disulfide_group_names import digest_disulfide_group_names
from molsysmt._private.smonitor import ArgumentError


def test_hbond_acceptor_and_donor_digesters():
    assert digest_acceptors('atom_type=="O"') == 'atom_type=="O"'
    assert digest_acceptors([1, 2, 3]) == [1, 2, 3]
    assert digest_acceptors(range(3)) == [0, 1, 2]
    assert np.array_equal(digest_acceptors([1, 2], syntax='OpenMM'), np.array([1, 2], dtype='int64'))
    assert digest_acceptors(None) is None
    assert digest_acceptors_2([4, 5]) == [4, 5]

    assert digest_donors('atom_type=="N"') == 'atom_type=="N"'
    assert digest_donors((6, 7)) == [6, 7]
    assert np.array_equal(digest_donors([6, 7], syntax='OpenMM'), np.array([6, 7], dtype='int64'))
    assert digest_donors(None) is None

    with pytest.raises(ArgumentError):
        digest_acceptors(object())
    with pytest.raises(ArgumentError):
        digest_donors(object())


def test_hbond_auxiliary_digesters():
    assert digest_anion('Cl-') == 'Cl-'
    assert digest_cation('Na+') == 'Na+'
    assert digest_hydrogens(True, caller='molsysmt.basic.contains.contains') is True
    assert digest_hydrogens(None, caller='molsysmt.basic.contains.contains') is None
    assert digest_disulfide_bonds(True, caller='molsysmt.build.get_missing_bonds') is True
    assert digest_disulfide_group_names(['CYS', 'CYX']) == ['CYS', 'CYX']

    with pytest.raises(ArgumentError):
        digest_anion('Na+')
    with pytest.raises(ArgumentError):
        digest_cation('Cl-')
    with pytest.raises(ArgumentError):
        digest_hydrogens('yes', caller='molsysmt.basic.contains.contains')
    with pytest.raises(ArgumentError):
        digest_disulfide_bonds('yes', caller='molsysmt.build.get_missing_bonds')
    with pytest.raises(ArgumentError):
        digest_disulfide_group_names(['CYS', 1])
