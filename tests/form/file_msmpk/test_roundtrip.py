"""
Contract and parity tests for file:msmpk form.

Oracle: builder_pdb_molsys (4 atoms, 2 groups, 1 chain, 2 bonds).
Contract: a MolSys can be saved to file:msmpk and read back.
Parity: the roundtrip preserves atom count, group count, chain count,
bond count, atom names, and group names.
"""

import pytest
import molsysmt as msm


@pytest.fixture()
def msmpk_file(builder_pdb_molsys, tmp_path):
    path = str(tmp_path / 'builder.msmpk')
    msm.convert(builder_pdb_molsys, to_form='file:msmpk', output_filename=path)
    return path


@pytest.fixture()
def roundtrip_molsys(msmpk_file):
    return msm.convert(msmpk_file, to_form='molsysmt.MolSys')


@pytest.fixture()
def source_topology(builder_pdb_molsys):
    return builder_pdb_molsys.topology


# ---------------------------------------------------------------------------
# Contract: file:msmpk can be written and read back
# ---------------------------------------------------------------------------

def test_msmpk_file_is_created(msmpk_file):
    import os
    assert os.path.isfile(msmpk_file)


def test_msmpk_loads_as_molsys(roundtrip_molsys):
    assert roundtrip_molsys is not None


# ---------------------------------------------------------------------------
# Parity: MolSys → file:msmpk → MolSys preserves topology
# ---------------------------------------------------------------------------

def test_parity_atom_count(roundtrip_molsys, source_topology):
    assert roundtrip_molsys.topology.n_atoms == source_topology.n_atoms


def test_parity_group_count(roundtrip_molsys, source_topology):
    assert roundtrip_molsys.topology.n_groups == source_topology.n_groups


def test_parity_chain_count(roundtrip_molsys, source_topology):
    assert roundtrip_molsys.topology.n_chains == source_topology.n_chains


def test_parity_bond_count(roundtrip_molsys, source_topology):
    assert roundtrip_molsys.topology.n_bonds == source_topology.n_bonds


def test_parity_atom_names(roundtrip_molsys, source_topology):
    assert roundtrip_molsys.topology.atoms['atom_name'].tolist() == source_topology.atoms['atom_name'].tolist()


def test_parity_group_names(roundtrip_molsys, source_topology):
    assert roundtrip_molsys.topology.groups['group_name'].tolist() == source_topology.groups['group_name'].tolist()
