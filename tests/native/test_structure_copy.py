"""Native structure copies must isolate writes without whole-series reads."""

import copy
import pickle

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.native import Structures
from molsysmt.native._structure_array import _StructureArray


@pytest.fixture
def structures(monkeypatch):
    import molsysmt.native._structure_array as storage

    monkeypatch.setattr(storage, "_BLOCK_BYTES", 192)
    result = Structures(
        coordinates=puw.quantity(np.arange(84.0).reshape(7, 4, 3), "nm"),
        box=puw.quantity(np.repeat(np.eye(3)[None], 7, axis=0), "nm"),
        time=puw.quantity(np.arange(7.0), "ps"),
        velocities=puw.quantity(np.ones((7, 4, 3)), "nm/ps"),
        temperature=puw.quantity(np.arange(7.0) + 300, "K"),
        occupancy=np.ones((7, 4)),
        alternate_location=[
            {
                0: {
                    "location_id": ["A"],
                    "occupancy": np.array([0.5]),
                    "b_factor": puw.quantity([0.01], "nm**2"),
                    "atom_id": ["1"],
                    "coordinates": puw.quantity([[0.0, 0.0, 0.0]], "nm"),
                }
            }
            for _ in range(7)
        ],
    )
    result.bioassembly = {
        "example": {
            "chain_indices": [np.array([0])],
            "rotations": np.eye(3)[None],
            "translations": puw.quantity(np.zeros((1, 3)), "nm"),
        }
    }
    return result


def _deferred(source):
    return source.copy(deep=False)


@pytest.mark.parametrize(
    "copier", [copy.copy, copy.deepcopy, _deferred, Structures.copy]
)
def test_copy_isolates_selected_coordinate_box_and_metadata_edits(structures, copier):
    original = puw.get_value(structures.get_coordinates(), to_unit="nm")
    duplicate = copier(structures)
    duplicate.set_coordinates(
        indices=[3, 1],
        structure_indices=[6, 0],
        value=puw.quantity(np.full((2, 2, 3), 1000.0), "angstrom"),
    )
    duplicate.set_box(
        structure_indices=[0], value=puw.quantity([np.eye(3) * 20], "angstrom")
    )
    duplicate._time[0] = 42
    duplicate._velocities[0, 0, 0] = 42
    duplicate._temperature[0] = 42
    duplicate._occupancy[0, 0] = 42
    duplicate.alternate_location[0][0]["occupancy"][0] = 0.8
    duplicate.bioassembly["example"]["chain_indices"][0][0] = 1
    np.testing.assert_array_equal(
        puw.get_value(structures.get_coordinates(), to_unit="nm"), original
    )
    truth = original.copy()
    truth[np.ix_([6, 0], [3, 1])] = 100
    np.testing.assert_allclose(
        puw.get_value(duplicate.get_coordinates(), to_unit="nm"), truth
    )
    np.testing.assert_array_equal(
        puw.get_value(structures.get_box(), to_unit="nm"),
        np.repeat(np.eye(3)[None], 7, axis=0),
    )
    np.testing.assert_allclose(
        puw.get_value(duplicate.get_box(structure_indices=[0]), to_unit="nm"),
        [np.eye(3) * 2],
    )
    assert structures._time[0] == 0
    assert structures._velocities[0, 0, 0] == 1
    assert structures._temperature[0] == 300
    assert structures._occupancy[0, 0] == 1
    assert structures.alternate_location[0][0]["occupancy"][0] == 0.5
    np.testing.assert_array_equal(
        structures.bioassembly["example"]["chain_indices"][0], [0]
    )
    structures.set_coordinates(
        indices=[0],
        structure_indices=[1],
        value=puw.quantity([[[9.0, 8.0, 7.0]]], "nm"),
    )
    np.testing.assert_array_equal(
        puw.get_value(
            duplicate.get_coordinates(indices=[0], structure_indices=[1]), to_unit="nm"
        ),
        original[1:2, 0:1],
    )


def test_deferred_copy_shares_untouched_bytes_and_replaces_only_affected_blocks(
    structures,
):
    duplicate = structures.copy(deep=False)
    source_blocks = structures._coordinates._blocks
    for first, second in zip(source_blocks, duplicate._coordinates._blocks):
        assert first is not second
        assert np.shares_memory(first, second)
        with pytest.raises(ValueError):
            second.flags.writeable = True
    duplicate.set_coordinates(
        indices=[0],
        structure_indices=[2],
        value=puw.quantity([[[1.0, 2.0, 3.0]]], "nm"),
    )
    for index, (first, second) in enumerate(
        zip(source_blocks, duplicate._coordinates._blocks)
    ):
        assert np.shares_memory(first, second) == (index != 1)
    for first, second in zip(structures._box._blocks, duplicate._box._blocks):
        assert np.shares_memory(first, second)


