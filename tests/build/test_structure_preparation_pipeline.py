"""
End-to-end integration test for the structure preparation pipeline.

Covers the canonical sequence:
    add_missing_heavy_atoms
    → add_missing_terminal_cappings
    → add_missing_hydrogens
    → solvate (with ion neutralization)

All steps use engine='MolSysMT' (no external dependencies).

The test system is a heavy-only version of Trp-Cage (1L2Y, structure 0),
which is small (~300 atoms) and finishes quickly.
"""

import pytest
import molsysmt as msm


@pytest.fixture(scope='module')
def trpcage_heavy():
    """Trp-Cage, first structure, heavy atoms only."""
    mol = msm.convert(msm.systems['Trp-Cage']['1l2y.h5msm'], structure_indices=0)
    return msm.remove(mol, selection='atom_type=="H"')


@pytest.fixture(scope='module')
def prepared(trpcage_heavy):
    """Full pipeline output: heavy→cappings→H→solvated."""
    mol = msm.build.add_missing_heavy_atoms(trpcage_heavy, engine='MolSysMT')
    mol = msm.build.add_missing_terminal_cappings(mol, engine='MolSysMT')
    mol = msm.build.add_missing_hydrogens(mol, pH=7.4, engine='MolSysMT')
    mol = msm.build.solvate(
        mol,
        box_shape='cubic',
        clearance='8 angstroms',
        water_model='TIP3P',
        n_cations='neutralize',
        n_anions='neutralize',
        ionic_strength='0.0 molar',
        engine='MolSysMT',
        to_form='molsysmt.MolSys',
    )
    return mol


# ── Step 1: heavy atoms ───────────────────────────────────────────────────────

def test_pipeline_heavy_atoms_added(trpcage_heavy):
    """add_missing_heavy_atoms increases the atom count."""
    n_before = msm.get(trpcage_heavy, n_atoms=True)
    result = msm.build.add_missing_heavy_atoms(trpcage_heavy, engine='MolSysMT')
    assert msm.get(result, n_atoms=True) >= n_before


def test_pipeline_no_missing_heavy_atoms_after_step1(trpcage_heavy):
    """After add_missing_heavy_atoms no heavy atoms are reported missing."""
    result = msm.build.add_missing_heavy_atoms(trpcage_heavy, engine='MolSysMT')
    missing = msm.build.get_missing_heavy_atoms(result, engine='MolSysMT')
    assert missing == {}


# ── Step 2: terminal cappings ─────────────────────────────────────────────────

def test_pipeline_oxt_present_after_step2(trpcage_heavy):
    """After add_missing_terminal_cappings the C-terminus has OXT."""
    mol = msm.build.add_missing_heavy_atoms(trpcage_heavy, engine='MolSysMT')
    mol = msm.build.add_missing_terminal_cappings(mol, engine='MolSysMT')
    oxt_count = msm.get(mol, element='atom', selection='atom_name=="OXT"', n_atoms=True)
    assert oxt_count >= 1


def test_pipeline_no_missing_cappings_after_step2(trpcage_heavy):
    """After add_missing_terminal_cappings no terminal atoms are reported missing."""
    mol = msm.build.add_missing_heavy_atoms(trpcage_heavy, engine='MolSysMT')
    mol = msm.build.add_missing_terminal_cappings(mol, engine='MolSysMT')
    missing = msm.build.get_missing_terminal_cappings(mol, engine='MolSysMT')
    assert missing == {}


# ── Step 3: hydrogens ─────────────────────────────────────────────────────────

def test_pipeline_hydrogens_added(trpcage_heavy):
    """After add_missing_hydrogens the system contains H atoms."""
    mol = msm.build.add_missing_heavy_atoms(trpcage_heavy, engine='MolSysMT')
    mol = msm.build.add_missing_terminal_cappings(mol, engine='MolSysMT')
    mol = msm.build.add_missing_hydrogens(mol, pH=7.4, engine='MolSysMT')
    n_h = msm.get(mol, element='atom', selection='atom_type=="H"', n_atoms=True)
    assert n_h > 0


def test_pipeline_heavy_count_unchanged_by_hydrogens(trpcage_heavy):
    """add_missing_hydrogens does not change the heavy atom count."""
    mol = msm.build.add_missing_heavy_atoms(trpcage_heavy, engine='MolSysMT')
    mol = msm.build.add_missing_terminal_cappings(mol, engine='MolSysMT')
    n_heavy = msm.get(mol, element='atom', selection='atom_type!="H"', n_atoms=True)
    mol = msm.build.add_missing_hydrogens(mol, pH=7.4, engine='MolSysMT')
    n_heavy_after = msm.get(mol, element='atom', selection='atom_type!="H"', n_atoms=True)
    assert n_heavy_after == n_heavy


# ── Step 4: solvation ─────────────────────────────────────────────────────────

def test_pipeline_solvated_has_water(prepared):
    """Solvated system contains water molecules."""
    n_water = msm.get(prepared, element='molecule',
                       selection='molecule_type=="water"', n_molecules=True)
    assert n_water > 0


def test_pipeline_solvated_has_box(prepared):
    """Solvated system has box vectors."""
    box = prepared.structures.box
    assert box is not None


def test_pipeline_neutralization_correct(prepared):
    """Trp-Cage has charge +1 → exactly 1 Cl- ion added for neutralization."""
    n_ions = msm.get(prepared, element='molecule',
                      selection='molecule_type=="ion"', n_molecules=True)
    ion_names = msm.get(prepared, element='group',
                         selection='group_type=="ion"', group_name=True)
    assert n_ions == 1
    assert ion_names == ['CL']


def test_pipeline_solute_present_after_solvation(prepared):
    """Peptide/protein chain is still present after solvation."""
    n_peptide = msm.get(prepared, element='molecule',
                         selection='molecule_type in ["protein", "peptide"]',
                         n_molecules=True)
    assert n_peptide >= 1


def test_pipeline_no_water_overlaps_solute(prepared):
    """No water oxygen is closer than 2.0 Å to any solute atom."""
    import numpy as np
    from molsysmt import pyunitwizard as puw

    protein_xyz = puw.get_value(
        msm.get(prepared, element='atom',
                selection='molecule_type in ["protein", "peptide"]',
                coordinates=True), to_unit='nm')[0]

    water_o_xyz = puw.get_value(
        msm.get(prepared, element='atom',
                selection='molecule_type=="water" and atom_name=="O"',
                coordinates=True), to_unit='nm')[0]

    threshold_nm = 0.20   # 2.0 Å
    for w_pos in water_o_xyz:
        min_d = np.sqrt(((protein_xyz - w_pos) ** 2).sum(axis=1)).min()
        assert min_d >= threshold_nm, (
            f"Water O at {min_d * 10:.2f} Å from protein (threshold 2.0 Å)"
        )
