"""
Tests for msm.build.get_missing_residues.

engine='MolSysMT' (default): uses SequenceMatcher to align the structural
sequence against a reference extracted from SEQRES (PDB) or _entity_poly_seq
(BCIF).  Returns {} with a UserWarning when no reference is available.

engine='PDBFixer': wraps pdbfixer.findMissingResidues.

Systems used
------------
- T4 lysozyme L99A (181l.h5msm): complete h5msm — no SEQRES → {} + warning
- 181L (PDB/BCIF): 162 structural residues, 164 in SEQRES → {(0,162): ['ASN','LEU']}
- chicken villin HP35 (h5msm): complete structure → {}
"""

import warnings
import pytest
import molsysmt as msm
from molsysmt import systems


@pytest.fixture(scope='module')
def t4_lysozyme_h5msm():
    return systems['T4 lysozyme L99A']['181l.h5msm']


@pytest.fixture(scope='module')
def villin():
    return systems['chicken villin HP35']['chicken_villin_HP35.h5msm']


@pytest.fixture(scope='module')
def t4_pdb(tmp_path_factory):
    """181L downloaded as a local PDB file (has SEQRES records)."""
    path = tmp_path_factory.mktemp('pdb') / '181L.pdb'
    msm.convert('181L', to_form=str(path))
    return str(path)


@pytest.fixture(scope='module')
def t4_bcif(tmp_path_factory):
    """181L downloaded as a local BCIF file (has _entity_poly_seq)."""
    path = tmp_path_factory.mktemp('bcif') / '181L.bcif'
    msm.convert('181L', to_form=str(path))
    return str(path)


# ---------------------------------------------------------------------------
# Return type and structure
# ---------------------------------------------------------------------------

def test_get_missing_residues_returns_dict(t4_pdb):
    result = msm.build.get_missing_residues(t4_pdb, engine='MolSysMT')
    assert isinstance(result, dict)


def test_get_missing_residues_keys_are_tuples(t4_pdb):
    """Dict keys are (chain_index, insertion_position) int tuples."""
    result = msm.build.get_missing_residues(t4_pdb, engine='MolSysMT')
    for k in result:
        assert isinstance(k, tuple)
        assert len(k) == 2
        assert isinstance(k[0], int)
        assert isinstance(k[1], int)


def test_get_missing_residues_values_are_lists_of_strings(t4_pdb):
    """Dict values are lists of residue name strings."""
    result = msm.build.get_missing_residues(t4_pdb, engine='MolSysMT')
    for v in result.values():
        assert isinstance(v, list)
        for name in v:
            assert isinstance(name, str)


# ---------------------------------------------------------------------------
# Known results — native engine
# ---------------------------------------------------------------------------

def test_get_missing_residues_pdb_detects_missing(t4_pdb):
    """181L PDB has 2 residues missing at C-terminus (ASN, LEU)."""
    result = msm.build.get_missing_residues(t4_pdb, engine='MolSysMT')
    assert (0, 162) in result
    assert result[(0, 162)] == ['ASN', 'LEU']


def test_get_missing_residues_bcif_detects_missing(t4_bcif):
    """181L BCIF has the same 2 residues missing."""
    result = msm.build.get_missing_residues(t4_bcif, engine='MolSysMT')
    assert (0, 162) in result
    assert result[(0, 162)] == ['ASN', 'LEU']


def test_get_missing_residues_villin_complete(villin):
    """Villin h5msm is complete: MolSysMT returns {} with warning (no SEQRES)."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        result = msm.build.get_missing_residues(villin, engine='MolSysMT')
    assert result == {}
    assert any(issubclass(x.category, UserWarning) for x in w)


def test_get_missing_residues_no_seqres_warns(t4_lysozyme_h5msm):
    """h5msm has no SEQRES → UserWarning emitted, {} returned."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        result = msm.build.get_missing_residues(t4_lysozyme_h5msm, engine='MolSysMT')
    assert result == {}
    assert any(issubclass(x.category, UserWarning) for x in w)


def test_get_missing_residues_explicit_sequence(t4_lysozyme_h5msm):
    """Explicit sequence argument bypasses the SEQRES auto-detection."""
    # Build reference: 164 residues for chain A (add ASN, LEU at the end)
    mol = msm.convert(t4_lysozyme_h5msm, to_form='molsysmt.MolSys')
    struct_seq = msm.get(mol, element='group', selection='chain_index==0', group_name=True)
    chain_id = msm.get(mol, element='chain', chain_id=True)[0]
    ref = {chain_id: list(struct_seq) + ['ASN', 'LEU']}
    result = msm.build.get_missing_residues(t4_lysozyme_h5msm, sequence=ref, engine='MolSysMT')
    assert (0, len(struct_seq)) in result
    assert result[(0, len(struct_seq))] == ['ASN', 'LEU']


# ---------------------------------------------------------------------------
# Selection argument
# ---------------------------------------------------------------------------

def test_get_missing_residues_with_selection(t4_pdb):
    result = msm.build.get_missing_residues(
        t4_pdb, selection='molecule_type=="protein"', engine='MolSysMT'
    )
    assert isinstance(result, dict)


# ---------------------------------------------------------------------------
# PDBFixer engine (parity)
# ---------------------------------------------------------------------------

def test_get_missing_residues_pdbfixer_parity(t4_pdb):
    """MolSysMT and PDBFixer return the same result for 181L."""
    result_msm = msm.build.get_missing_residues(t4_pdb, engine='MolSysMT')
    result_pdb = msm.build.get_missing_residues(t4_pdb, engine='PDBFixer')
    assert result_msm == result_pdb
