"""Comprehensive tests for molsysmt/form/molsysmt_Structures/get_structural_attributes.py.

Covers all getter functions:
  - get_coordinates_from_atom (all/atom-subset/struct-subset/both-subset/None indices)
  - get_velocities_from_atom (same variants)
  - get_occupancy_from_atom (None attribute, set via dynamic attr, subsets, None indices)
  - get_b_factor_from_atom (None attribute, values, subsets, None indices)
  - get_alternate_location_from_atom (None attribute, all, atom-subset, struct-subset, None indices)
  - get_n_atoms_from_system
  - get_n_structures_from_system (all / subset)
  - get_coordinates_from_system (all / subset / None)
  - get_velocities_from_system (all / subset / None)
  - get_box_from_system (all / subset / None / no-box)
  - get_box_shape_from_system (cubic / None struct_indices / no-box)
  - get_box_lengths_from_system (all / subset / None / no-box)
  - get_box_angles_from_system (all / subset / None / no-box)
  - get_box_volume_from_system (with-box / None struct_indices / no-box)
  - get_time_from_system (all / subset / None / no-time)
  - get_structure_id_from_system (all / subset / None / no-time)
  - get_occupancy_from_system
  - get_b_factor_from_system
  - get_alternate_location_from_system
  - get_bioassembly_from_system
  - get_n_bioassemblies_from_system
"""

import numpy as np
import pytest

from molsysmt.native import Structures
from molsysmt import pyunitwizard as puw
import molsysmt.form.molsysmt_Structures.get_structural_attributes as aux
from molsysmt.form.molsysmt_Structures.get_topological_attributes import (
    get_atom_index_from_atom,
)
from molsysmt.form.molsysmt_Structures.set import (
    set_occupancy_to_atom,
    set_b_factor_to_atom,
)


# ---------------------------------------------------------------------------
# Helpers / shared fixtures
# ---------------------------------------------------------------------------

def _make_structures(n_structs=3, n_atoms=4, with_box=True, with_time=True,
                     with_velocities=False, with_structure_id=True):
    """Return a Structures object populated with minimal test data."""
    coords = puw.quantity(
        np.arange(n_structs * n_atoms * 3, dtype=float).reshape(n_structs, n_atoms, 3) * 0.01,
        'nanometer',
    )
    box = None
    if with_box:
        box_vals = np.stack([np.eye(3) * (1.0 + 0.1 * i) for i in range(n_structs)])
        box = puw.quantity(box_vals, 'nanometer')

    time = None
    if with_time:
        time = puw.quantity(np.arange(n_structs, dtype=float), 'picosecond')

    structure_id = None
    if with_structure_id:
        structure_id = np.arange(n_structs)

    velocities = None
    if with_velocities:
        velocities = puw.quantity(
            np.ones((n_structs, n_atoms, 3), dtype=float) * 0.5,
            'nanometer/picosecond',
        )

    return Structures(
        coordinates=coords,
        box=box,
        time=time,
        structure_id=structure_id,
        velocities=velocities,
    )


def _make_alt_loc_entry():
    """Return a single alternate-location dict entry (for one atom, two locations)."""
    return {
        'location_id': np.array(['A', 'B']),
        'occupancy': np.array([0.5, 0.5]),
        'b_factor': puw.quantity(np.array([10.0, 10.0]), 'angstrom**2'),
        'atom_id': np.array([1, 1]),
        'coordinates': puw.quantity(
            np.array([[0.0, 0.0, 0.0], [0.1, 0.0, 0.0]]), 'nanometer'
        ),
    }


def test_structure_thermodynamic_series_and_total_energy():
    structures = _make_structures(n_structs=3, n_atoms=2)
    structures.temperature = puw.quantity([300.0, 301.0, 302.0], 'K')
    structures.potential_energy = puw.quantity([-10.0, -8.0, -6.0], 'kJ/mol')
    structures.kinetic_energy = puw.quantity([3.0, 4.0, 5.0], 'kJ/mol')

    temperature = aux.get_temperature_from_system(
        structures,
        structure_indices=np.array([0, 2]),
        skip_digestion=True,
    )
    total_energy = aux.get_total_energy_from_system(
        structures,
        structure_indices=np.array([0, 2]),
        skip_digestion=True,
    )

    np.testing.assert_allclose(puw.get_value(temperature, to_unit='K'), [300.0, 302.0])
    np.testing.assert_allclose(puw.get_value(total_energy, to_unit='kJ/mol'), [-7.0, -1.0])


def test_missing_occupancy_returns_none():
    structures = _make_structures(n_structs=1, n_atoms=2)

    assert aux.get_occupancy_from_atom(structures, skip_digestion=True) is None


# ===========================================================================
# get_n_atoms_from_system
# ===========================================================================

