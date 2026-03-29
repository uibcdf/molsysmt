"""
Extended unit and regression tests for molsysmt.build.build_peptide (MolSysMT engine).

These tests target branches and code paths not already covered by
test_build_peptide_molsysmt_MolSys.py, including:
  - Single-residue peptides
  - All twenty standard amino acids individually
  - Capped sequences with ACE/NME
  - Long sequences (10+ residues)
  - Sequences containing charged/polar residues
  - Sequences containing special residues (HIS variants, PRO-rich)
  - Topology invariants (chain name, molecule type, entity type)
  - Output-form conversion to molsysmt.Topology and molsysmt.Structures
  - Error paths: unsupported engine, invalid/unknown residue code
  - Coordinate and bond geometry sanity for each residue category
"""

import pytest
import numpy as np
import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_coordinates_nm(molsys):
    return msm.pyunitwizard.get_value(molsys.structures.coordinates[0], to_unit='nm')


def _bond_lengths_nm(molsys):
    coords = _get_coordinates_nm(molsys)
    bonds = molsys.topology.bonds[['atom1_index', 'atom2_index']].to_numpy(dtype=int)
    if bonds.shape[0] == 0:
        return np.array([])
    return np.linalg.norm(coords[bonds[:, 0]] - coords[bonds[:, 1]], axis=1)


def _min_nonbonded_heavy_distance_nm(molsys):
    coords = _get_coordinates_nm(molsys)
    bonds = molsys.topology.bonds[['atom1_index', 'atom2_index']].to_numpy(dtype=int)
    atom_types = molsys.topology.atoms['atom_type'].to_numpy()
    heavy = np.where(atom_types != 'H')[0]
    bonded = {tuple(sorted((int(i), int(j)))) for i, j in bonds}
    min_d = np.inf
    for ii, a in enumerate(heavy):
        for b in heavy[ii + 1:]:
            if tuple(sorted((int(a), int(b)))) in bonded:
                continue
            d = np.linalg.norm(coords[a] - coords[b])
            if d < min_d:
                min_d = d
    return min_d


def _basic_geometry_ok(molsys, min_bond=0.09, max_bond=0.185, min_nonbonded=0.10):
    """Return True when bond lengths and non-bonded contacts are within expected ranges."""
    bl = _bond_lengths_nm(molsys)
    if bl.size > 0 and (np.min(bl) < min_bond or np.max(bl) > max_bond):
        return False
    mnb = _min_nonbonded_heavy_distance_nm(molsys)
    return mnb >= min_nonbonded


# ---------------------------------------------------------------------------
# Single-residue peptides
# ---------------------------------------------------------------------------

@pytest.mark.parametrize('aa', ['A', 'G', 'V', 'L', 'I', 'P', 'F', 'W', 'M', 'S'])
def test_single_residue_standard_1(aa):
    """Single amino acid (one-letter code) yields a non-empty MolSys."""
    molsys = msm.build.build_peptide(aa, to_form='molsysmt.MolSys', engine='MolSysMT')
    assert msm.get(molsys, n_atoms=True) > 0
    assert msm.get(molsys, n_groups=True) == 1


@pytest.mark.parametrize('aa', ['T', 'C', 'Y', 'H', 'D', 'E', 'N', 'Q', 'K', 'R'])
def test_single_residue_standard_2(aa):
    """Single amino acid (polar / charged) yields a non-empty MolSys."""
    molsys = msm.build.build_peptide(aa, to_form='molsysmt.MolSys', engine='MolSysMT')
    assert msm.get(molsys, n_atoms=True) > 0
    assert msm.get(molsys, n_groups=True) == 1


def test_single_residue_sequence_roundtrip():
    """Single alanine: sequence round-trips through MolSysMT engine."""
    molsys = msm.build.build_peptide('A', to_form='molsysmt.MolSys', engine='MolSysMT')
    seq = msm.convert(molsys, to_form='string:amino_acids_3')
    assert seq.upper() == 'ALA'


# ---------------------------------------------------------------------------
# All 20 standard amino acids in a dipeptide context
# ---------------------------------------------------------------------------

