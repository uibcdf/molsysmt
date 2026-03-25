"""
Contract tests for molsysmt.MolecularMechanicsDict form getters.

The MolecularMechanicsDict is a plain Python dict with well-known keys.
These tests exercise every getter in get_mechanical_attributes.py:

- get_atom_index_from_atom (all / subset)
- get_n_atoms_from_atom (all / subset / missing charge arrays)
- get_formal_charge_from_atom (all / subset / missing key)
- get_partial_charge_from_atom (all / subset / missing key)
- get_n_atoms_from_system
- all 14 system-level getters (forcefield, non_bonded_method, …)
"""

import pytest
import numpy as np
import molsysmt as msm
from molsysmt.form.molsysmt_MolecularMechanicsDict import get_mechanical_attributes as gma


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

N_ATOMS = 5


@pytest.fixture
def full_mmdict():
    """A MolecularMechanicsDict populated with all known keys."""
    from molsysmt import pyunitwizard as puw

    return {
        'formal_charge': np.zeros(N_ATOMS, dtype=int),
        'partial_charge': np.ones(N_ATOMS, dtype=float) * 0.1,
        'forcefield': ['amber14-all.xml', 'amber14/tip3pfb.xml'],
        'water_model': 'TIP3P-FB',
        'implicit_solvent': None,
        'non_bonded_method': 'PME',
        'cutoff_distance': puw.quantity(1.0, 'nm'),
        'switch_distance': puw.quantity(0.9, 'nm'),
        'dispersion_correction': True,
        'ewald_error_tolerance': 1e-4,
        'constraints': 'HBonds',
        'flexible_constraints': False,
        'rigid_water': True,
        'hydrogen_mass': puw.quantity(1.5, 'amu'),
        'salt_concentration': puw.quantity(0.15, 'mol/L'),
        'kappa': None,
        'solute_dielectric': 1.0,
        'solvent_dielectric': 78.5,
    }


@pytest.fixture
def empty_mmdict():
    """A MolecularMechanicsDict with no charge arrays (all None)."""
    return {
        'formal_charge': None,
        'partial_charge': None,
        'forcefield': None,
        'water_model': None,
        'implicit_solvent': None,
        'non_bonded_method': None,
        'cutoff_distance': None,
        'switch_distance': None,
        'dispersion_correction': None,
        'ewald_error_tolerance': None,
        'constraints': None,
        'flexible_constraints': None,
        'rigid_water': None,
        'hydrogen_mass': None,
        'salt_concentration': None,
        'kappa': None,
        'solute_dielectric': None,
        'solvent_dielectric': None,
    }


# ---------------------------------------------------------------------------
# get_n_atoms_from_atom / get_n_atoms_from_system
# ---------------------------------------------------------------------------

def test_n_atoms_all_from_formal_charge(full_mmdict):
    n = gma.get_n_atoms_from_atom(full_mmdict, skip_digestion=True)
    assert n == N_ATOMS


def test_n_atoms_subset(full_mmdict):
    n = gma.get_n_atoms_from_atom(full_mmdict, indices=[0, 1, 2], skip_digestion=True)
    assert n == 3


def test_n_atoms_no_charges(empty_mmdict):
    n = gma.get_n_atoms_from_atom(empty_mmdict, skip_digestion=True)
    assert n is None


def test_n_atoms_from_system(full_mmdict):
    n = gma.get_n_atoms_from_system(full_mmdict, skip_digestion=True)
    assert n == N_ATOMS


# ---------------------------------------------------------------------------
# get_atom_index_from_atom
# ---------------------------------------------------------------------------

def test_atom_index_all(full_mmdict):
    idx = gma.get_atom_index_from_atom(full_mmdict, skip_digestion=True)
    np.testing.assert_array_equal(idx, np.arange(N_ATOMS))


def test_atom_index_subset(full_mmdict):
    subset = np.array([1, 3])
    idx = gma.get_atom_index_from_atom(full_mmdict, indices=subset, skip_digestion=True)
    np.testing.assert_array_equal(idx, subset)


# ---------------------------------------------------------------------------
# get_formal_charge_from_atom
# ---------------------------------------------------------------------------