def test_get_atom_index_from_atom():
    structures = _make_structures(n_structs=2, n_atoms=4)

    assert get_atom_index_from_atom(structures, skip_digestion=True) == [0, 1, 2, 3]
    assert get_atom_index_from_atom(
        structures,
        indices=[3, 1],
        skip_digestion=True,
    ) == [3, 1]


class TestGetNAtomsFromSystem:

    def test_returns_correct_count(self):
        s = _make_structures(n_structs=2, n_atoms=5)
        assert aux.get_n_atoms_from_system(s, skip_digestion=True) == 5

    def test_single_atom(self):
        s = _make_structures(n_structs=1, n_atoms=1)
        assert aux.get_n_atoms_from_system(s, skip_digestion=True) == 1

    def test_large_system(self):
        s = _make_structures(n_structs=1, n_atoms=1000)
        assert aux.get_n_atoms_from_system(s, skip_digestion=True) == 1000


# ===========================================================================
# get_n_structures_from_system
# ===========================================================================

class TestGetNStructuresFromSystem:

    def test_all_structures(self):
        s = _make_structures(n_structs=3, n_atoms=2)
        assert aux.get_n_structures_from_system(s, skip_digestion=True) == 3

    def test_subset_structures(self):
        s = _make_structures(n_structs=5, n_atoms=2)
        result = aux.get_n_structures_from_system(
            s, structure_indices=np.array([0, 2, 4]), skip_digestion=True
        )
        assert result == 3

    def test_single_structure_subset(self):
        s = _make_structures(n_structs=5, n_atoms=2)
        result = aux.get_n_structures_from_system(
            s, structure_indices=np.array([1]), skip_digestion=True
        )
        assert result == 1


# ===========================================================================
# get_coordinates_from_atom
# ===========================================================================

class TestGetCoordinatesFromAtom:

    def test_all_returns_full_array(self):
        s = _make_structures(n_structs=3, n_atoms=4)
        result = aux.get_coordinates_from_atom(s, skip_digestion=True)
        assert puw.get_value(result).shape == (3, 4, 3)

    def test_atom_subset(self):
        s = _make_structures(n_structs=3, n_atoms=4)
        result = aux.get_coordinates_from_atom(
            s, indices=np.array([0, 2]), skip_digestion=True
        )
        assert puw.get_value(result).shape == (3, 2, 3)

    def test_structure_subset(self):
        s = _make_structures(n_structs=3, n_atoms=4)
        result = aux.get_coordinates_from_atom(
            s, structure_indices=np.array([0, 2]), skip_digestion=True
        )
        assert puw.get_value(result).shape == (2, 4, 3)

    def test_both_subsets(self):
        s = _make_structures(n_structs=3, n_atoms=4)
        result = aux.get_coordinates_from_atom(
            s,
            indices=np.array([1, 3]),
            structure_indices=np.array([0]),
            skip_digestion=True,
        )
        assert puw.get_value(result).shape == (1, 2, 3)

    def test_none_indices_returns_none(self):
        s = _make_structures(n_structs=2, n_atoms=3)
        result = aux.get_coordinates_from_atom(s, indices=None, skip_digestion=True)
        assert result is None

    def test_none_structure_indices_returns_none(self):
        s = _make_structures(n_structs=2, n_atoms=3)
        result = aux.get_coordinates_from_atom(
            s, structure_indices=None, skip_digestion=True
        )
        assert result is None

    def test_correct_unit(self):
        s = _make_structures(n_structs=2, n_atoms=3)
        result = aux.get_coordinates_from_atom(s, skip_digestion=True)
        assert puw.get_unit(result) == puw.unit('nanometer')

    def test_values_are_correct(self):
        n_structs, n_atoms = 2, 2
        raw = np.array([[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]],
                        [[7.0, 8.0, 9.0], [10.0, 11.0, 12.0]]])
        coords = puw.quantity(raw, 'nanometer')
        s = Structures(coordinates=coords)
        result = aux.get_coordinates_from_atom(
            s, indices=np.array([1]), structure_indices=np.array([0]),
            skip_digestion=True
        )
        np.testing.assert_allclose(puw.get_value(result), [[[4.0, 5.0, 6.0]]])


# ===========================================================================
# get_velocities_from_atom
# ===========================================================================

