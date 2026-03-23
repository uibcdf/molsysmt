"""
Contract and parity tests for parmed.Structure form.

parmed.Structure carries topology without coordinates.  The creation path
is molsysmt.Topology → parmed.Structure (via openmm.Topology bridge).

Oracle: builder_pdb_molsys (4 atoms: N/CA/C/O, 2 groups ALA+HOH, 1 chain A,
2 bonds).  Using the deterministic Builder oracle avoids dependency on PDB
file parsers.

Contract: a Topology can be converted to parmed.Structure and back.
Parity: the roundtrip preserves atom count, group count, chain count, atom
names, and group names.
"""

import pytest
import molsysmt as msm


@pytest.fixture(scope='module')
def source_topology(_base_builder_pdb_molsys):
    return _base_builder_pdb_molsys.topology


@pytest.fixture(scope='module')
def parmed_structure(source_topology):
    return msm.convert(source_topology, to_form='parmed.Structure')


@pytest.fixture(scope='module')
def roundtrip_topology(parmed_structure):
    return msm.convert(parmed_structure, to_form='molsysmt.Topology')


# ---------------------------------------------------------------------------
# Contract: Topology → parmed.Structure is created
# ---------------------------------------------------------------------------

def test_parmed_structure_is_created(parmed_structure):
    import parmed
    assert isinstance(parmed_structure, parmed.Structure)


def test_parmed_structure_atom_count(parmed_structure):
    assert len(parmed_structure.atoms) == 4


def test_parmed_structure_residue_count(parmed_structure):
    assert len(parmed_structure.residues) == 2


# ---------------------------------------------------------------------------
# Parity: parmed.Structure → molsysmt.Topology preserves topology
# ---------------------------------------------------------------------------

def test_parity_atom_count(roundtrip_topology, source_topology):
    assert roundtrip_topology.n_atoms == source_topology.n_atoms


def test_parity_group_count(roundtrip_topology, source_topology):
    assert roundtrip_topology.n_groups == source_topology.n_groups


def test_parity_chain_count(roundtrip_topology, source_topology):
    assert roundtrip_topology.n_chains == source_topology.n_chains


def test_parity_atom_names(roundtrip_topology, source_topology):
    assert roundtrip_topology.atoms['atom_name'].tolist() == source_topology.atoms['atom_name'].tolist()


def test_parity_group_names(roundtrip_topology, source_topology):
    assert roundtrip_topology.groups['group_name'].tolist() == source_topology.groups['group_name'].tolist()