def test_formal_charge_all(full_mmdict):
    fc = gma.get_formal_charge_from_atom(full_mmdict, skip_digestion=True)
    assert fc is not None
    assert len(fc) == N_ATOMS


def test_formal_charge_subset(full_mmdict):
    fc = gma.get_formal_charge_from_atom(full_mmdict, indices=[0, 1], skip_digestion=True)
    assert len(fc) == 2


def test_formal_charge_missing(empty_mmdict):
    fc = gma.get_formal_charge_from_atom(empty_mmdict, skip_digestion=True)
    assert fc is None


# ---------------------------------------------------------------------------
# get_partial_charge_from_atom
# ---------------------------------------------------------------------------

def test_partial_charge_all(full_mmdict):
    pc = gma.get_partial_charge_from_atom(full_mmdict, skip_digestion=True)
    assert pc is not None
    assert len(pc) == N_ATOMS


def test_partial_charge_subset(full_mmdict):
    pc = gma.get_partial_charge_from_atom(full_mmdict, indices=[2, 4], skip_digestion=True)
    assert len(pc) == 2


def test_partial_charge_missing(empty_mmdict):
    pc = gma.get_partial_charge_from_atom(empty_mmdict, skip_digestion=True)
    assert pc is None


# ---------------------------------------------------------------------------
# System-level getters
# ---------------------------------------------------------------------------

def test_get_forcefield(full_mmdict):
    ff = gma.get_forcefield_from_system(full_mmdict, skip_digestion=True)
    assert ff is not None
    assert 'amber14-all.xml' in ff


def test_get_non_bonded_method(full_mmdict):
    assert gma.get_non_bonded_method_from_system(full_mmdict, skip_digestion=True) == 'PME'


def test_get_cutoff_distance(full_mmdict):
    assert gma.get_cutoff_distance_from_system(full_mmdict, skip_digestion=True) is not None


def test_get_switch_distance(full_mmdict):
    assert gma.get_switch_distance_from_system(full_mmdict, skip_digestion=True) is not None


def test_get_dispersion_correction(full_mmdict):
    assert gma.get_dispersion_correction_from_system(full_mmdict, skip_digestion=True) is True


def test_get_ewald_error_tolerance(full_mmdict):
    assert gma.get_ewald_error_tolerance_from_system(full_mmdict, skip_digestion=True) == 1e-4


def test_get_hydrogen_mass(full_mmdict):
    assert gma.get_hydrogen_mass_from_system(full_mmdict, skip_digestion=True) is not None


def test_get_constraints(full_mmdict):
    assert gma.get_constraints_from_system(full_mmdict, skip_digestion=True) == 'HBonds'


def test_get_flexible_constraints(full_mmdict):
    assert gma.get_flexible_constraints_from_system(full_mmdict, skip_digestion=True) is False


def test_get_water_model(full_mmdict):
    assert gma.get_water_model_from_system(full_mmdict, skip_digestion=True) == 'TIP3P-FB'


def test_get_rigid_water(full_mmdict):
    assert gma.get_rigid_water_from_system(full_mmdict, skip_digestion=True) is True


def test_get_implicit_solvent(full_mmdict):
    val = gma.get_implicit_solvent_from_system(full_mmdict, skip_digestion=True)
    assert val is None


def test_get_solute_dielectric(full_mmdict):
    assert gma.get_solute_dielectric_from_system(full_mmdict, skip_digestion=True) == 1.0


def test_get_solvent_dielectric(full_mmdict):
    assert gma.get_solvent_dielectric_from_system(full_mmdict, skip_digestion=True) == 78.5


def test_get_salt_concentration(full_mmdict):
    assert gma.get_salt_concentration_from_system(full_mmdict, skip_digestion=True) is not None


def test_get_kappa(full_mmdict):
    assert gma.get_kappa_from_system(full_mmdict, skip_digestion=True) is None


# ---------------------------------------------------------------------------
# System getters return None when key is absent
# ---------------------------------------------------------------------------

def test_forcefield_none_when_missing(empty_mmdict):
    assert gma.get_forcefield_from_system(empty_mmdict, skip_digestion=True) is None


def test_non_bonded_method_none_when_missing(empty_mmdict):
    assert gma.get_non_bonded_method_from_system(empty_mmdict, skip_digestion=True) is None