def test_eager_copy_allocates_geometry_bytes_independently(structures):
    duplicate = structures.copy()
    for name in ("_coordinates", "_box"):
        for first, second in zip(
            getattr(structures, name)._blocks, getattr(duplicate, name)._blocks
        ):
            assert not np.shares_memory(first, second)


def test_caller_alias_and_input_writeability_are_not_changed():
    coordinates = np.arange(18.0).reshape(2, 3, 3)
    boxes = np.repeat(np.eye(3)[None], 2, axis=0)
    structures = Structures(
        coordinates=puw.quantity(coordinates, "nm"), box=puw.quantity(boxes, "nm")
    )
    assert coordinates.flags.writeable
    assert boxes.flags.writeable
    coordinates[:] = -1
    boxes[:] = -1
    np.testing.assert_array_equal(
        puw.get_value(structures.get_coordinates(), to_unit="nm"),
        np.arange(18.0).reshape(2, 3, 3),
    )
    np.testing.assert_array_equal(
        puw.get_value(structures.get_box(), to_unit="nm"),
        np.repeat(np.eye(3)[None], 2, axis=0),
    )


def test_full_native_coordinate_assignment_initializes_and_clears_absent_series():
    source = Structures()
    assert source.get_coordinates() is None
    source.set_coordinates(value=puw.quantity(np.ones((2, 3, 3)) * 10, "angstrom"))
    np.testing.assert_allclose(
        puw.get_value(source.get_coordinates(), to_unit="nm"), 1.0
    )
    assert source.n_structures == 2
    source.coordinates = None
    assert source.get_coordinates() is None
    assert source.n_structures == 0


@pytest.mark.parametrize("getter", ["get_coordinates", "get_box"])
def test_selected_public_outputs_are_owned_and_editable(structures, getter):
    duplicate = structures.copy(deep=False)
    values = puw.get_value(
        getattr(duplicate, getter)(structure_indices=[6, 0, 6]), to_unit="nm"
    )
    assert values.flags.writeable
    values[:] = -100
    assert np.all(puw.get_value(getattr(duplicate, getter)(), to_unit="nm") >= 0)
    assert np.all(puw.get_value(getattr(structures, getter)(), to_unit="nm") >= 0)


