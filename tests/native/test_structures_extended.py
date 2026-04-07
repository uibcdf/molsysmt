"""
Extended tests for molsysmt.native.Structures covering uncovered properties and methods.
"""
import numpy as np
import pytest
from molsysmt.native import Structures
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentLengthError


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
    s.velocities = _coords(n_structures=3)
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
    s.velocities = _coords(n_structures=1, n_atoms=7)
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
