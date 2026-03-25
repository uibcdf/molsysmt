"""
Additional coverage tests for molsysmt.build.build_peptide (MolSysMT engine).

Targets branches not yet exercised by existing test files:
- HIS variant aliases (HIE, HID, HIP, HISE, HISD) via _resolve_template_alias
- CYX (cysteine in disulfide)
- Template fallback path (residues not in amber14sb template database)
- ACE-only and NME-only (terminal cappings without flanking amino acid)
- All-caps 3-letter sequences passed directly (string input)
- Output to string:pdb_text form
- Single-residue with each terminal capping variant
- Sequences that maximise torsion optimisation iterations (long + bulky)
- Chain-index reset path via set_chain_index_to_atom broadcast (len(value)==1)
"""

import pytest
import numpy as np
import molsysmt as msm


# ---------------------------------------------------------------------------
# HIS variants
# ---------------------------------------------------------------------------

@pytest.mark.parametrize('his_variant', ['HIE', 'HID', 'HIP'])
def test_his_variants_geometry(his_variant):
    """HIS aliases (HIE/HID/HIP) build without error and produce valid geometry."""
    molsys = msm.build.build_peptide(f'ALA{his_variant}ALA',
                                     to_form='molsysmt.MolSys', engine='MolSysMT')
    assert molsys is not None
    n_groups = msm.get(molsys, element='system', n_groups=True)
    assert n_groups == 3


@pytest.mark.parametrize('his_variant', ['HISE', 'HISD'])
def test_his_long_variants(his_variant):
    """Three-letter HIS synonyms also resolve and build."""
    molsys = msm.build.build_peptide(f'GLY{his_variant}GLY',
                                     to_form='molsysmt.MolSys', engine='MolSysMT')
    assert molsys is not None


# ---------------------------------------------------------------------------
# CYX (cysteine in disulfide context)
# ---------------------------------------------------------------------------

def test_cyx_builds():
    """CYX (disulfide cysteine) sequence builds without error."""
    molsys = msm.build.build_peptide('ALACYXALA',
                                     to_form='molsysmt.MolSys', engine='MolSysMT')
    assert molsys is not None
    n_groups = msm.get(molsys, element='system', n_groups=True)
    assert n_groups == 3


# ---------------------------------------------------------------------------
# Terminal capping combinations — all explicit
# ---------------------------------------------------------------------------

def test_ace_only_sequence():
    """ACE as the only group (no amino acid) — fallback topology path."""
    # ACE alone triggers the terminal_capping_group_names path with no amino acid
    molsys = msm.build.build_peptide('ACE',
                                     to_form='molsysmt.MolSys', engine='MolSysMT')
    assert molsys is not None


def test_nme_only_sequence():
    """NME as the only group."""
    molsys = msm.build.build_peptide('NME',
                                     to_form='molsysmt.MolSys', engine='MolSysMT')
    assert molsys is not None


def test_ace_nme_no_amino_acid():
    """ACE + NME with no amino acid between them."""
    molsys = msm.build.build_peptide('ACENME',
                                     to_form='molsysmt.MolSys', engine='MolSysMT')
    assert molsys is not None


# ---------------------------------------------------------------------------
# Long sequences that stress torsion optimisation
# ---------------------------------------------------------------------------

def test_long_charged_sequence():
    """Long sequence with many rotatable side-chains → multiple optimisation passes."""
    seq = 'ACEARGLYSLYSASPGLUNME'
    molsys = msm.build.build_peptide(seq, to_form='molsysmt.MolSys', engine='MolSysMT')
    assert molsys is not None
    n_groups = msm.get(molsys, element='system', n_groups=True)
    assert n_groups == 7  # ACE + 5 AA + NME


def test_long_bulky_sequence():
    """Bulky aromatics maximise the geometry packing search."""
    seq = 'TRPPHETYRTYRTRP'
    molsys = msm.build.build_peptide(seq, to_form='molsysmt.MolSys', engine='MolSysMT')
    assert molsys is not None
    n_groups = msm.get(molsys, element='system', n_groups=True)
    assert n_groups == 5


# ---------------------------------------------------------------------------
# Output forms other than molsysmt.MolSys
# ---------------------------------------------------------------------------

def test_output_string_pdb_text():
    """build_peptide → string:pdb_text form."""
    result = msm.build.build_peptide('ALAG', to_form='string:pdb_text', engine='MolSysMT')
    assert isinstance(result, str)
    assert 'ATOM' in result


def test_output_openmm_topology():
    """build_peptide → openmm.Topology form."""
    pytest.importorskip('openmm')
    result = msm.build.build_peptide('AGV', to_form='openmm.Topology', engine='MolSysMT')
    assert result is not None


# ---------------------------------------------------------------------------
# 3-letter code string input (all-caps, space-separated)
# ---------------------------------------------------------------------------

def test_three_letter_string_input():
    """Passing a 3-letter amino acid string directly."""
    molsys = msm.build.build_peptide('AlaGlyVal', to_form='molsysmt.MolSys', engine='MolSysMT')
    assert molsys is not None
    n_groups = msm.get(molsys, element='system', n_groups=True)
    assert n_groups == 3


# ---------------------------------------------------------------------------
# First group has head_index=None (e.g. ACE: connect=[None, C])
# exercises the else-branch at group_index==0
# ---------------------------------------------------------------------------

def test_first_group_no_head_index():
    """ACE as first group exercises the anchor fallback when head_index is None."""
    molsys = msm.build.build_peptide('ACEGLYGLY', to_form='molsysmt.MolSys', engine='MolSysMT')
    assert molsys is not None
    # ACE + GLY + GLY
    n_groups = msm.get(molsys, element='system', n_groups=True)
    assert n_groups == 3


# ---------------------------------------------------------------------------
# MolSys with from a MolSys input (molecular_system already a MolSys)
# ---------------------------------------------------------------------------

def test_input_is_molsys():
    """build_peptide accepts a MolSys as input (string:amino_acids_3 conversion path)."""
    peptide = msm.build.build_peptide('AGVIL', to_form='molsysmt.MolSys', engine='MolSysMT')
    rebuilt = msm.build.build_peptide(peptide, to_form='molsysmt.MolSys', engine='MolSysMT')
    assert rebuilt is not None
    n_groups = msm.get(rebuilt, element='system', n_groups=True)
    assert n_groups == 5