_ALL_AA_1 = list("ACDEFGHIKLMNPQRSTVWY")


@pytest.mark.parametrize('aa', _ALL_AA_1)
def test_dipeptide_all_residues_geometry(aa):
    """Dipeptide GA<X> has valid bond lengths and no severe clashes."""
    seq = 'G' + aa
    molsys = msm.build.build_peptide(seq, to_form='molsysmt.MolSys', engine='MolSysMT')
    assert msm.get(molsys, n_groups=True) == 2
    assert _basic_geometry_ok(molsys, min_bond=0.09, max_bond=0.185, min_nonbonded=0.10)


@pytest.mark.parametrize('aa', _ALL_AA_1)
def test_dipeptide_all_residues_sequence_preserved(aa):
    """Dipeptide G<X>: sequence is preserved after build."""
    seq = 'G' + aa
    molsys = msm.build.build_peptide(seq, to_form='molsysmt.MolSys', engine='MolSysMT')
    recovered = msm.convert(molsys, to_form='string:amino_acids_1')
    assert recovered.upper() == seq.upper()


# ---------------------------------------------------------------------------
# Capped sequences (ACE/NME)
# ---------------------------------------------------------------------------

def test_capped_single_aa_groups():
    """ACE-ALA-NME yields 3 groups."""
    molsys = msm.build.build_peptide('ACEALANME', to_form='molsysmt.MolSys', engine='MolSysMT')
    assert msm.get(molsys, n_groups=True) == 3


def test_capped_single_aa_group_names():
    """ACE-ALA-NME group names are ACE, ALA, NME."""
    molsys = msm.build.build_peptide('ACEALANME', to_form='molsysmt.MolSys', engine='MolSysMT')
    group_names = list(molsys.topology.groups['group_name'])
    assert group_names == ['ACE', 'ALA', 'NME']


def test_capped_gly_geometry():
    """ACE-GLY-NME geometry is within acceptable ranges."""
    molsys = msm.build.build_peptide('ACEGLYNME', to_form='molsysmt.MolSys', engine='MolSysMT')
    assert _basic_geometry_ok(molsys, min_bond=0.09, max_bond=0.185, min_nonbonded=0.10)


@pytest.mark.parametrize('seq', ['ACEVALNME', 'ACETRPNME', 'ACELEUILENME'])
def test_capped_various_residues_geometry(seq):
    """Capped sequences with bulky residues have acceptable geometry."""
    molsys = msm.build.build_peptide(seq, to_form='molsysmt.MolSys', engine='MolSysMT')
    assert _basic_geometry_ok(molsys, min_bond=0.09, max_bond=0.185, min_nonbonded=0.09)


def test_ace_only_at_n_terminus():
    """ACE cap is recognised only when placed at N-terminus."""
    molsys = msm.build.build_peptide('ACEALA', to_form='molsysmt.MolSys', engine='MolSysMT')
    group_names = list(molsys.topology.groups['group_name'])
    assert group_names[0] == 'ACE'


def test_nme_only_at_c_terminus():
    """NME cap is recognised when placed at C-terminus."""
    molsys = msm.build.build_peptide('ALANME', to_form='molsysmt.MolSys', engine='MolSysMT')
    group_names = list(molsys.topology.groups['group_name'])
    assert group_names[-1] == 'NME'


# ---------------------------------------------------------------------------
# Long sequences
# ---------------------------------------------------------------------------

def test_long_sequence_10_residues():
    """10-residue sequence builds without error."""
    seq = 'ACDEFGHIKL'
    molsys = msm.build.build_peptide(seq, to_form='molsysmt.MolSys', engine='MolSysMT')
    assert msm.get(molsys, n_groups=True) == 10


def test_long_sequence_15_residues_geometry():
    """15-residue sequence has acceptable bond geometry."""
    seq = 'MNPQRSTVWYACDEF'
    molsys = msm.build.build_peptide(seq, to_form='molsysmt.MolSys', engine='MolSysMT')
    bl = _bond_lengths_nm(molsys)
    assert bl.size > 0
    assert np.max(bl) <= 0.185


