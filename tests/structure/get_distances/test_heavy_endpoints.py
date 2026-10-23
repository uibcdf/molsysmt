"""Protecting endpoint identities and units through chunked distance execution."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.native import Structures


@pytest.fixture
def geometry():
    xyz = np.array(
        [
            [[0, 0, 0], [2, 1, 0], [4, 0, 1], [9, 0, 0], [3, 3, 0], [6, 2, 2]],
            [[1, 0, 0], [3, 2, 0], [5, 1, 1], [8, 0, 0], [2, 4, 0], [7, 2, 3]],
            [[2, 0, 0], [4, 3, 0], [6, 2, 1], [7, 0, 0], [1, 5, 0], [8, 2, 4]],
        ],
        dtype=float,
    )
    return Structures(
        coordinates=puw.quantity(xyz, "nm"),
        box=puw.quantity(np.tile(np.eye(3) * 10, (3, 1, 1)), "nm"),
    )


def oracle(geometry, atoms, second, structures, other, periodic):
    xyz = puw.get_value(geometry.coordinates, to_unit="nm")
    delta = (
        xyz[np.ix_(other, second)][:, None, :, :]
        - xyz[np.ix_(structures, atoms)][:, :, None, :]
    )
    if periodic:
        delta -= 10 * np.round(delta / 10)
    return np.sqrt(np.sum(delta * delta, axis=-1))


@pytest.mark.parametrize("second", [[1, 3], [1, 3, 5], [3, 1, 3]])
@pytest.mark.parametrize("separate", [False, True])
@pytest.mark.parametrize("periodic", [False, True])
def test_flat_endpoints_keep_populations_and_structure_correspondence(
    geometry, second, separate, periodic
):
    first = [4, 0, 2]
    structures = [2, 0, 2]
    other = [0, 2, 1] if separate else structures
    options = dict(
        selection=first,
        selection_2=second,
        structure_indices=structures,
        pbc=periodic,
        output_indices="atom",
        output_structure_indices="structure",
    )
    if separate:
        options["structure_indices_2"] = other
    expected = oracle(geometry, first, second, structures, other, periodic)
    with msm.configure.context(chunk_size=2, chunk_memory_fraction=None):
        result = msm.structure.get_distances(geometry, heavy_mode="force", **options)
    np.testing.assert_array_equal(result[0], first)
    np.testing.assert_array_equal(result[1], second)
    np.testing.assert_array_equal(result[2], structures)
    if separate:
        np.testing.assert_array_equal(result[3], other)
    assert result[-1].shape == (3, 3, len(second))
    np.testing.assert_allclose(
        puw.get_value(result[-1], to_unit="nm"), expected, atol=1e-13
    )
    eager = msm.structure.get_distances(geometry, heavy_mode="off", **options)
    np.testing.assert_allclose(
        puw.get_value(eager[-1], to_unit="nm"), expected, atol=1e-13
    )


def test_forced_units_follow_application_policy(geometry):
    previous = list(puw.configure.get_standard_units())
    try:
        puw.configure.set_standard_units(
            ["pm", "ps", "K", "mole", "dalton", "e", "kJ/mol", "radians"]
        )
        result = msm.structure.get_distances(
            geometry,
            selection=[0, 2],
            selection_2=[1],
            structure_indices=[2, 0],
            pbc=False,
            heavy_mode="force",
        )
        assert puw.get_unit(result) == puw.unit("pm")
        expected = oracle(geometry, [0, 2], [1], [2, 0], [2, 0], False)
        np.testing.assert_allclose(puw.get_value(result), expected * 1000)
    finally:
        puw.configure.set_standard_units(previous)


def test_implicit_atoms_with_explicit_structure_axis(geometry):
    result = msm.structure.get_distances(
        geometry,
        selection=[4, 0],
        structure_indices=[2, 0, 2],
        structure_indices_2=[0, 2, 1],
        pbc=False,
        heavy_mode="force",
    )
    np.testing.assert_allclose(
        puw.get_value(result, to_unit="nm"),
        oracle(geometry, [4, 0], [4, 0], [2, 0, 2], [0, 2, 1], False),
    )


@pytest.mark.parametrize("form", ["native", "h5msm"])
def test_separate_endpoint_reads_are_bounded(geometry, form, tmp_path, monkeypatch):
    from molsysmt._private.execution import ChunkedExecutor

    source = geometry
    if form == "h5msm":
        source = str(tmp_path / "coordinates.h5msm")
        msm.convert(geometry, to_form=source)
    reads = []
    original = ChunkedExecutor._get_form_iterator

    def inspect(executor, structures, chunk_size):
        if executor.operation == "get_distances":
            reads.append((list(structures), chunk_size))
        return original(executor, structures, chunk_size)

    monkeypatch.setattr(ChunkedExecutor, "_get_form_iterator", inspect)
    options = dict(
        selection=[4, 0],
        selection_2=[1, 3, 5],
        structure_indices=[2, 0, 2],
        structure_indices_2=[0, 2, 1],
        pbc=False,
        heavy_mode="force",
    )
    with msm.configure.context(chunk_size=2, chunk_memory_fraction=None):
        result = msm.structure.get_distances(source, **options)
    np.testing.assert_allclose(
        puw.get_value(result, to_unit="nm"),
        oracle(geometry, [4, 0], [1, 3, 5], [2, 0, 2], [0, 2, 1], False),
    )
    assert reads == [([2, 0, 2], 2), ([0, 2], 2), ([1], 1)]


def test_indexed_pdbqt_endpoints_use_requested_models(tmp_path):
    from devtools.scripts.benchmark_pdbqt_storage import write_fixture
    from molsysmt.native import PDBQTFileHandler

    path = tmp_path / "poses.pdbqt"
    write_fixture(path, 12, 8)
    first, second = [7, 0, 4], [1, 3]
    structures, other = [11, 0, 11], [0, 7, 3]
    options = dict(
        selection=first,
        selection_2=second,
        structure_indices=structures,
        structure_indices_2=other,
        pbc=False,
        heavy_mode="force",
    )
    # The writer places atom a at ((1+s/1000)/10, a/1000, .3) nm.
    expected = np.sqrt(
        ((np.array(other) - structures)[:, None, None] / 10000) ** 2
        + ((np.array(second)[None, None, :] - np.array(first)[None, :, None]) / 1000)
        ** 2
    )
    with PDBQTFileHandler(path, storage_mode="indexed") as source:
        with msm.configure.context(chunk_size=2, chunk_memory_fraction=None):
            result = msm.structure.get_distances(source, **options)
            file_result = msm.structure.get_distances(str(path), **options)
    np.testing.assert_allclose(
        puw.get_value(result, to_unit="nm"), expected, atol=1e-14
    )
    np.testing.assert_allclose(
        puw.get_value(file_result, to_unit="nm"), expected, atol=1e-14
    )


@pytest.mark.parametrize("mode", ["force", "auto"])
def test_selected_output_shape_and_units_survive_disk_backing(geometry, mode):
    from molsysmt._private.execution import PersistentResultHandle

    xyz = np.tile(puw.get_value(geometry.coordinates, to_unit="nm"), (40, 1, 1))
    source = Structures(coordinates=puw.quantity(xyz, "nm"))
    with puw.context(standard_units=["pm", "ps", "radians"]):
        with msm.configure.context(
            max_ram_usage=4096, chunk_memory_fraction=None, chunk_size=2
        ):
            result = msm.structure.get_distances(
                source,
                selection=[4, 0, 2],
                selection_2=[1, 3],
                pbc=False,
                heavy_mode=mode,
            )
    values = puw.get_value(result)
    assert isinstance(values, PersistentResultHandle)
    path = values.path
    try:
        assert values.shape == (120, 3, 2)
        assert path.stat().st_size == 120 * 3 * 2 * 8
        assert puw.get_unit(result) == puw.unit("pm")
        expected = np.tile(
            oracle(geometry, [4, 0, 2], [1, 3], [0, 1, 2], [0, 1, 2], False), (40, 1, 1)
        )
        np.testing.assert_allclose(values[:], expected * 1000)
    finally:
        values.cleanup()
    assert not path.exists()


def test_mismatched_structure_lists_fail_before_the_kernel(geometry, monkeypatch):
    from molsysmt._private import rust_backend
    from molsysmt._private.smonitor import ArgumentError

    def forbidden(*args, **kwargs):
        raise AssertionError("An invalid structure correspondence must not reach Rust.")

    monkeypatch.setattr(rust_backend, "get_distances", forbidden)
    with pytest.raises(ArgumentError, match="equal length"):
        msm.structure.get_distances(
            geometry,
            selection=[0, 2],
            selection_2=[1],
            structure_indices=[2, 0],
            structure_indices_2=[1],
            pbc=False,
            heavy_mode="force",
        )


@pytest.mark.parametrize(
    "atoms, second, structures, shape",
    [
        ([0, 2], [1], [], (0, 2, 1)),
        ([], [1], [2, 0], (2, 0, 1)),
        ([0, 2], [], [2, 0], (2, 2, 0)),
    ],
)
def test_empty_axes_are_shaped(geometry, atoms, second, structures, shape):
    result = msm.structure.get_distances(
        geometry,
        selection=atoms,
        selection_2=second,
        structure_indices=structures,
        pbc=False,
        heavy_mode="force",
    )
    assert result.shape == shape


def test_second_center_uses_the_existing_center_path(geometry):
    result = msm.structure.get_distances(
        geometry,
        selection=[0, 2],
        selection_2=[1, 3],
        center_of_atoms_2=True,
        structure_indices=[2, 0],
        pbc=False,
        heavy_mode="force",
    )
    xyz = puw.get_value(geometry.coordinates, to_unit="nm")
    first = xyz[np.ix_([2, 0], [0, 2])]
    center = xyz[np.ix_([2, 0], [1, 3])].mean(axis=1, keepdims=True)
    expected = np.sqrt(np.sum((first[:, :, None] - center[:, None]) ** 2, axis=-1))
    assert result.shape == (2, 2, 1)
    np.testing.assert_allclose(puw.get_value(result, to_unit="nm"), expected)


def test_original_bundled_report_retains_the_second_population():
    source = msm.convert(
        msm.systems["pentalanine"]["traj_pentalanine.h5msm"],
        structure_indices=[0, 8, 3],
    )
    result = msm.structure.get_distances(
        source,
        selection=[0, 2, 4],
        selection_2=[1, 3],
        structure_indices=[2, 0, 2],
        pbc=False,
        heavy_mode="force",
    )
    assert result.shape == (3, 3, 2)
    assert puw.get_value(result, to_unit="nm")[0, 0, 0] == pytest.approx(
        0.10899963385132325
    )


def test_dictionary_retains_source_atom_and_structure_indices(geometry):
    result = msm.structure.get_distances(
        geometry,
        selection=[4, 0],
        selection_2=[1, 3],
        structure_indices=[2, 0, 1],
        structure_indices_2=[0, 2, 1],
        output_type="dictionary",
        output_indices="atom",
        output_structure_indices="structure",
        pbc=False,
        heavy_mode="force",
    )
    expected = oracle(geometry, [4, 0], [1, 3], [2, 0, 1], [0, 2, 1], False)
    for ai, atom in enumerate([4, 0]):
        for bi, second in enumerate([1, 3]):
            for si, (first_structure, second_structure) in enumerate(
                zip([2, 0, 1], [0, 2, 1])
            ):
                assert puw.get_value(
                    result[atom][second][first_structure][second_structure],
                    to_unit="nm",
                ) == pytest.approx(expected[si, ai, bi])


def test_one_slab_work_budget_is_checked_before_rust(geometry, monkeypatch):
    from molsysmt._private import rust_backend
    from molsysmt._private.smonitor import MemoryBudgetExceededError

    def forbidden(*args, **kwargs):
        raise AssertionError("Over-budget work must not reach the scientific kernel.")

    monkeypatch.setattr(rust_backend, "get_distances", forbidden)
    with msm.configure.context(max_ram_usage=100):
        with pytest.raises(MemoryBudgetExceededError, match="slab"):
            msm.structure.get_distances(
                geometry,
                selection=[0, 2],
                selection_2=[1, 3],
                pbc=False,
                heavy_mode="force",
            )