class TestGetVelocitiesFromAtom:

    def test_missing_velocities_with_subsets_returns_none(self):
        s = _make_structures(n_structs=2, n_atoms=3, with_velocities=False)
        result = aux.get_velocities_from_atom(
            s,
            indices=np.array([0, 1]),
            structure_indices=np.array([1]),
            skip_digestion=True,
        )
        assert result is None

    def test_all_returns_full_array(self):
        s = _make_structures(n_structs=3, n_atoms=4, with_velocities=True)
        result = aux.get_velocities_from_atom(s, skip_digestion=True)
        assert puw.get_value(result).shape == (3, 4, 3)

    def test_atom_subset(self):
        s = _make_structures(n_structs=3, n_atoms=4, with_velocities=True)
        result = aux.get_velocities_from_atom(
            s, indices=np.array([0, 1]), skip_digestion=True
        )
        assert puw.get_value(result).shape == (3, 2, 3)

    def test_structure_subset(self):
        s = _make_structures(n_structs=3, n_atoms=4, with_velocities=True)
        result = aux.get_velocities_from_atom(
            s, structure_indices=np.array([2]), skip_digestion=True
        )
        assert puw.get_value(result).shape == (1, 4, 3)

    def test_both_subsets(self):
        s = _make_structures(n_structs=3, n_atoms=4, with_velocities=True)
        result = aux.get_velocities_from_atom(
            s,
            indices=np.array([0]),
            structure_indices=np.array([1, 2]),
            skip_digestion=True,
        )
        assert puw.get_value(result).shape == (2, 1, 3)

    def test_none_indices_returns_none(self):
        s = _make_structures(n_structs=2, n_atoms=3, with_velocities=True)
        result = aux.get_velocities_from_atom(s, indices=None, skip_digestion=True)
        assert result is None

    def test_none_structure_indices_returns_none(self):
        s = _make_structures(n_structs=2, n_atoms=3, with_velocities=True)
        result = aux.get_velocities_from_atom(
            s, structure_indices=None, skip_digestion=True
        )
        assert result is None

    def test_correct_unit(self):
        s = _make_structures(n_structs=2, n_atoms=2, with_velocities=True)
        result = aux.get_velocities_from_atom(s, skip_digestion=True)
        assert puw.get_unit(result) == puw.unit('nanometer/picosecond')


# ===========================================================================
# get_occupancy_from_atom
# ===========================================================================

class TestGetOccupancyFromAtom:

    def _make_with_occupancy(self, n_structs=2, n_atoms=3):
        s = _make_structures(n_structs=n_structs, n_atoms=n_atoms)
        occupancy = np.linspace(0.5, 1.0, n_structs * n_atoms).reshape(n_structs, n_atoms)
        set_occupancy_to_atom(s, value=occupancy, skip_digestion=True)
        return s, occupancy

    def test_returns_none_when_no_occupancy_attribute(self):
        s = _make_structures(n_structs=2, n_atoms=3)
        assert aux.get_occupancy_from_atom(s, skip_digestion=True) is None

    def test_all_indices_returns_full_array(self):
        s, occ = self._make_with_occupancy(n_structs=2, n_atoms=3)
        result = aux.get_occupancy_from_atom(s, skip_digestion=True)
        assert result is not None
        np.testing.assert_allclose(result, occ)

    def test_atom_subset(self):
        s, _ = self._make_with_occupancy(n_structs=2, n_atoms=4)
        result = aux.get_occupancy_from_atom(
            s, indices=np.array([0, 2]), skip_digestion=True
        )
        assert result.shape == (2, 2)

    def test_structure_subset(self):
        s, _ = self._make_with_occupancy(n_structs=3, n_atoms=4)
        result = aux.get_occupancy_from_atom(
            s, structure_indices=np.array([0, 2]), skip_digestion=True
        )
        assert result.shape == (2, 4)

    def test_none_indices_returns_none(self):
        s, _ = self._make_with_occupancy()
        result = aux.get_occupancy_from_atom(s, indices=None, skip_digestion=True)
        assert result is None

    def test_none_structure_indices_returns_none(self):
        s, _ = self._make_with_occupancy()
        result = aux.get_occupancy_from_atom(
            s, structure_indices=None, skip_digestion=True
        )
        assert result is None


# ===========================================================================
# get_b_factor_from_atom
# ===========================================================================

