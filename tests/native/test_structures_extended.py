"""
Extended tests for molsysmt.native.Structures covering uncovered properties and methods.
"""
import warnings

import numpy as np
import pytest
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import (
    ArgumentLengthError,
    StructuralAttributeDropWarning,
)
from molsysmt.native import Structures


def _coords(n_structures=1, n_atoms=5):
    val = np.random.rand(n_structures, n_atoms, 3).astype(np.float64)
    return puw.quantity(val, 'nm')


def _velocity(n_structures=1, n_atoms=5):
    val = np.random.rand(n_structures, n_atoms, 3).astype(np.float64)
    return puw.quantity(val, 'nm/ps')


def _box(n_structures=1):
    val = np.eye(3)[np.newaxis, :, :].repeat(n_structures, axis=0) * 3.0
    return puw.quantity(val, 'nm')


def _time(n_structures=1):
    val = np.arange(n_structures, dtype=np.float64)
    return puw.quantity(val, 'ps')


def _b_factor(n_structures=1, n_atoms=5):
    val = np.arange(n_structures * n_atoms, dtype=np.float64).reshape(n_structures, n_atoms)
    return puw.quantity(val, 'nm**2')


def _energy(n_structures=1):
    val = np.arange(n_structures, dtype=np.float64)
    return puw.quantity(val, 'kcal/mol')


# ---------------------------------------------------------------------------
# n_structures property
# ---------------------------------------------------------------------------

def test_n_structures_from_velocities():
    """n_structures falls back to velocities when coordinates is None."""
    s = Structures()
    s.velocities = _velocity(n_structures=3)
    assert s.n_structures == 3


def test_n_structures_from_box():
    """n_structures falls back to box when both coordinates and velocities are None."""
    s = Structures()
    s.box = _box(n_structures=2)
    assert s.n_structures == 2


def test_n_structures_empty():
    """n_structures is 0 when everything is None."""
    s = Structures()
    assert s.n_structures == 0


# ---------------------------------------------------------------------------
# n_atoms property
# ---------------------------------------------------------------------------

def test_n_atoms_from_velocities():
    """n_atoms falls back to velocities when coordinates is None."""
    s = Structures()
    s.velocities = _velocity(n_structures=1, n_atoms=7)
    assert s.n_atoms == 7


def test_n_atoms_empty():
    """n_atoms is 0 when both coordinates and velocities are None."""
    s = Structures()
    assert s.n_atoms == 0


# ---------------------------------------------------------------------------
# append — argument length errors
# ---------------------------------------------------------------------------

def test_append_time_length_mismatch():
    """Mismatched time length raises ArgumentLengthError."""
    s = Structures()
    coords = _coords(n_structures=2)
    time_wrong = _time(n_structures=3)
    with pytest.raises(ArgumentLengthError):
        s.append(coordinates=coords, time=time_wrong)


def test_append_coordinates_frame_mismatch():
    """Mismatched coordinate frame count raises ArgumentLengthError."""
    s = Structures()
    time = _time(n_structures=2)
    coords_wrong = _coords(n_structures=3)
    with pytest.raises(ArgumentLengthError):
        s.append(time=time, coordinates=coords_wrong)


def test_append_coordinates_atom_mismatch():
    """Appending coordinates with wrong atom count raises ArgumentLengthError."""
    s = Structures()
    s.coordinates = _coords(n_structures=1, n_atoms=5)
    coords_wrong = _coords(n_structures=1, n_atoms=7)
    with pytest.raises(ArgumentLengthError):
        s.append(coordinates=coords_wrong)


def test_append_box_frame_mismatch():
    """Mismatched box frame count raises ArgumentLengthError."""
    s = Structures()
    coords = _coords(n_structures=2)
    box_wrong = _box(n_structures=3)
    with pytest.raises(ArgumentLengthError):
        s.append(coordinates=coords, box=box_wrong)


# ---------------------------------------------------------------------------
# append — accumulation (already-existing attributes)
# ---------------------------------------------------------------------------

def test_append_accumulates_time():
    """Appending time+coordinates when they already exist concatenates correctly."""
    s = Structures()
    t1 = _time(n_structures=2)
    c1 = _coords(n_structures=2, n_atoms=4)
    t2 = _time(n_structures=3)
    c2 = _coords(n_structures=3, n_atoms=4)
    s.append(time=t1, coordinates=c1)
    s.append(time=t2, coordinates=c2)
    assert s.n_structures == 5


def test_append_accumulates_coordinates():
    """Appending coordinates when coordinates already exist concatenates correctly."""
    s = Structures()
    c1 = _coords(n_structures=2, n_atoms=4)
    c2 = _coords(n_structures=3, n_atoms=4)
    s.append(coordinates=c1)
    s.append(coordinates=c2)
    assert s.n_structures == 5
    assert s.n_atoms == 4


