"""
Contract and parity tests for biopython.PDBStructure form.

biopython.PDBStructure is a Bio.PDB.Structure.Structure object.  The
creation path is molsysmt.MolSys → biopython.PDBStructure.

Oracle: builder_pdb_molsys (4 atoms: N/CA/C/O, 2 groups ALA+HOH, 1 chain A,
2 bonds).  Using the deterministic Builder oracle avoids dependency on PDB
file parsers.

Contract: a MolSys can be converted to biopython.PDBStructure and back.
Parity: the roundtrip preserves atom count, group count, chain count, atom
names, and group names.
"""

import pytest
import molsysmt as msm


@pytest.fixture(scope='module')
def source_topology(_base_builder_pdb_molsys):
    return _base_builder_pdb_molsys.topology


@pytest.fixture(scope='module')
def bio_structure(_base_builder_pdb_molsys):
    return msm.convert(_base_builder_pdb_molsys, to_form='biopython.PDBStructure')


@pytest.fixture(scope='module')
def roundtrip_topology(bio_structure):
    return msm.convert(bio_structure, to_form='molsysmt.Topology')


# ---------------------------------------------------------------------------
# Contract: MolSys → biopython.PDBStructure is created
# ---------------------------------------------------------------------------

def test_bio_structure_is_created(bio_structure):
    from Bio.PDB.Structure import Structure
    assert isinstance(bio_structure, Structure)


def test_bio_structure_atom_count(bio_structure):
    assert len(list(bio_structure.get_atoms())) == 4


def test_bio_structure_chain_count(bio_structure):
    assert len(list(bio_structure.get_chains())) == 1


# ---------------------------------------------------------------------------
# Parity: biopython.PDBStructure → molsysmt.Topology preserves topology
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