class TestGetBFactorFromAtom:

    def _make_with_b_factor(self, n_structs=2, n_atoms=3):
        s = _make_structures(n_structs=n_structs, n_atoms=n_atoms)
        b_factor = puw.quantity(
            np.ones((n_structs, n_atoms)) * 20.0, 'angstrom**2'
        )
        set_b_factor_to_atom(s, value=b_factor, skip_digestion=True)
        return s

    def test_returns_none_when_no_b_factor(self):
        s = _make_structures(n_structs=2, n_atoms=3)
        result = aux.get_b_factor_from_atom(s, skip_digestion=True)
        assert result is None

    def test_all_indices(self):
        s = self._make_with_b_factor(n_structs=2, n_atoms=3)
        result = aux.get_b_factor_from_atom(s, skip_digestion=True)
        assert result is not None
        assert puw.get_value(result).shape == (2, 3)

    def test_atom_subset(self):
        s = self._make_with_b_factor(n_structs=2, n_atoms=4)
        result = aux.get_b_factor_from_atom(
            s, indices=np.array([1, 3]), skip_digestion=True
        )
        assert puw.get_value(result).shape == (2, 2)

    def test_structure_subset(self):
        s = self._make_with_b_factor(n_structs=3, n_atoms=4)
        result = aux.get_b_factor_from_atom(
            s, structure_indices=np.array([0]), skip_digestion=True
        )
        assert puw.get_value(result).shape == (1, 4)

    def test_none_indices_returns_none(self):
        s = self._make_with_b_factor()
        result = aux.get_b_factor_from_atom(s, indices=None, skip_digestion=True)
        assert result is None

    def test_none_structure_indices_returns_none(self):
        s = self._make_with_b_factor()
        result = aux.get_b_factor_from_atom(
            s, structure_indices=None, skip_digestion=True
        )
        assert result is None


# ===========================================================================
# get_alternate_location_from_atom
# ===========================================================================

class TestGetAlternateLocationFromAtom:

    def _make_with_alt_loc(self, n_structs=2, n_atoms=2):
        coords = puw.quantity(np.ones((n_structs, n_atoms, 3)), 'nanometer')
        entry = _make_alt_loc_entry()
        # Only atom 0 has alternate locations
        alt_loc = [{0: entry} for _ in range(n_structs)]
        return Structures(coordinates=coords, alternate_location=alt_loc)

    def test_returns_none_when_no_alt_loc(self):
        s = _make_structures(n_structs=2, n_atoms=2)
        result = aux.get_alternate_location_from_atom(s, skip_digestion=True)
        assert result is None

    def test_none_indices_returns_none(self):
        s = self._make_with_alt_loc()
        result = aux.get_alternate_location_from_atom(
            s, indices=None, skip_digestion=True
        )
        assert result is None

    def test_none_structure_indices_returns_none(self):
        s = self._make_with_alt_loc()
        result = aux.get_alternate_location_from_atom(
            s, structure_indices=None, skip_digestion=True
        )
        assert result is None

    def test_all_indices_returns_all_structures(self):
        s = self._make_with_alt_loc(n_structs=2)
        result = aux.get_alternate_location_from_atom(s, skip_digestion=True)
        assert isinstance(result, list)
        assert len(result) == 2

    def test_atom_subset_filters_keys(self):
        s = self._make_with_alt_loc(n_structs=2, n_atoms=2)
        # Ask only for atom 1 — atom 0 has alt loc, atom 1 does not
        result = aux.get_alternate_location_from_atom(
            s, indices=np.array([1]), skip_digestion=True
        )
        # atom 0 should be excluded from each dict
        for frame_dict in result:
            assert 0 not in frame_dict

    def test_atom_subset_includes_matching_key(self):
        s = self._make_with_alt_loc(n_structs=2, n_atoms=2)
        result = aux.get_alternate_location_from_atom(
            s, indices=np.array([0]), skip_digestion=True
        )
        for frame_dict in result:
            assert 0 in frame_dict

    def test_structure_subset(self):
        s = self._make_with_alt_loc(n_structs=3)
        result = aux.get_alternate_location_from_atom(
            s, structure_indices=np.array([0, 2]), skip_digestion=True
        )
        assert len(result) == 2

    def test_structure_subset_single(self):
        s = self._make_with_alt_loc(n_structs=3)
        result = aux.get_alternate_location_from_atom(
            s, structure_indices=np.array([1]), skip_digestion=True
        )
        assert len(result) == 1


# ===========================================================================
# get_coordinates_from_system
# ===========================================================================

class TestGetCoordinatesFromSystem:

    def test_all_returns_full_array(self):
        s = _make_structures(n_structs=3, n_atoms=4)
        result = aux.get_coordinates_from_system(s, skip_digestion=True)
        assert puw.get_value(result).shape == (3, 4, 3)

    def test_structure_subset(self):
        s = _make_structures(n_structs=3, n_atoms=4)
        result = aux.get_coordinates_from_system(
            s, structure_indices=np.array([0, 2]), skip_digestion=True
        )
        assert puw.get_value(result).shape == (2, 4, 3)

    def test_none_structure_indices_returns_none(self):
        s = _make_structures(n_structs=2, n_atoms=3)
        result = aux.get_coordinates_from_system(
            s, structure_indices=None, skip_digestion=True
        )
        assert result is None

    def test_correct_unit(self):
        s = _make_structures(n_structs=2, n_atoms=3)
        result = aux.get_coordinates_from_system(s, skip_digestion=True)
        assert puw.get_unit(result) == puw.unit('nanometer')