def test_append_velocities():
    """Appending coordinates+velocities to empty Structures stores both."""
    s = Structures()
    c = _coords(n_structures=2, n_atoms=4)
    v = _velocity(n_structures=2, n_atoms=4)
    s.append(coordinates=c, velocities=v)
    assert s.velocities is not None
    assert s.n_structures == 2


def test_append_box():
    """Appending box to empty Structures stores it."""
    s = Structures()
    b = _box(n_structures=2)
    s.append(box=b)
    assert s.box is not None


def test_append_none_does_nothing():
    """Calling append with all None is a no-op."""
    s = Structures()
    s.append()
    assert s.n_structures == 0


def test_append_structures_accepts_missing_optional_occupancy():
    """Append coordinate frames when neither source declares occupancy."""

    target = Structures(coordinates=_coords(n_structures=1, n_atoms=4))
    source = Structures(coordinates=_coords(n_structures=2, n_atoms=4))

    assert target.occupancy is None
    assert source.occupancy is None

    target.append_structures(source)

    assert target.n_structures == 3
    assert target.occupancy is None


# ---------------------------------------------------------------------------
# extract with specific indices
# ---------------------------------------------------------------------------

def test_extract_specific_structure_indices():
    """extract with specific structure_indices returns subset."""
    s = Structures()
    s.coordinates = _coords(n_structures=5, n_atoms=4)
    sub = s.extract(structure_indices=[0, 2, 4])
    assert sub.n_structures == 3
    assert sub.n_atoms == 4


def test_extract_specific_atom_indices():
    """extract with specific atom_indices returns subset."""
    s = Structures()
    s.coordinates = _coords(n_structures=2, n_atoms=6)
    sub = s.extract(atom_indices=[0, 1, 2])
    assert sub.n_atoms == 3


def test_extract_both_indices():
    """extract with both structure and atom indices returns correct shape."""
    s = Structures()
    s.coordinates = _coords(n_structures=4, n_atoms=6)
    sub = s.extract(structure_indices=[1, 3], atom_indices=[0, 2, 4])
    assert sub.n_structures == 2
    assert sub.n_atoms == 3


def test_extract_copy_if_all_false():
    """extract with all indices and copy_if_all=False returns self."""
    s = Structures()
    s.coordinates = _coords(n_structures=2, n_atoms=3)
    result = s.extract(copy_if_all=False)
    assert result is s


def test_extract_preserves_b_factor_with_structure_subset():
    """extract preserves b_factor when selecting a subset of structures."""
    s = Structures()
    s.coordinates = _coords(n_structures=3, n_atoms=4)
    s.b_factor = _b_factor(n_structures=3, n_atoms=4)

    sub = s.extract(structure_indices=[1])

    assert sub.b_factor is not None
    np.testing.assert_allclose(
        puw.get_value(sub.b_factor, to_unit='nm**2'),
        puw.get_value(s.b_factor[[1], :], to_unit='nm**2'),
    )


def test_extract_preserves_atomwise_and_structurewise_metadata():
    """extract preserves velocities, b_factor, and per-structure metadata."""
    s = Structures()
    s.structure_id = np.array(['a', 'b', 'c'], dtype=object)
    s.time = _time(n_structures=3)
    s.coordinates = _coords(n_structures=3, n_atoms=5)
    s.velocities = _velocity(n_structures=3, n_atoms=5)
    s.box = _box(n_structures=3)
    s.b_factor = _b_factor(n_structures=3, n_atoms=5)
    s.alternate_location = np.array(['A', 'B', 'C'], dtype=object)
    s.temperature = puw.quantity(np.array([300.0, 301.0, 302.0]), 'K')
    s.potential_energy = _energy(n_structures=3)
    s.kinetic_energy = _energy(n_structures=3) + _energy(n_structures=3)
    s.bioassembly = {'assembly': 1}

    sub = s.extract(structure_indices=[0, 2], atom_indices=[1, 3])

    assert sub.structure_id.tolist() == ['a', 'c']
    assert sub.alternate_location.tolist() == ['A', 'C']
    assert sub.bioassembly == s.bioassembly
    assert puw.get_value(sub.time, to_unit='ps').tolist() == [0.0, 2.0]
    np.testing.assert_allclose(
        puw.get_value(sub.coordinates, to_unit='nm'),
        puw.get_value(s.coordinates[np.ix_([0, 2], [1, 3], [0, 1, 2])], to_unit='nm'),
    )
    np.testing.assert_allclose(
        puw.get_value(sub.velocities, to_unit='nm/ps'),
        puw.get_value(s.velocities[np.ix_([0, 2], [1, 3], [0, 1, 2])], to_unit='nm/ps'),
    )
    np.testing.assert_allclose(
        puw.get_value(sub.box, to_unit='nm'),
        puw.get_value(s.box[[0, 2], :, :], to_unit='nm'),
    )
    np.testing.assert_allclose(
        puw.get_value(sub.b_factor, to_unit='nm**2'),
        puw.get_value(s.b_factor[np.ix_([0, 2], [1, 3])], to_unit='nm**2'),
    )
    np.testing.assert_allclose(
        puw.get_value(sub.temperature, to_unit='K'),
        [300.0, 302.0],
    )
    np.testing.assert_allclose(
        puw.get_value(sub.potential_energy, to_unit='kcal/mol'),
        [0.0, 2.0],
    )
    np.testing.assert_allclose(
        puw.get_value(sub.kinetic_energy, to_unit='kcal/mol'),
        [0.0, 4.0],
    )


