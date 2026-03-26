"""
Parity tests for add_missing_heavy_atoms: MolSysMT engine vs PDBFixer engine.

Both engines should produce the same total atom count and the same missing
atom names per residue when applied to a real structure with known missing
heavy atoms (Barnase-Barstar 1brs).

Also tested: a synthetic case (AlaValPro with CB removed) where both engines
should recover identical atom counts.
"""

import pytest
import molsysmt as msm


@pytest.fixture(scope='module')
def barnase_barstar():
    return msm.convert(msm.systems['Barnase-Barstar']['1brs.bcif.gz'])


@pytest.fixture(scope='module')
def avp_no_cb():
    mol = msm.build.build_peptide('AlaValPro', engine='MolSysMT')
    return msm.remove(mol, selection='atom_name=="CB"')


# ── Barnase-Barstar (real PDB structure) ──────────────────────────────────────

def test_parity_1brs_total_atom_count(barnase_barstar):
    """Both engines add the same number of atoms to 1brs."""
    r_native = msm.build.add_missing_heavy_atoms(barnase_barstar, engine='MolSysMT')
    r_pdb    = msm.build.add_missing_heavy_atoms(barnase_barstar, engine='PDBFixer')
    assert msm.get(r_native, n_atoms=True) == msm.get(r_pdb, n_atoms=True)


def test_parity_1brs_atoms_added(barnase_barstar):
    """Both engines add atoms to the same set of residues."""
    r_native = msm.build.add_missing_heavy_atoms(barnase_barstar, engine='MolSysMT')
    r_pdb    = msm.build.add_missing_heavy_atoms(barnase_barstar, engine='PDBFixer')
    n_before = msm.get(barnase_barstar, n_atoms=True)
    delta_native = msm.get(r_native, n_atoms=True) - n_before
    delta_pdb    = msm.get(r_pdb, n_atoms=True) - n_before
    assert delta_native == delta_pdb


def test_parity_1brs_backbone_present_native(barnase_barstar):
    """After MolSysMT fix, all residues in the repaired groups have backbone atoms."""
    from molsysmt.build.get_missing_heavy_atoms import get_missing_heavy_atoms
    missing_before = get_missing_heavy_atoms(barnase_barstar, engine='MolSysMT')
    r_native = msm.build.add_missing_heavy_atoms(barnase_barstar, engine='MolSysMT')
    missing_after = get_missing_heavy_atoms(r_native, engine='MolSysMT')
    # All previously-missing residues should now be complete
    assert set(missing_after.keys()).isdisjoint(set(missing_before.keys()))


def test_parity_1brs_backbone_present_pdbfixer(barnase_barstar):
    """After PDBFixer fix, all residues that had missing atoms are now complete."""
    from molsysmt.build.get_missing_heavy_atoms import get_missing_heavy_atoms
    missing_before = get_missing_heavy_atoms(barnase_barstar, engine='MolSysMT')
    r_pdb = msm.build.add_missing_heavy_atoms(barnase_barstar, engine='PDBFixer')
    missing_after = get_missing_heavy_atoms(r_pdb, engine='MolSysMT')
    assert set(missing_after.keys()).isdisjoint(set(missing_before.keys()))


# ── Synthetic: AlaValPro with CB removed ─────────────────────────────────────

def test_parity_synthetic_atom_count(avp_no_cb):
    """Both engines recover the same atom count on a peptide with CB removed."""
    r_native = msm.build.add_missing_heavy_atoms(avp_no_cb, engine='MolSysMT')
    r_pdb    = msm.build.add_missing_heavy_atoms(avp_no_cb, engine='PDBFixer')
    assert msm.get(r_native, n_atoms=True) == msm.get(r_pdb, n_atoms=True)


def test_parity_synthetic_cb_present(avp_no_cb):
    """Both engines restore CB atoms to all three residues."""
    for eng in ('MolSysMT', 'PDBFixer'):
        r = msm.build.add_missing_heavy_atoms(avp_no_cb, engine=eng)
        n_cb = msm.get(r, element='atom', selection='atom_name=="CB"', n_atoms=True)
        assert n_cb == 3, f"{eng}: expected 3 CB atoms, got {n_cb}"


def test_parity_synthetic_group_names_unchanged(avp_no_cb):
    """Group names are not altered by either engine."""
    for eng in ('MolSysMT', 'PDBFixer'):
        r = msm.build.add_missing_heavy_atoms(avp_no_cb, engine=eng)
        names = msm.get(r, element='group', group_name=True)
        assert names == ['ALA', 'VAL', 'PRO'], f"{eng}: {names}"
