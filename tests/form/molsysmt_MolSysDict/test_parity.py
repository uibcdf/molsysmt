"""
Parity tests for molsysmt.MolSysDict form.

Oracle: builder_pdb_molsys (4 atoms, 2 groups, 1 chain).
Parity means that get() on a MolSysDict returns identical values to
get() on the original MolSys for all documented topological attributes.
"""

import pytest
import molsysmt as msm


@pytest.fixture()
def source_molsys(builder_pdb_molsys):
    return builder_pdb_molsys


@pytest.fixture()
def molsys_dict(builder_pdb_molsys):
    return msm.convert(builder_pdb_molsys, to_form='molsysmt.MolSysDict')


# ---------------------------------------------------------------------------
# Parity: MolSysDict get() == MolSys get() on the same system
# ---------------------------------------------------------------------------

def test_parity_n_atoms(molsys_dict, source_molsys):
    assert (msm.get(molsys_dict, element='system', n_atoms=True) ==
            msm.get(source_molsys, element='system', n_atoms=True))


def test_parity_n_groups(molsys_dict, source_molsys):
    assert (msm.get(molsys_dict, element='system', n_groups=True) ==
            msm.get(source_molsys, element='system', n_groups=True))


def test_parity_n_chains(molsys_dict, source_molsys):
    assert (msm.get(molsys_dict, element='system', n_chains=True) ==
            msm.get(source_molsys, element='system', n_chains=True))


def test_parity_n_bonds(molsys_dict, source_molsys):
    assert (msm.get(molsys_dict, element='system', n_bonds=True) ==
            msm.get(source_molsys, element='system', n_bonds=True))


def test_parity_atom_names(molsys_dict, source_molsys):
    assert (msm.get(molsys_dict, element='atom', atom_name=True) ==
            msm.get(source_molsys, element='atom', atom_name=True))


def test_parity_group_names(molsys_dict, source_molsys):
    assert (msm.get(molsys_dict, element='group', group_name=True) ==
            msm.get(source_molsys, element='group', group_name=True))


def test_parity_chain_ids(molsys_dict, source_molsys):
    assert (msm.get(molsys_dict, element='chain', chain_id=True) ==
            msm.get(source_molsys, element='chain', chain_id=True))