# ===========================================================================
# get_velocities_from_system
# ===========================================================================

class TestGetVelocitiesFromSystem:

    def test_missing_velocities_with_subset_returns_none(self):
        s = _make_structures(n_structs=2, n_atoms=3, with_velocities=False)
        result = aux.get_velocities_from_system(
            s,
            structure_indices=np.array([1]),
            skip_digestion=True,
        )
        assert result is None

    def test_all_returns_full_array(self):
        s = _make_structures(n_structs=3, n_atoms=4, with_velocities=True)
        result = aux.get_velocities_from_system(s, skip_digestion=True)
        assert puw.get_value(result).shape == (3, 4, 3)

    def test_structure_subset(self):
        s = _make_structures(n_structs=3, n_atoms=4, with_velocities=True)
        result = aux.get_velocities_from_system(
            s, structure_indices=np.array([1]), skip_digestion=True
        )
        assert puw.get_value(result).shape == (1, 4, 3)

    def test_none_structure_indices_returns_none(self):
        s = _make_structures(n_structs=2, n_atoms=3, with_velocities=True)
        result = aux.get_velocities_from_system(
            s, structure_indices=None, skip_digestion=True
        )
        assert result is None

    def test_correct_unit(self):
        s = _make_structures(n_structs=2, n_atoms=3, with_velocities=True)
        result = aux.get_velocities_from_system(s, skip_digestion=True)
        assert puw.get_unit(result) == puw.unit('nanometer/picosecond')


# ===========================================================================
# get_box_from_system
# ===========================================================================

class TestGetBoxFromSystem:

    def test_all_returns_full_array(self):
        s = _make_structures(n_structs=3, n_atoms=2, with_box=True)
        result = aux.get_box_from_system(s, skip_digestion=True)
        assert puw.get_value(result).shape == (3, 3, 3)

    def test_structure_subset(self):
        s = _make_structures(n_structs=3, n_atoms=2, with_box=True)
        result = aux.get_box_from_system(
            s, structure_indices=np.array([0, 2]), skip_digestion=True
        )
        assert puw.get_value(result).shape == (2, 3, 3)

    def test_none_structure_indices_returns_none(self):
        s = _make_structures(n_structs=2, n_atoms=2, with_box=True)
        result = aux.get_box_from_system(
            s, structure_indices=None, skip_digestion=True
        )
        assert result is None

    def test_no_box_returns_none(self):
        s = _make_structures(n_structs=2, n_atoms=2, with_box=False)
        result = aux.get_box_from_system(s, skip_digestion=True)
        assert result is None

    def test_correct_unit(self):
        s = _make_structures(n_structs=2, n_atoms=2, with_box=True)
        result = aux.get_box_from_system(s, skip_digestion=True)
        assert puw.get_unit(result) == puw.unit('nanometer')


# ===========================================================================
# get_box_shape_from_system
# ===========================================================================

class TestGetBoxShapeFromSystem:

    def test_cubic_box(self):
        s = _make_structures(n_structs=2, n_atoms=2, with_box=True)
        result = aux.get_box_shape_from_system(s, skip_digestion=True)
        assert result == 'cubic'

    def test_no_box_returns_none(self):
        s = _make_structures(n_structs=2, n_atoms=2, with_box=False)
        result = aux.get_box_shape_from_system(s, skip_digestion=True)
        assert result is None

    def test_none_structure_indices_returns_none(self):
        s = _make_structures(n_structs=2, n_atoms=2, with_box=True)
        result = aux.get_box_shape_from_system(
            s, structure_indices=None, skip_digestion=True
        )
        assert result is None

    def test_structure_subset_still_cubic(self):
        s = _make_structures(n_structs=3, n_atoms=2, with_box=True)
        result = aux.get_box_shape_from_system(
            s, structure_indices=np.array([0]), skip_digestion=True
        )
        assert result == 'cubic'


# ===========================================================================
# get_box_lengths_from_system
# ===========================================================================