def test_long_capped_sequence_groups():
    """Capped sequence yields the expected number of groups."""
    seq = 'ACEALAGLYVALILEPROARGNME'
    molsys = msm.build.build_peptide(seq, to_form='molsysmt.MolSys', engine='MolSysMT')
    assert msm.get(molsys, n_groups=True) == 8


# ---------------------------------------------------------------------------
# Charged / polar residue sequences
# ---------------------------------------------------------------------------

def test_charged_sequence_asp_glu_lys_arg():
    """Sequence with charged residues (D, E, K, R) builds successfully."""
    seq = 'DEKR'
    molsys = msm.build.build_peptide(seq, to_form='molsysmt.MolSys', engine='MolSysMT')
    assert msm.get(molsys, n_groups=True) == 4
    assert _basic_geometry_ok(molsys, min_bond=0.09, max_bond=0.185, min_nonbonded=0.09)


def test_polar_sequence_ser_thr_asn_gln():
    """Sequence with polar residues (S, T, N, Q) builds successfully."""
    seq = 'STNQ'
    molsys = msm.build.build_peptide(seq, to_form='molsysmt.MolSys', engine='MolSysMT')
    assert msm.get(molsys, n_groups=True) == 4
    assert _basic_geometry_ok(molsys, min_bond=0.09, max_bond=0.185, min_nonbonded=0.09)


def test_aromatic_sequence_phe_tyr_trp():
    """Sequence with aromatic residues (F, Y, W) builds successfully."""
    seq = 'FYW'
    molsys = msm.build.build_peptide(seq, to_form='molsysmt.MolSys', engine='MolSysMT')
    assert msm.get(molsys, n_groups=True) == 3
    assert _basic_geometry_ok(molsys, min_bond=0.09, max_bond=0.185, min_nonbonded=0.09)


def test_cysteine_sequence():
    """Sequence with cysteine builds correctly."""
    seq = 'CAC'
    molsys = msm.build.build_peptide(seq, to_form='molsysmt.MolSys', engine='MolSysMT')
    assert msm.get(molsys, n_groups=True) == 3


# ---------------------------------------------------------------------------
# Proline-rich / ring-constrained sequences
# ---------------------------------------------------------------------------

def test_pro_at_n_terminus():
    """Proline at N-terminus builds without error."""
    molsys = msm.build.build_peptide('PA', to_form='molsysmt.MolSys', engine='MolSysMT')
    assert msm.get(molsys, n_groups=True) == 2


def test_consecutive_prolines():
    """Multiple consecutive prolines yield acceptable geometry."""
    molsys = msm.build.build_peptide('PPP', to_form='molsysmt.MolSys', engine='MolSysMT')
    assert msm.get(molsys, n_groups=True) == 3
    bl = _bond_lengths_nm(molsys)
    assert np.max(bl) <= 0.185


def test_pro_in_capped_sequence():
    """ACE-PRO-NME (degenerate ring cap) builds without error."""
    molsys = msm.build.build_peptide('ACEPRONME', to_form='molsysmt.MolSys', engine='MolSysMT')
    assert msm.get(molsys, n_groups=True) >= 2


# ---------------------------------------------------------------------------
# Topology invariants
# ---------------------------------------------------------------------------

def test_chain_name_is_A():
    """MolSysMT engine sets chain name to 'A'."""
    molsys = msm.build.build_peptide('ALA', to_form='molsysmt.MolSys', engine='MolSysMT')
    chain_names = list(molsys.topology.chains['chain_name'])
    assert chain_names == ['A']


def test_molecule_type_is_peptide():
    """Molecule type is recorded as 'peptide'."""
    molsys = msm.build.build_peptide('GG', to_form='molsysmt.MolSys', engine='MolSysMT')
    mol_types = list(molsys.topology.molecules['molecule_type'])
    assert mol_types == ['peptide']


def test_entity_type_is_protein():
    """Entity type is recorded as 'protein'."""
    molsys = msm.build.build_peptide('GG', to_form='molsysmt.MolSys', engine='MolSysMT')
    entity_types = list(molsys.topology.entities['entity_type'])
    assert entity_types == ['protein']


