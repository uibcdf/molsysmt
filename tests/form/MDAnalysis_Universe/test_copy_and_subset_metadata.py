"""Preserving stored MDAnalysis data through public independent operations."""

import numpy as np
import pytest

import molsysmt as msm

_PAIRS = [(0, 1), (1, 2), (2, 3), (3, 4)]
_ORDERS = [1.5, 2, 1, None]
_TYPES = ["aromatic", "unrecognized bond class longer than eight", "single", "dative"]
_GUESSED = [False, True, False, True]
_FORMAL_CHARGES = [0, 0, 1, -1, 0]


@pytest.fixture
def stored_universe():
    """Build three structures with independently declared chemical metadata."""
    mda = pytest.importorskip("MDAnalysis")
    from MDAnalysis.core.topologyattrs import Bonds, FormalCharges

    universe = mda.Universe.empty(
        5,
        n_residues=2,
        n_segments=1,
        atom_resindex=[0, 0, 1, 1, 1],
        residue_segindex=[0, 0],
    )
    for name, values in (
        ("names", ["C1", "C2", "N", "O", "S"]),
        ("types", ["C", "C", "N", "O", "S"]),
        ("ids", [10, 11, 12, 13, 14]),
        ("resnames", ["L1", "L2"]),
        ("resids", [7, 7]),
        ("segids", ["source-chain"]),
    ):
        universe.add_TopologyAttr(name, values)
    universe.add_TopologyAttr(FormalCharges(_FORMAL_CHARGES))
    universe.add_TopologyAttr(
        Bonds(_PAIRS, order=_ORDERS, types=_TYPES, guessed=_GUESSED)
    )
    coordinates = np.arange(45, dtype=np.float32).reshape(3, 5, 3)
    universe.load_new(
        coordinates,
        format=mda.coordinates.memory.MemoryReader,
        order="fac",
        velocities=coordinates / 10,
        forces=coordinates / 100,
        dimensions=np.array(
            [
                [20, 30, 40, 80, 90, 100],
                [21, 31, 41, 81, 91, 101],
                [22, 32, 42, 82, 92, 102],
            ],
            dtype=np.float32,
        ),
        dt=2,
        time_offset=5,
    )
    universe.trajectory[1]
    return universe


def _source(universe, source_kind):
    if source_kind == "universe":
        return universe, [0, 1, 2, 3, 4]
    indices = [4, 1, 3, 2, 0]
    return universe.atoms[indices], indices


def _bonds(item):
    """Read stored values by stable atom labels, without chemical interpretation."""
    atoms = item.atoms
    topology = atoms.universe._topology
    members = set(atoms.indices.tolist())
    output = {}
    bonds = topology.bonds
    for pair, order, kind, guessed in zip(
        bonds.values, bonds.order, bonds.types, bonds._guessed, strict=True
    ):
        if all(index in members for index in pair):
            labels = tuple(
                sorted(int(atoms.universe.atoms.ids[index]) for index in pair)
            )
            output[labels] = (order, kind, bool(guessed))
    return output


def _stamp(universe):
    """Capture the complete fixture's cursor, arrays and stored declarations."""
    reader = universe.trajectory
    return (
        reader.frame,
        tuple(universe.atoms.ids),
        tuple(universe.atoms.names),
        tuple(universe.atoms.formalcharges),
        tuple(sorted(_bonds(universe).items())),
        reader.coordinate_array.tobytes(),
        reader.velocity_array.tobytes(),
        reader.force_array.tobytes(),
        reader.dimensions_array.tobytes(),
        reader.ts.dt,
        reader.ts.data.get("time_offset"),
    )


def _expected_bonds(indices, types=None):
    selected = set(indices)
    types = _TYPES if types is None else types
    return {
        (left + 10, right + 10): (order, kind, guessed)
        for (left, right), order, kind, guessed in zip(
            _PAIRS, _ORDERS, types, _GUESSED, strict=True
        )
        if left in selected and right in selected
    }