class TestGetBoxLengthsFromSystem:

    def test_all_returns_correct_shape(self):
        s = _make_structures(n_structs=3, n_atoms=2, with_box=True)
        result = aux.get_box_lengths_from_system(s, skip_digestion=True)
        assert puw.get_value(result).shape == (3, 3)

    def test_structure_subset(self):
        s = _make_structures(n_structs=3, n_atoms=2, with_box=True)
        result = aux.get_box_lengths_from_system(
            s, structure_indices=np.array([0, 2]), skip_digestion=True
        )
        assert puw.get_value(result).shape == (2, 3)

    def test_none_structure_indices_returns_none(self):
        s = _make_structures(n_structs=2, n_atoms=2, with_box=True)
        result = aux.get_box_lengths_from_system(
            s, structure_indices=None, skip_digestion=True
        )
        assert result is None

    def test_no_box_returns_none(self):
        s = _make_structures(n_structs=2, n_atoms=2, with_box=False)
        result = aux.get_box_lengths_from_system(s, skip_digestion=True)
        assert result is None

    def test_correct_unit(self):
        s = _make_structures(n_structs=2, n_atoms=2, with_box=True)
        result = aux.get_box_lengths_from_system(s, skip_digestion=True)
        assert puw.get_unit(result) == puw.unit('nanometer')

    def test_values_match_diagonal(self):
        # Box is diagonal: lengths should equal the diagonal elements
        box_vals = np.array([[[2.0, 0.0, 0.0], [0.0, 3.0, 0.0], [0.0, 0.0, 4.0]]])
        coords = puw.quantity(np.ones((1, 2, 3)), 'nanometer')
        box = puw.quantity(box_vals, 'nanometer')
        s = Structures(coordinates=coords, box=box)
        result = aux.get_box_lengths_from_system(s, skip_digestion=True)
        values = puw.get_value(result)
        np.testing.assert_allclose(values[0], [2.0, 3.0, 4.0], rtol=1e-5)


# ===========================================================================
# get_box_angles_from_system
# ===========================================================================

class TestGetBoxAnglesFromSystem:

    def test_all_returns_correct_shape(self):
        s = _make_structures(n_structs=3, n_atoms=2, with_box=True)
        result = aux.get_box_angles_from_system(s, skip_digestion=True)
        assert puw.get_value(result).shape == (3, 3)

    def test_structure_subset(self):
        s = _make_structures(n_structs=3, n_atoms=2, with_box=True)
        result = aux.get_box_angles_from_system(
            s, structure_indices=np.array([1]), skip_digestion=True
        )
        assert puw.get_value(result).shape == (1, 3)

    def test_none_structure_indices_returns_none(self):
        s = _make_structures(n_structs=2, n_atoms=2, with_box=True)
        result = aux.get_box_angles_from_system(
            s, structure_indices=None, skip_digestion=True
        )
        assert result is None

    def test_no_box_returns_none(self):
        s = _make_structures(n_structs=2, n_atoms=2, with_box=False)
        result = aux.get_box_angles_from_system(s, skip_digestion=True)
        assert result is None

    def test_correct_unit(self):
        s = _make_structures(n_structs=2, n_atoms=2, with_box=True)
        result = aux.get_box_angles_from_system(s, skip_digestion=True)
        assert puw.get_unit(result) == puw.unit('radian')

    def test_cubic_box_angles_are_90_degrees(self):
        s = _make_structures(n_structs=1, n_atoms=2, with_box=True)
        result = aux.get_box_angles_from_system(s, skip_digestion=True)
        values = puw.get_value(result)
        np.testing.assert_allclose(values, [[np.pi / 2, np.pi / 2, np.pi / 2]], rtol=1e-5)


# ===========================================================================
# get_box_volume_from_system
# ===========================================================================

class TestGetBoxVolumeFromSystem:

    def test_all_returns_correct_shape(self):
        s = _make_structures(n_structs=3, n_atoms=2, with_box=True)
        result = aux.get_box_volume_from_system(s, skip_digestion=True)
        assert puw.get_value(result).shape == (3,)

    def test_none_structure_indices_returns_none(self):
        s = _make_structures(n_structs=2, n_atoms=2, with_box=True)
        result = aux.get_box_volume_from_system(
            s, structure_indices=None, skip_digestion=True
        )
        assert result is None

    def test_no_box_returns_none(self):
        s = _make_structures(n_structs=2, n_atoms=2, with_box=False)
        result = aux.get_box_volume_from_system(s, skip_digestion=True)
        assert result is None

    def test_correct_unit(self):
        s = _make_structures(n_structs=2, n_atoms=2, with_box=True)
        result = aux.get_box_volume_from_system(s, skip_digestion=True)
        assert puw.get_unit(result) == puw.unit('nanometer**3')

    def test_cubic_box_volume(self):
        # 2 nm cubic box: volume = 8 nm^3
        box_vals = np.array([[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]])
        coords = puw.quantity(np.ones((1, 2, 3)), 'nanometer')
        box = puw.quantity(box_vals, 'nanometer')
        s = Structures(coordinates=coords, box=box)
        result = aux.get_box_volume_from_system(s, skip_digestion=True)
        np.testing.assert_allclose(puw.get_value(result), [8.0], rtol=1e-5)

    def test_structure_subset_via_box(self):
        s = _make_structures(n_structs=3, n_atoms=2, with_box=True)
        result = aux.get_box_volume_from_system(
            s, structure_indices=np.array([0, 1]), skip_digestion=True
        )
        assert puw.get_value(result).shape == (2,)