def test_atom_ff_type_column_present():
    """MolecularMechanics contains atom_ff_type after build_peptide."""
    molsys = msm.build.build_peptide('AV', to_form='molsysmt.MolSys', engine='MolSysMT')
    assert molsys.molecular_mechanics.atom_ff_type is not None


def test_bonds_atom_indices_are_sorted():
    """All bond pairs satisfy atom1_index < atom2_index."""
    molsys = msm.build.build_peptide('AGS', to_form='molsysmt.MolSys', engine='MolSysMT')
    bonds = molsys.topology.bonds[['atom1_index', 'atom2_index']].to_numpy(dtype=int)
    assert np.all(bonds[:, 0] < bonds[:, 1])


def test_n_components_is_one():
    """A peptide chain is one covalently connected component, not one per residue."""
    molsys = msm.build.build_peptide('AGVIL', to_form='molsysmt.MolSys', engine='MolSysMT')
    n_components = msm.get(molsys, n_components=True)
    assert n_components == 1


# ---------------------------------------------------------------------------
# Output-form conversions
# ---------------------------------------------------------------------------

def test_output_form_topology():
    """build_peptide can produce a molsysmt.Topology output."""
    topology = msm.build.build_peptide('AG', to_form='molsysmt.Topology', engine='MolSysMT')
    from molsysmt.native import Topology
    assert isinstance(topology, Topology)
    assert topology.atoms.shape[0] > 0


def test_output_form_structures():
    """build_peptide can produce a molsysmt.Structures output."""
    structures = msm.build.build_peptide('AG', to_form='molsysmt.Structures', engine='MolSysMT')
    from molsysmt.native import Structures
    assert isinstance(structures, Structures)


# ---------------------------------------------------------------------------
# Coordinates consistency
# ---------------------------------------------------------------------------

def test_coordinates_shape():
    """Coordinates have shape (1, n_atoms, 3)."""
    molsys = msm.build.build_peptide('AGA', to_form='molsysmt.MolSys', engine='MolSysMT')
    n_atoms = msm.get(molsys, n_atoms=True)
    coords = molsys.structures.coordinates
    assert coords.shape == (1, n_atoms, 3)


def test_coordinates_finite():
    """All coordinate values are finite (no NaN or Inf)."""
    molsys = msm.build.build_peptide('ACDEFGHIKL', to_form='molsysmt.MolSys', engine='MolSysMT')
    coords = _get_coordinates_nm(molsys)
    assert np.all(np.isfinite(coords))


def test_coordinates_not_all_zero():
    """Coordinate array is not all zeros."""
    molsys = msm.build.build_peptide('AGV', to_form='molsysmt.MolSys', engine='MolSysMT')
    coords = _get_coordinates_nm(molsys)
    assert not np.all(coords == 0.0)


def test_deterministic_output():
    """Two calls with the same sequence produce identical coordinates and bonds."""
    seq = 'ACVLIMFYW'
    molsys_a = msm.build.build_peptide(seq, to_form='molsysmt.MolSys', engine='MolSysMT')
    molsys_b = msm.build.build_peptide(seq, to_form='molsysmt.MolSys', engine='MolSysMT')
    coords_a = _get_coordinates_nm(molsys_a)
    coords_b = _get_coordinates_nm(molsys_b)
    bonds_a = molsys_a.topology.bonds[['atom1_index', 'atom2_index']].to_numpy(dtype=int)
    bonds_b = molsys_b.topology.bonds[['atom1_index', 'atom2_index']].to_numpy(dtype=int)
    assert np.array_equal(bonds_a, bonds_b)
    assert np.allclose(coords_a, coords_b, atol=1.0e-12)


# ---------------------------------------------------------------------------
# Error paths
# ---------------------------------------------------------------------------

def test_unsupported_engine_raises():
    """Passing an unknown engine raises ArgumentError."""
    with pytest.raises(ArgumentError):
        msm.build.build_peptide('AG', to_form='molsysmt.MolSys', engine='UnknownEngine')


def test_invalid_residue_code_raises():
    """Passing an unrecognised residue code raises an error."""
    with pytest.raises((ValueError, Exception)):
        msm.build.build_peptide('XYZ', to_form='molsysmt.MolSys', engine='MolSysMT')