# ---------------------------------------------------------------------------
# add — atom-axis alignment
# ---------------------------------------------------------------------------

def test_add_concatenates_every_shared_atom_aligned_attribute():
    """Adding atoms concatenates every shared atom-aligned attribute."""
    target = Structures(
        time=puw.quantity([1.0], 'ps'),
        coordinates=puw.quantity(np.arange(6).reshape(1, 2, 3), 'nm'),
        velocities=puw.quantity(np.arange(6).reshape(1, 2, 3), 'nm/ps'),
        box=puw.quantity(np.eye(3)[None, :, :], 'nm'),
        b_factor=puw.quantity([[0.1, 0.2]], 'nm**2'),
        occupancy=[[0.4, 0.5]],
    )
    source = Structures(
        time=puw.quantity([9.0], 'ps'),
        coordinates=puw.quantity(np.arange(3).reshape(1, 1, 3) + 10, 'nm'),
        velocities=puw.quantity(np.arange(3).reshape(1, 1, 3) + 20, 'nm/ps'),
        box=puw.quantity((np.eye(3) * 2.0)[None, :, :], 'nm'),
        b_factor=puw.quantity([[0.3]], 'nm**2'),
        occupancy=[[0.6]],
    )

    target.add(source, skip_digestion=True)

    assert target.coordinates.shape == (1, 3, 3)
    assert target.velocities.shape == (1, 3, 3)
    assert target.b_factor.shape == (1, 3)
    assert target.occupancy.shape == (1, 3)
    np.testing.assert_allclose(
        puw.get_value(target.b_factor, to_unit='nm**2'),
        [[0.1, 0.2, 0.3]],
    )
    np.testing.assert_allclose(target.occupancy, [[0.4, 0.5, 0.6]])
    np.testing.assert_allclose(puw.get_value(target.time, to_unit='ps'), [1.0])
    np.testing.assert_allclose(
        puw.get_value(target.box, to_unit='nm'),
        np.eye(3)[None, :, :],
    )


def test_add_selects_source_atoms_and_structures_before_concatenating():
    """Selecting source axes produces an aligned atom-axis addition."""
    target = Structures(
        coordinates=puw.quantity(np.zeros((2, 1, 3)), 'nm'),
    )
    source_values = np.arange(27, dtype=float).reshape(3, 3, 3)
    source = Structures(coordinates=puw.quantity(source_values, 'nm'))

    target.add(
        source,
        atom_indices=[0, 2],
        structure_indices=[2, 0],
        skip_digestion=True,
    )

    expected = np.concatenate(
        (
            np.zeros((2, 1, 3)),
            source_values[np.ix_([2, 0], [0, 2], [0, 1, 2])],
        ),
        axis=1,
    )
    np.testing.assert_allclose(
        puw.get_value(target.coordinates, to_unit='nm'),
        expected,
    )


def test_add_drops_one_sided_atom_aligned_attribute():
    """Adding atoms drops a one-sided atom-aligned attribute with a warning."""
    target = Structures(
        coordinates=puw.quantity(np.zeros((1, 2, 3)), 'nm'),
        b_factor=puw.quantity([[0.1, 0.2]], 'nm**2'),
    )
    source = Structures(
        coordinates=puw.quantity(np.ones((1, 1, 3)), 'nm'),
    )

    with pytest.warns(StructuralAttributeDropWarning, match='b_factor'):
        target.add(source, skip_digestion=True)

    assert target.coordinates.shape == (1, 3, 3)
    assert target.b_factor is None


def test_add_is_atomic_when_a_warning_is_an_error():
    """Treating the drop warning as an error leaves the target unchanged."""
    target = Structures(
        coordinates=puw.quantity(np.zeros((1, 2, 3)), 'nm'),
        b_factor=puw.quantity([[0.1, 0.2]], 'nm**2'),
    )
    source = Structures(coordinates=puw.quantity(np.ones((1, 1, 3)), 'nm'))
    original_coordinates = target.coordinates.copy()
    original_b_factor = target.b_factor.copy()

    with warnings.catch_warnings():
        warnings.simplefilter('error', StructuralAttributeDropWarning)
        with pytest.raises(StructuralAttributeDropWarning):
            target.add(source, skip_digestion=True)

    np.testing.assert_allclose(
        puw.get_value(target.coordinates, to_unit='nm'),
        puw.get_value(original_coordinates, to_unit='nm'),
    )
    np.testing.assert_allclose(
        puw.get_value(target.b_factor, to_unit='nm**2'),
        puw.get_value(original_b_factor, to_unit='nm**2'),
    )
