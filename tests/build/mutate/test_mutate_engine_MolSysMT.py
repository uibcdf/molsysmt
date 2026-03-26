"""
Tests for mutate(engine='MolSysMT') — no external dependencies required.
"""

import pytest
import molsysmt as msm


@pytest.fixture(scope='module')
def ala_val_pro():
    return msm.build.build_peptide('AlaValPro', engine='MolSysMT')


# ── group name changes ────────────────────────────────────────────────────────

def test_mutate_group_name_changes(ala_val_pro):
    mutated = msm.build.mutate(ala_val_pro, mutations={1: 'GLY'},
                                keys='group_index', engine='MolSysMT')
    names = msm.get(mutated, element='group', group_name=True)
    assert names[1] == 'GLY'


def test_mutate_other_groups_unchanged(ala_val_pro):
    mutated = msm.build.mutate(ala_val_pro, mutations={1: 'GLY'},
                                keys='group_index', engine='MolSysMT')
    names = msm.get(mutated, element='group', group_name=True)
    assert names[0] == 'ALA'
    assert names[2] == 'PRO'


# ── atom counts ───────────────────────────────────────────────────────────────

def test_mutate_val_to_gly_atom_count(ala_val_pro):
    """VAL→GLY: loses CB, CG1, CG2 sidechain (3 heavy + their H's)."""
    mutated = msm.build.mutate(ala_val_pro, mutations={1: 'GLY'},
                                keys='group_index', engine='MolSysMT')
    n_after = msm.get(mutated, n_atoms=True)
    n_before = msm.get(ala_val_pro, n_atoms=True)
    assert n_after < n_before


def test_mutate_val_to_trp_atom_count(ala_val_pro):
    """VAL→TRP: gains a large indole sidechain."""
    mutated = msm.build.mutate(ala_val_pro, mutations={1: 'TRP'},
                                keys='group_index', engine='MolSysMT')
    n_after = msm.get(mutated, n_atoms=True)
    n_before = msm.get(ala_val_pro, n_atoms=True)
    assert n_after > n_before


def test_mutate_gly_has_only_backbone(ala_val_pro):
    """GLY has no sidechain: only N, CA, C, O (+ H atoms)."""
    mutated = msm.build.mutate(ala_val_pro, mutations={1: 'GLY'},
                                keys='group_index', engine='MolSysMT')
    atom_names = msm.get(mutated, element='atom',
                          selection='group_index==1 and atom_type!="H"',
                          atom_name=True)
    assert set(atom_names) == {'N', 'CA', 'C', 'O'}


def test_mutate_trp_has_full_indole(ala_val_pro):
    """TRP sidechain must contain the full indole ring."""
    mutated = msm.build.mutate(ala_val_pro, mutations={1: 'TRP'},
                                keys='group_index', engine='MolSysMT')
    heavy = msm.get(mutated, element='atom',
                    selection='group_index==1 and atom_type!="H"',
                    atom_name=True)
    heavy_set = set(heavy)
    for expected in ('CB', 'CG', 'CD1', 'CD2', 'NE1', 'CE2', 'CE3', 'CZ2', 'CZ3', 'CH2'):
        assert expected in heavy_set, f"Missing TRP atom: {expected}"


# ── backbone retained ─────────────────────────────────────────────────────────

def test_mutate_backbone_atoms_present(ala_val_pro):
    """Backbone atoms N, CA, C, O must be present after any mutation."""
    mutated = msm.build.mutate(ala_val_pro, mutations={1: 'LEU'},
                                keys='group_index', engine='MolSysMT')
    heavy = msm.get(mutated, element='atom',
                    selection='group_index==1 and atom_type!="H"',
                    atom_name=True)
    for bb in ('N', 'CA', 'C', 'O'):
        assert bb in heavy


# ── hydrogens ─────────────────────────────────────────────────────────────────

def test_mutate_preserves_hydrogens_when_present(ala_val_pro):
    """If input has H atoms, output should also have H atoms."""
    n_h_before = len(msm.get(ala_val_pro, element='atom',
                              selection='atom_type=="H"', atom_index=True))
    mutated = msm.build.mutate(ala_val_pro, mutations={1: 'ALA'},
                                keys='group_index', engine='MolSysMT')
    n_h_after = len(msm.get(mutated, element='atom',
                             selection='atom_type=="H"', atom_index=True))
    assert n_h_after > 0
    # ALA has fewer H than VAL sidechain, so totals may differ — just check presence
    _ = n_h_before  # used for context only


# ── mutation specification formats ────────────────────────────────────────────

def test_mutate_via_string_list(ala_val_pro):
    mutated = msm.build.mutate(ala_val_pro, mutations=['VAL-1-GLY'],
                                engine='MolSysMT')
    names = msm.get(mutated, element='group', group_name=True)
    assert names[1] == 'GLY'


def test_mutate_via_group_index_dict(ala_val_pro):
    mutated = msm.build.mutate(ala_val_pro, mutations={1: 'ALA'},
                                keys='group_index', engine='MolSysMT')
    names = msm.get(mutated, element='group', group_name=True)
    assert names[1] == 'ALA'


def test_mutate_via_group_id_dict(ala_val_pro):
    mutated = msm.build.mutate(ala_val_pro, mutations={'1': 'ALA'},
                                keys='group_id', engine='MolSysMT')
    names = msm.get(mutated, element='group', group_name=True)
    assert names[1] == 'ALA'


def test_mutate_multiple_at_once(ala_val_pro):
    mutated = msm.build.mutate(ala_val_pro, mutations={0: 'LEU', 2: 'SER'},
                                keys='group_index', engine='MolSysMT')
    names = msm.get(mutated, element='group', group_name=True)
    assert names[0] == 'LEU'
    assert names[1] == 'VAL'   # unchanged
    assert names[2] == 'SER'
