"""
Tests for solvate(engine='MolSysMT') — no external dependencies required.
"""

import pytest
import numpy as np
import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.fixture(scope='module')
def ala_val_pro():
    return msm.build.build_peptide('AlaValPro', engine='MolSysMT')


# ── basic smoke test ──────────────────────────────────────────────────────────

def test_solvate_returns_molsys(ala_val_pro):
    solvated = msm.build.solvate(ala_val_pro, box_shape='cubic',
                                  clearance='10 angstroms',
                                  n_cations=0, n_anions=0,
                                  water_model='TIP3P', engine='MolSysMT')
    assert solvated is not None


def test_solvate_atom_count_increases(ala_val_pro):
    n_solute = msm.get(ala_val_pro, n_atoms=True)
    solvated = msm.build.solvate(ala_val_pro, box_shape='cubic',
                                  clearance='10 angstroms',
                                  n_cations=0, n_anions=0,
                                  water_model='TIP3P', engine='MolSysMT')
    n_solvated = msm.get(solvated, n_atoms=True)
    assert n_solvated > n_solute


def test_solvate_has_water_molecules(ala_val_pro):
    solvated = msm.build.solvate(ala_val_pro, box_shape='cubic',
                                  clearance='10 angstroms',
                                  n_cations=0, n_anions=0,
                                  water_model='TIP3P', engine='MolSysMT')
    n_water = msm.get(solvated, element='molecule',
                      selection='molecule_type=="water"', n_molecules=True)
    assert n_water > 0


# ── box geometry ──────────────────────────────────────────────────────────────

def test_solvate_cubic_box_is_cube(ala_val_pro):
    """All three box diagonal elements must be equal for a cubic box."""
    solvated = msm.build.solvate(ala_val_pro, box_shape='cubic',
                                  clearance='10 angstroms',
                                  n_cations=0, n_anions=0,
                                  water_model='TIP3P', engine='MolSysMT')
    box = puw.get_value(msm.get(solvated, box=True), to_unit='nm')[0]
    assert abs(box[0, 0] - box[1, 1]) < 1e-9
    assert abs(box[0, 0] - box[2, 2]) < 1e-9


def test_solvate_clearance_respected(ala_val_pro):
    """Box side must be at least solute_extent + 2*clearance."""
    clearance_nm = 1.0   # 10 angstroms
    solvated = msm.build.solvate(ala_val_pro, box_shape='cubic',
                                  clearance='10 angstroms',
                                  n_cations=0, n_anions=0,
                                  water_model='TIP3P', engine='MolSysMT')
    coords = puw.get_value(msm.get(solvated, element='atom',
                                   selection='molecule_type!="water"',
                                   coordinates=True), to_unit='nm')[0]
    box = puw.get_value(msm.get(solvated, box=True), to_unit='nm')[0]
    extent = coords.max(axis=0) - coords.min(axis=0)
    for dim in range(3):
        assert box[dim, dim] >= extent[dim] + 2 * clearance_nm - 1e-3


def test_solvate_box_orthogonal(ala_val_pro):
    """Off-diagonal elements must be zero for a cubic/rectangular box."""
    solvated = msm.build.solvate(ala_val_pro, box_shape='cubic',
                                  clearance='10 angstroms',
                                  n_cations=0, n_anions=0,
                                  water_model='TIP3P', engine='MolSysMT')
    box = puw.get_value(msm.get(solvated, box=True), to_unit='nm')[0]
    assert abs(box[0, 1]) < 1e-12
    assert abs(box[0, 2]) < 1e-12
    assert abs(box[1, 2]) < 1e-12


# ── no-overlap guarantee ──────────────────────────────────────────────────────

def test_solvate_no_overlap_with_solute(ala_val_pro):
    """No water O atom should be closer than 2.0 Å to any solute atom."""
    solvated = msm.build.solvate(ala_val_pro, box_shape='cubic',
                                  clearance='10 angstroms',
                                  n_cations=0, n_anions=0,
                                  water_model='TIP3P', engine='MolSysMT')
    solute_xyz = puw.get_value(
        msm.get(solvated, element='atom',
                selection='molecule_type!="water"', coordinates=True),
        to_unit='angstroms'
    )[0]
    water_o_xyz = puw.get_value(
        msm.get(solvated, element='atom',
                selection='atom_name=="O" and molecule_type=="water"',
                coordinates=True),
        to_unit='angstroms'
    )[0]
    min_threshold = 2.0   # angstroms
    for o_pos in water_o_xyz:
        dists = np.linalg.norm(solute_xyz - o_pos, axis=1)
        assert dists.min() >= min_threshold - 1e-3