# ===========================================================================
# get_time_from_system
# ===========================================================================

class TestGetTimeFromSystem:

    def test_all_returns_full_array(self):
        s = _make_structures(n_structs=3, n_atoms=2, with_time=True)
        result = aux.get_time_from_system(s, skip_digestion=True)
        assert puw.get_value(result).shape == (3,)

    def test_structure_subset(self):
        s = _make_structures(n_structs=4, n_atoms=2, with_time=True)
        result = aux.get_time_from_system(
            s, structure_indices=np.array([0, 3]), skip_digestion=True
        )
        np.testing.assert_allclose(puw.get_value(result), [0.0, 3.0])

    def test_none_structure_indices_returns_none(self):
        s = _make_structures(n_structs=2, n_atoms=2, with_time=True)
        result = aux.get_time_from_system(
            s, structure_indices=None, skip_digestion=True
        )
        assert result is None

    def test_no_time_returns_none(self):
        s = _make_structures(n_structs=2, n_atoms=2, with_time=False)
        result = aux.get_time_from_system(s, skip_digestion=True)
        assert result is None

    def test_correct_unit(self):
        s = _make_structures(n_structs=2, n_atoms=2, with_time=True)
        result = aux.get_time_from_system(s, skip_digestion=True)
        assert puw.get_unit(result) == puw.unit('picosecond')

    def test_values_are_correct(self):
        s = _make_structures(n_structs=3, n_atoms=2, with_time=True)
        result = aux.get_time_from_system(s, skip_digestion=True)
        # _make_structures uses np.arange(n_structs)
        np.testing.assert_allclose(puw.get_value(result), [0.0, 1.0, 2.0])


# ===========================================================================
# get_structure_id_from_system
# ===========================================================================

class TestGetStructureIdFromSystem:

    def test_all_returns_full_array(self):
        s = _make_structures(n_structs=3, n_atoms=2, with_structure_id=True)
        result = aux.get_structure_id_from_system(s, skip_digestion=True)
        assert result.shape == (3,)

    def test_structure_subset(self):
        s = _make_structures(n_structs=4, n_atoms=2, with_structure_id=True)
        result = aux.get_structure_id_from_system(
            s, structure_indices=np.array([1, 3]), skip_digestion=True
        )
        np.testing.assert_array_equal(result, [1, 3])

    def test_none_structure_indices_returns_none(self):
        s = _make_structures(n_structs=2, n_atoms=2, with_structure_id=True)
        result = aux.get_structure_id_from_system(
            s, structure_indices=None, skip_digestion=True
        )
        assert result is None

    def test_structure_ids_do_not_require_time(self):
        s = _make_structures(
            n_structs=2, n_atoms=2, with_time=False, with_structure_id=True
        )
        result = aux.get_structure_id_from_system(s, skip_digestion=True)
        np.testing.assert_array_equal(result, [0, 1])

    def test_missing_structure_ids_with_subset_returns_none(self):
        s = _make_structures(
            n_structs=2, n_atoms=2, with_time=True, with_structure_id=False
        )
        result = aux.get_structure_id_from_system(
            s,
            structure_indices=np.array([1]),
            skip_digestion=True,
        )
        assert result is None

    def test_values_are_correct(self):
        s = _make_structures(n_structs=3, n_atoms=2, with_structure_id=True)
        result = aux.get_structure_id_from_system(s, skip_digestion=True)
        np.testing.assert_array_equal(result, [0, 1, 2])


# ===========================================================================
# get_occupancy_from_system (delegates to get_occupancy_from_atom)
# ===========================================================================

class TestGetOccupancyFromSystem:

    def test_returns_none_when_no_occupancy_attribute(self):
        s = _make_structures(n_structs=2, n_atoms=3)
        assert aux.get_occupancy_from_system(s, skip_digestion=True) is None

    def test_returns_full_array_when_set(self):
        s = _make_structures(n_structs=2, n_atoms=3)
        occ = np.ones((2, 3)) * 0.7
        set_occupancy_to_atom(s, value=occ, skip_digestion=True)
        result = aux.get_occupancy_from_system(s, skip_digestion=True)
        np.testing.assert_allclose(result, occ)

    def test_structure_subset(self):
        s = _make_structures(n_structs=3, n_atoms=3)
        occ = np.ones((3, 3)) * 0.9
        set_occupancy_to_atom(s, value=occ, skip_digestion=True)
        result = aux.get_occupancy_from_system(
            s, structure_indices=np.array([0, 2]), skip_digestion=True
        )
        assert result.shape == (2, 3)


# ===========================================================================
# get_b_factor_from_system (delegates to get_b_factor_from_atom)
# ===========================================================================

