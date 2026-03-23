"""
Parity tests for file:molsys_yaml form.

Oracle: builder_pdb_molsys (4 atoms, 2 groups, 1 chain, 2 bonds).
Parity means that get() on a file:molsys_yaml returns identical values
to get() on the source MolSys for all documented topological attributes.
"""

import pytest
import molsysmt as msm


@pytest.fixture()
def yaml_file(builder_pdb_molsys, tmp_path):
    path = str(tmp_path / 'parity.yaml')
    msm.convert(builder_pdb_molsys, to_form='file:molsys_yaml', output_filename=path)
    return path


@pytest.fixture()
def source_molsys(builder_pdb_molsys):
    return builder_pdb_molsys


# ---------------------------------------------------------------------------
# Parity: file:molsys_yaml get() == MolSys get() on the same system
# ---------------------------------------------------------------------------

def test_parity_n_atoms(yaml_file, source_molsys):
    assert (msm.get(yaml_file, element='system', n_atoms=True) ==
            msm.get(source_molsys, element='system', n_atoms=True))


def test_parity_n_groups(yaml_file, source_molsys):
    assert (msm.get(yaml_file, element='system', n_groups=True) ==
            msm.get(source_molsys, element='system', n_groups=True))


def test_parity_n_chains(yaml_file, source_molsys):
    assert (msm.get(yaml_file, element='system', n_chains=True) ==
            msm.get(source_molsys, element='system', n_chains=True))


def test_parity_atom_names(yaml_file, source_molsys):
    assert (msm.get(yaml_file, element='atom', atom_name=True) ==
            msm.get(source_molsys, element='atom', atom_name=True))


def test_parity_group_names(yaml_file, source_molsys):
    assert (msm.get(yaml_file, element='group', group_name=True) ==
            msm.get(source_molsys, element='group', group_name=True))


def test_parity_chain_ids(yaml_file, source_molsys):
    assert (msm.get(yaml_file, element='chain', chain_id=True) ==
            msm.get(source_molsys, element='chain', chain_id=True))