# ── water-model variants ──────────────────────────────────────────────────────

def test_solvate_spce_water_model(ala_val_pro):
    solvated = msm.build.solvate(ala_val_pro, box_shape='cubic',
                                  clearance='10 angstroms',
                                  n_cations=0, n_anions=0,
                                  water_model='SPC/E', engine='MolSysMT')
    n_water = msm.get(solvated, element='molecule',
                      selection='molecule_type=="water"', n_molecules=True)
    assert n_water > 0


def test_solvate_spc_water_model(ala_val_pro):
    """SPC water uses spc216.gro (1.86206 nm tile box)."""
    solvated = msm.build.solvate(ala_val_pro, box_shape='cubic',
                                  clearance='10 angstroms',
                                  n_cations=0, n_anions=0,
                                  water_model='SPC', engine='MolSysMT')
    n_water = msm.get(solvated, element='molecule',
                      selection='molecule_type=="water"', n_molecules=True)
    assert n_water > 0


# ── error handling ────────────────────────────────────────────────────────────

def test_solvate_raises_for_non_orthogonal_box(ala_val_pro):
    with pytest.raises(NotImplementedError):
        msm.build.solvate(ala_val_pro, box_shape='truncated octahedral',
                           n_cations=0, n_anions=0, engine='MolSysMT')


def test_solvate_raises_for_rhombic_dodecahedral(ala_val_pro):
    with pytest.raises(NotImplementedError):
        msm.build.solvate(ala_val_pro, box_shape='rhombic dodecahedral',
                           n_cations=0, n_anions=0, engine='MolSysMT')


def test_solvate_explicit_cation(ala_val_pro):
    """Requesting n_cations=1 adds exactly one Na+ ion."""
    solvated = msm.build.solvate(ala_val_pro, box_shape='cubic',
                                  n_cations=1, n_anions=0,
                                  engine='MolSysMT', to_form='molsysmt.MolSys')
    ion_names = msm.get(solvated, element='group',
                         selection='group_type=="ion"', group_name=True)
    assert ion_names == ['NA']


def test_solvate_explicit_anion(ala_val_pro):
    """Requesting n_anions=1 adds exactly one Cl- ion."""
    solvated = msm.build.solvate(ala_val_pro, box_shape='cubic',
                                  n_cations=0, n_anions=1,
                                  engine='MolSysMT', to_form='molsysmt.MolSys')
    ion_names = msm.get(solvated, element='group',
                         selection='group_type=="ion"', group_name=True)
    assert ion_names == ['CL']


def test_solvate_ion_min_distance_from_solute(ala_val_pro):
    """Ion is placed at least 5 Å from any solute atom."""
    import numpy as np
    from molsysmt import pyunitwizard as puw

    solvated = msm.build.solvate(ala_val_pro, box_shape='cubic',
                                  n_cations=1, n_anions=0,
                                  engine='MolSysMT', to_form='molsysmt.MolSys')
    solute_xyz = puw.get_value(
        msm.get(solvated, element='atom',
                selection='molecule_type!="water" and group_type!="ion"',
                coordinates=True), to_unit='nm')[0]
    ion_xyz = puw.get_value(
        msm.get(solvated, element='atom',
                selection='group_type=="ion"',
                coordinates=True), to_unit='nm')[0]
    for ion_pos in ion_xyz:
        min_d = np.sqrt(((solute_xyz - ion_pos) ** 2).sum(axis=1)).min()
        assert min_d >= 0.5, f"Ion placed {min_d * 10:.2f} Å from solute (min 5.0 Å required)"


def test_solvate_raises_for_unsupported_water_model(ala_val_pro):
    with pytest.raises(NotImplementedError):
        msm.build.solvate(ala_val_pro, box_shape='cubic',
                           n_cations=0, n_anions=0,
                           water_model='TIP5P', engine='MolSysMT')