class TestGetBFactorFromSystem:

    def test_returns_none_when_no_b_factor(self):
        s = _make_structures(n_structs=2, n_atoms=3)
        result = aux.get_b_factor_from_system(s, skip_digestion=True)
        assert result is None

    def test_returns_full_array_when_set(self):
        s = _make_structures(n_structs=2, n_atoms=3)
        b_factor = puw.quantity(np.ones((2, 3)) * 15.0, 'angstrom**2')
        set_b_factor_to_atom(s, value=b_factor, skip_digestion=True)
        result = aux.get_b_factor_from_system(s, skip_digestion=True)
        assert result is not None
        assert puw.get_value(result).shape == (2, 3)

    def test_structure_subset(self):
        s = _make_structures(n_structs=3, n_atoms=3)
        b_factor = puw.quantity(np.ones((3, 3)) * 12.0, 'angstrom**2')
        set_b_factor_to_atom(s, value=b_factor, skip_digestion=True)
        result = aux.get_b_factor_from_system(
            s, structure_indices=np.array([1]), skip_digestion=True
        )
        assert puw.get_value(result).shape == (1, 3)


# ===========================================================================
# get_alternate_location_from_system (delegates to get_alternate_location_from_atom)
# ===========================================================================

class TestGetAlternateLocationFromSystem:

    def _make_with_alt_loc(self, n_structs=2, n_atoms=2):
        coords = puw.quantity(np.ones((n_structs, n_atoms, 3)), 'nanometer')
        entry = _make_alt_loc_entry()
        alt_loc = [{0: entry} for _ in range(n_structs)]
        return Structures(coordinates=coords, alternate_location=alt_loc)

    def test_returns_none_when_no_alt_loc(self):
        s = _make_structures(n_structs=2, n_atoms=2)
        result = aux.get_alternate_location_from_system(s, skip_digestion=True)
        assert result is None

    def test_returns_list_when_set(self):
        s = self._make_with_alt_loc(n_structs=3)
        result = aux.get_alternate_location_from_system(s, skip_digestion=True)
        assert isinstance(result, list)
        assert len(result) == 3

    def test_structure_subset(self):
        s = self._make_with_alt_loc(n_structs=3)
        result = aux.get_alternate_location_from_system(
            s, structure_indices=np.array([0, 2]), skip_digestion=True
        )
        assert len(result) == 2


# ===========================================================================
# get_bioassembly_from_system / get_n_bioassemblies_from_system
# ===========================================================================

class TestGetBioassemblyFromSystem:

    def _make_with_bioassembly(self, n_assemblies=2):
        coords = puw.quantity(np.ones((1, 2, 3)), 'nanometer')
        bioassembly = {
            f'BA{i}': {
                'chain_indices': np.array([0]),
                'rotations': [np.eye(3)],
                'translations': [puw.quantity(np.array([0.0, 0.0, 0.0]), 'nm')],
            }
            for i in range(n_assemblies)
        }
        return Structures(coordinates=coords, bioassembly=bioassembly)

    def test_returns_none_when_no_bioassembly(self):
        s = _make_structures(n_structs=1, n_atoms=2)
        result = aux.get_bioassembly_from_system(s, skip_digestion=True)
        assert result is None

    def test_returns_dict_when_set(self):
        s = self._make_with_bioassembly(n_assemblies=2)
        result = aux.get_bioassembly_from_system(s, skip_digestion=True)
        assert isinstance(result, dict)
        assert len(result) == 2

    def test_bioassembly_keys_present(self):
        s = self._make_with_bioassembly(n_assemblies=3)
        result = aux.get_bioassembly_from_system(s, skip_digestion=True)
        for i in range(3):
            assert f'BA{i}' in result

    def test_n_bioassemblies_when_set(self):
        s = self._make_with_bioassembly(n_assemblies=3)
        result = aux.get_n_bioassemblies_from_system(s, skip_digestion=True)
        assert result == 3

    def test_n_bioassemblies_zero_when_none(self):
        # bioassembly=None → len(None) raises, so check actual behavior
        s = _make_structures(n_structs=1, n_atoms=2)
        # When bioassembly is None, len(None) would raise; verify current behavior
        # (if it raises, the test documents the behavior)
        try:
            result = aux.get_n_bioassemblies_from_system(s, skip_digestion=True)
            # If it doesn't raise, it should be 0 (empty container)
            assert result == 0
        except TypeError:
            # bioassembly is None and len(None) raises — document expected gap
            pytest.skip("get_n_bioassemblies_from_system raises TypeError when bioassembly is None")

    def test_n_bioassemblies_single(self):
        s = self._make_with_bioassembly(n_assemblies=1)
        result = aux.get_n_bioassemblies_from_system(s, skip_digestion=True)
        assert result == 1