def test_nonconsecutive_queries_iterator_extraction_and_rust_avoid_dense_reads(
    structures, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail(
            "A selected native operation assembled the complete geometry series"
        )

    with puw.context(standard_units=["angstrom", "ns", "kcal/mol", "K"]):
        with monkeypatch.context() as patch:
            patch.setattr(_StructureArray, "_dense", forbidden)
            assert structures.n_atoms == 4
            assert structures.n_structures == 7
            assert "n_atoms=4" in repr(structures)
            output = structures.get(
                element="atom",
                selection=[3, 1, 3],
                structure_indices=[6, 0, 6],
                coordinates=True,
            )
            universal = msm.get(
                structures,
                element="atom",
                selection=[3, 1, 3],
                structure_indices=[6, 0, 6],
                coordinates=True,
            )
            all_atoms = structures.get(structure_indices=[6, 0, 6], coordinates=True)
            boxes = structures.get(structure_indices=[6, 0, 6], box=True)
            chunks = list(
                msm.Iterator(
                    structures,
                    selection=[3, 1],
                    structure_indices=[6, 0, 6],
                    chunk=2,
                    coordinates=True,
                )
            )
            extracted = structures.extract(
                atom_indices=[3, 1], structure_indices=[6, 0, 6]
            )
            distances = msm.structure.get_distances(
                structures,
                selection=[0],
                selection_2=[1],
                structure_indices=[6, 0, 6],
                pbc=False,
            )
        assert puw.has_unit(output, "angstrom")
        assert puw.has_unit(boxes, "angstrom")
        truth = np.arange(84.0).reshape(7, 4, 3)
        expected = truth[np.ix_([6, 0, 6], [3, 1, 3])]
        np.testing.assert_allclose(puw.get_value(output, to_unit="nm"), expected)
        np.testing.assert_allclose(puw.get_value(universal, to_unit="nm"), expected)
        np.testing.assert_allclose(
            puw.get_value(all_atoms, to_unit="nm"), truth[[6, 0, 6]]
        )
        np.testing.assert_allclose(
            np.concatenate([puw.get_value(chunk, to_unit="nm") for chunk in chunks]),
            truth[np.ix_([6, 0, 6], [3, 1])],
        )
        np.testing.assert_allclose(
            puw.get_value(extracted.get_coordinates(), to_unit="nm"),
            truth[np.ix_([6, 0, 6], [3, 1])],
        )
        np.testing.assert_allclose(
            puw.get_value(distances, to_unit="nm"), np.full((3, 1, 1), np.sqrt(27))
        )


def test_repeated_write_indices_use_last_value_and_empty_edits_do_nothing(structures):
    duplicate = structures.copy(deep=False)
    values = np.arange(27.0).reshape(3, 3, 3) + 100
    duplicate.set_coordinates(
        indices=[3, 1, 3], structure_indices=[6, 0, 6], value=puw.quantity(values, "nm")
    )
    truth = np.arange(84.0).reshape(7, 4, 3)
    for i, structure in enumerate([6, 0, 6]):
        for j, atom in enumerate([3, 1, 3]):
            truth[structure, atom] = values[i, j]
    np.testing.assert_array_equal(
        puw.get_value(duplicate.get_coordinates(), to_unit="nm"), truth
    )
    store = duplicate._coordinates
    duplicate.set_coordinates(
        indices=[], structure_indices=[0], value=puw.quantity(np.empty((1, 0, 3)), "nm")
    )
    assert duplicate._coordinates is store


def test_failed_replacement_is_atomic(structures, monkeypatch):
    import molsysmt.native._structure_array as storage

    before = structures._coordinates
    with pytest.raises((ValueError, IndexError)):
        structures.set_coordinates(
            indices=[0],
            structure_indices=[0, 3],
            value=puw.quantity([[[1.0, 2.0, 3.0]]], "nm"),
        )
    assert structures._coordinates is before
    original = storage._freeze
    count = 0

    def fail_second_block(array):
        nonlocal count
        count += 1
        if count == 2:
            raise MemoryError("synthetic allocation failure")
        return original(array)

    monkeypatch.setattr(storage, "_freeze", fail_second_block)
    with pytest.raises(MemoryError):
        structures.set_coordinates(
            indices=[0],
            structure_indices=[0, 3],
            value=puw.quantity(np.ones((2, 1, 3)), "nm"),
        )
    assert structures._coordinates is before


def test_failed_append_does_not_publish_part_of_a_new_payload(structures, monkeypatch):
    import molsysmt.native._structure_array as storage
    from molsysmt._private.smonitor import StructuralAttributeDropWarning

    before = vars(structures).copy()
    original = storage._freeze
    count = 0

    def fail_second_block(array):
        nonlocal count
        count += 1
        if count == 2:
            raise MemoryError("synthetic append allocation failure")
        return original(array)

    monkeypatch.setattr(storage, "_freeze", fail_second_block)
    with pytest.warns(StructuralAttributeDropWarning), pytest.raises(MemoryError):
        structures.append(
            coordinates=puw.quantity(np.ones((1, 4, 3)), "nm"),
            box=puw.quantity([np.eye(3)], "nm"),
            time=puw.quantity([7.0], "ps"),
        )
    assert vars(structures).keys() == before.keys()
    assert all(vars(structures)[key] is value for key, value in before.items())


def test_native_hooks_preserve_memo_type_and_skip_restoration(structures, monkeypatch):
    class Extended(Structures):
        __slots__ = ("extra",)

    source = object.__new__(Extended)
    source.__dict__.update(vars(structures))
    source.extra = {"self": source}
    source.alias = source.extra

    def forbidden(*args, **kwargs):
        pytest.fail("Copy called a constructor or restoration hook")

    with monkeypatch.context() as patch:
        patch.setattr(Structures, "__init__", forbidden)
        patch.setattr(Structures, "__setstate__", forbidden)
        duplicate, again, metadata = copy.deepcopy([source, source, source.extra])
        deferred = copy.copy(source)
    assert type(duplicate) is Extended
    assert duplicate is again
    assert duplicate.extra is metadata
    assert duplicate.alias is metadata
    assert metadata["self"] is duplicate
    assert deferred.extra["self"] is deferred


@pytest.mark.parametrize("deep", [True, False])
def test_h5msm_and_pickle_preserve_copied_blocks_under_nondefault_units(
    structures, deep, tmp_path
):
    duplicate = structures.copy(deep=deep)
    with puw.context(standard_units=["angstrom", "ns", "kcal/mol", "K"]):
        duplicate.set_coordinates(
            indices=[0],
            structure_indices=[0],
            value=puw.quantity([[[10.0, 20.0, 30.0]]], "angstrom"),
        )
        path = str(tmp_path / "structures.h5msm")
        msm.convert(duplicate, to_form="file:h5msm", output_filename=path)
        restored = msm.convert(path, to_form="molsysmt.MolSys").structures
        unpickled = pickle.loads(pickle.dumps(duplicate))
        expected = np.arange(84.0).reshape(7, 4, 3)
        expected[0, 0] = [1.0, 2.0, 3.0]
        for candidate in (restored, unpickled):
            np.testing.assert_allclose(
                puw.get_value(candidate.get_coordinates(), to_unit="nm"),
                expected,
            )
            np.testing.assert_allclose(
                puw.get_value(candidate.get_time(), to_unit="ps"), np.arange(7.0)
            )
            for block in candidate._coordinates._blocks:
                with pytest.raises(ValueError):
                    block.flags.writeable = True
        np.testing.assert_array_equal(
            puw.get_value(structures.get_coordinates(), to_unit="nm"),
            np.arange(84.0).reshape(7, 4, 3),
        )


def test_h5msm_reads_writes_and_appends_geometry_in_bounded_blocks(
    structures, tmp_path, monkeypatch
):
    import h5py

    source = structures.copy(deep=False)
    source.bioassembly = None
    source.constant_box = True
    filename = str(tmp_path / "blocked.h5msm")
    original_read = h5py.Dataset.__getitem__
    original_write = h5py.Dataset.__setitem__
    reads = []
    writes = []

    def rows_touched(dataset, key):
        axis = key[0] if isinstance(key, tuple) else key
        if isinstance(axis, slice):
            return len(range(*axis.indices(dataset.shape[0])))
        if np.isscalar(axis):
            return 1
        return len(axis)

    def read(dataset, key):
        if dataset.name in {"/structures/coordinates", "/structures/box"}:
            count = rows_touched(dataset, key)
            assert count <= 2, (
                "A geometry read exceeded the fixture's numeric block budget"
            )
            reads.append(count)
        return original_read(dataset, key)

    def write(dataset, key, value):
        if dataset.name in {"/structures/coordinates", "/structures/box"}:
            count = rows_touched(dataset, key)
            assert count <= 2, (
                "A geometry write exceeded the fixture's numeric block budget"
            )
            writes.append(count)
        return original_write(dataset, key, value)

    def forbidden(*args, **kwargs):
        pytest.fail("H5MSM materialized the complete native geometry storage")

    with puw.context(standard_units=["angstrom", "ns", "kcal/mol", "K"]):
        with monkeypatch.context() as patch:
            patch.setattr(_StructureArray, "_dense", forbidden)
            patch.setattr(h5py.Dataset, "__getitem__", read)
            patch.setattr(h5py.Dataset, "__setitem__", write)
            msm.convert(source, to_form="file:h5msm", output_filename=filename)
            msm.h5msm.append_structures(filename, source)
            complete = msm.h5msm.read(filename)
            selected = msm.convert(
                filename,
                to_form="molsysmt.MolSys",
                selection=[3, 1],
                structure_indices=[13, 0, 13],
            )
        truth = np.arange(84.0).reshape(7, 4, 3)
        np.testing.assert_allclose(
            puw.get_value(complete.structures.get_coordinates(), to_unit="nm"),
            np.concatenate([truth, truth]),
        )
        np.testing.assert_allclose(
            puw.get_value(selected.structures.get_coordinates(), to_unit="nm"),
            truth[np.ix_([6, 0, 6], [3, 1])],
        )
        assert complete.structures.constant_box
        assert reads and writes


@pytest.mark.parametrize("deep", [None, 1, "False", np.bool_(True)])
def test_copy_rejects_invalid_allocation_option(structures, deep):
    from molsysmt._private.smonitor import ArgumentError

    with pytest.raises(ArgumentError):
        structures.copy(deep=deep)