def _assert_stored_data(output, source, indices, structures):
    atoms = output.atoms
    np.testing.assert_array_equal(atoms.ids, np.array(indices) + 10)
    np.testing.assert_array_equal(atoms.names, source.atoms.names[indices])
    np.testing.assert_array_equal(
        atoms.formalcharges, np.array(_FORMAL_CHARGES)[indices]
    )
    assert _bonds(output) == _expected_bonds(indices)
    assert atoms.residues.resids.tolist() == [7, 7]
    assert atoms.segments.segids.tolist() == ["source-chain"]

    reader = atoms.universe.trajectory
    frame = reader.frame
    assert len(reader) == len(structures)
    try:
        for output_index, source_index in enumerate(structures):
            ts = reader[output_index]
            np.testing.assert_allclose(
                atoms.positions,
                source.trajectory.coordinate_array[source_index, indices],
            )
            assert ts.has_velocities
            np.testing.assert_allclose(
                atoms.velocities,
                source.trajectory.velocity_array[source_index, indices],
            )
            assert ts.has_forces
            np.testing.assert_allclose(
                atoms.forces, source.trajectory.force_array[source_index, indices]
            )
            np.testing.assert_allclose(
                ts.dimensions, source.trajectory.dimensions_array[source_index]
            )
            assert ts.time == 5 + 2 * source_index
    finally:
        reader[frame]


@pytest.mark.parametrize("source_kind", ["universe", "atomgroup"])
def test_public_copy_preserves_stored_data_independently(stored_universe, source_kind):
    item, indices = _source(stored_universe, source_kind)
    before = _stamp(stored_universe)

    output = msm.copy(item)

    assert output is not item
    assert output.atoms.universe is not stored_universe
    _assert_stored_data(output, stored_universe, indices, [0, 1, 2])
    output.atoms.positions += 100
    output.atoms.formalcharges = np.zeros(len(indices), dtype=int)
    output.atoms.universe._topology.bonds.order[0] = 4
    output.atoms.universe._topology.bonds.types[0] = "changed independent label"
    assert _stamp(stored_universe) == before


@pytest.mark.parametrize("source_kind", ["universe", "atomgroup"])
@pytest.mark.parametrize("operation", ["extract", "same_form", "to_universe"])
@pytest.mark.parametrize(
    "selection_kind", ["all", "atoms_and_structures", "structures"]
)
def test_public_extraction_preserves_stored_data(
    stored_universe, source_kind, operation, selection_kind
):
    item, indices = _source(stored_universe, source_kind)
    before = _stamp(stored_universe)
    selection = "all"
    structures = [0, 1, 2]
    options = {}
    if selection_kind == "atoms_and_structures":
        indices = [4, 1, 3, 2]
        selection = indices if source_kind == "universe" else [0, 1, 2, 3]
    if selection_kind != "all":
        structures = [2, 0]
        options["structure_indices"] = structures

    if operation == "extract":
        output = msm.extract(item, selection=selection, **options)
    else:
        target = (
            "MDAnalysis.Universe" if operation == "to_universe" else msm.get_form(item)
        )
        output = msm.convert(item, to_form=target, selection=selection, **options)

    assert output is not item
    assert output.atoms.universe is not stored_universe
    _assert_stored_data(output, stored_universe, indices, structures)
    assert _stamp(stored_universe) == before


@pytest.mark.parametrize("source_kind", ["universe", "atomgroup"])
def test_missing_bond_type_does_not_erase_other_stored_types(
    stored_universe, source_kind
):
    kinds = list(_TYPES)
    kinds[2] = None
    stored_universe._topology.bonds.types[2] = None
    item, indices = _source(stored_universe, source_kind)
    before = _stamp(stored_universe)

    output = msm.extract(item)

    assert _bonds(output) == _expected_bonds(indices, kinds)
    assert _stamp(stored_universe) == before


@pytest.mark.parametrize("source_kind", ["universe", "atomgroup"])
@pytest.mark.parametrize("operation", ["extract", "same_form"])
def test_structure_selection_preserves_stored_forces(
    stored_universe, source_kind, operation
):
    item, indices = _source(stored_universe, source_kind)
    before = _stamp(stored_universe)
    options = {"structure_indices": [2, 0]}

    if operation == "extract":
        output = msm.extract(item, **options)
    else:
        output = msm.convert(item, to_form=msm.get_form(item), **options)

    reader = output.atoms.universe.trajectory
    assert reader.ts.has_forces
    np.testing.assert_allclose(
        reader.force_array[:, output.atoms.indices],
        stored_universe.trajectory.force_array[[2, 0]][:, indices],
    )
    assert _stamp(stored_universe) == before


@pytest.mark.parametrize("source_kind", ["universe", "atomgroup"])
@pytest.mark.parametrize("operation", ["extract", "same_form"])
def test_unrestricted_no_copy_returns_the_original(
    stored_universe, source_kind, operation
):
    item, _ = _source(stored_universe, source_kind)
    before = _stamp(stored_universe)

    if operation == "extract":
        output = msm.extract(item, copy_if_all=False)
    else:
        output = msm.convert(item, to_form=msm.get_form(item), copy_if_all=False)

    assert output is item
    assert _stamp(stored_universe) == before
