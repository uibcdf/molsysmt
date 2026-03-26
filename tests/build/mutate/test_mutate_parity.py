"""
Parity tests for mutate: MolSysMT engine vs PDBFixer engine.

Known difference between engines:
  - engine='PDBFixer' calls addMissingAtoms() after mutation, which adds OXT
    to the C-terminal residue if absent.  engine='MolSysMT' only adds what
    its own add_missing_heavy_atoms detects as missing — for a peptide built
    without OXT, OXT will not be added.

The tests therefore focus on what must agree:
  - Group names after mutation.
  - Backbone heavy atoms (N, CA, C, O) present in every mutated group.
  - Sidechain heavy atoms (by name) present in every mutated group.
  - Mutations that shrink the sidechain (VAL→GLY) reduce heavy-atom count.
  - Mutations that grow the sidechain (VAL→TRP) increase heavy-atom count.
"""

import pytest
import molsysmt as msm


@pytest.fixture(scope='module')
def ala_val_pro():
    return msm.build.build_peptide('AlaValPro', engine='MolSysMT')


@pytest.fixture(scope='module')
def ala_val_pro_heavy():
    """Heavy-only version so OXT-related differences do not interfere."""
    mol = msm.build.build_peptide('AlaValPro', engine='MolSysMT',
                                  to_form='molsysmt.MolSys')
    return msm.remove(mol, selection='atom_type=="H"')


# ── Group names ───────────────────────────────────────────────────────────────

def test_parity_group_name_val_to_gly(ala_val_pro):
    """Both engines rename group 1 to GLY."""
    for eng in ('MolSysMT', 'PDBFixer'):
        r = msm.build.mutate(ala_val_pro, mutations={1: 'GLY'},
                              keys='group_index', engine=eng)
        names = msm.get(r, element='group', group_name=True)
        assert names[1] == 'GLY', f"{eng}: names[1] = {names[1]}"


def test_parity_group_names_other_unchanged(ala_val_pro):
    """ALA (group 0) and PRO (group 2) are unchanged in both engines."""
    for eng in ('MolSysMT', 'PDBFixer'):
        r = msm.build.mutate(ala_val_pro, mutations={1: 'GLY'},
                              keys='group_index', engine=eng)
        names = msm.get(r, element='group', group_name=True)
        assert names[0] == 'ALA', f"{eng}: names[0] = {names[0]}"
        assert names[2] == 'PRO', f"{eng}: names[2] = {names[2]}"


# ── Backbone atoms ────────────────────────────────────────────────────────────

def test_parity_backbone_present_both_engines(ala_val_pro_heavy):
    """N, CA, C, O must be present in the mutated GLY residue for both engines."""
    for eng in ('MolSysMT', 'PDBFixer'):
        r = msm.build.mutate(ala_val_pro_heavy, mutations={1: 'GLY'},
                              keys='group_index', engine=eng)
        heavy = msm.get(r, element='atom',
                         selection='group_index==1 and atom_type!="H"',
                         atom_name=True)
        for bb in ('N', 'CA', 'C', 'O'):
            assert bb in heavy, f"{eng}: backbone atom {bb} missing from GLY"


# ── Sidechain removal (VAL→GLY) ───────────────────────────────────────────────

def test_parity_gly_no_sidechain_native(ala_val_pro_heavy):
    """MolSysMT: GLY has only backbone heavy atoms {N, CA, C, O}."""
    r = msm.build.mutate(ala_val_pro_heavy, mutations={1: 'GLY'},
                          keys='group_index', engine='MolSysMT')
    heavy = msm.get(r, element='atom',
                     selection='group_index==1 and atom_type!="H"',
                     atom_name=True)
    assert set(heavy) == {'N', 'CA', 'C', 'O'}


def test_parity_gly_no_sidechain_pdbfixer(ala_val_pro_heavy):
    """PDBFixer: GLY has only backbone heavy atoms {N, CA, C, O}."""
    r = msm.build.mutate(ala_val_pro_heavy, mutations={1: 'GLY'},
                          keys='group_index', engine='PDBFixer')
    heavy = msm.get(r, element='atom',
                     selection='group_index==1 and atom_type!="H"',
                     atom_name=True)
    # PDBFixer may add OXT to the C-terminal PRO (not the mutated GLY); GLY itself
    # should still have only backbone atoms.
    assert set(heavy) == {'N', 'CA', 'C', 'O'}


def test_parity_val_to_gly_reduces_heavy_count(ala_val_pro_heavy):
    """VAL→GLY reduces heavy-atom count in both engines."""
    n_before = msm.get(ala_val_pro_heavy, n_atoms=True)
    for eng in ('MolSysMT', 'PDBFixer'):
        r = msm.build.mutate(ala_val_pro_heavy, mutations={1: 'GLY'},
                              keys='group_index', engine=eng)
        # PDBFixer may add OXT to C-terminal, so use ≤ instead of <
        n_after_in_g1 = msm.get(r, element='atom',
                                  selection='group_index==1 and atom_type!="H"',
                                  n_atoms=True)
        assert n_after_in_g1 == 4, f"{eng}: GLY group 1 has {n_after_in_g1} heavy atoms (expected 4)"


# ── Sidechain build (VAL→TRP) ─────────────────────────────────────────────────

def test_parity_trp_sidechain_present_native(ala_val_pro_heavy):
    """MolSysMT: TRP sidechain contains the expected indole atoms."""
    r = msm.build.mutate(ala_val_pro_heavy, mutations={1: 'TRP'},
                          keys='group_index', engine='MolSysMT')
    heavy = set(msm.get(r, element='atom',
                         selection='group_index==1 and atom_type!="H"',
                         atom_name=True))
    for expected in ('CB', 'CG', 'CD1', 'CD2', 'NE1', 'CE2', 'CE3', 'CZ2', 'CZ3', 'CH2'):
        assert expected in heavy, f"MolSysMT: TRP atom {expected} missing"


def test_parity_trp_sidechain_present_pdbfixer(ala_val_pro_heavy):
    """PDBFixer: TRP sidechain contains the expected indole atoms."""
    r = msm.build.mutate(ala_val_pro_heavy, mutations={1: 'TRP'},
                          keys='group_index', engine='PDBFixer')
    heavy = set(msm.get(r, element='atom',
                         selection='group_index==1 and atom_type!="H"',
                         atom_name=True))
    for expected in ('CB', 'CG', 'CD1', 'CD2', 'NE1', 'CE2', 'CE3', 'CZ2', 'CZ3', 'CH2'):
        assert expected in heavy, f"PDBFixer: TRP atom {expected} missing"


# ── Multiple simultaneous mutations ──────────────────────────────────────────

def test_parity_multiple_mutations_group_names(ala_val_pro_heavy):
    """Both engines apply multiple mutations and produce correct group names."""
    for eng in ('MolSysMT', 'PDBFixer'):
        r = msm.build.mutate(ala_val_pro_heavy, mutations={0: 'LEU', 2: 'SER'},
                              keys='group_index', engine=eng)
        names = msm.get(r, element='group', group_name=True)
        assert names[0] == 'LEU', f"{eng}: names[0] = {names[0]}"
        assert names[1] == 'VAL', f"{eng}: names[1] = {names[1]}"  # unchanged
        assert names[2] == 'SER', f"{eng}: names[2] = {names[2]}"
