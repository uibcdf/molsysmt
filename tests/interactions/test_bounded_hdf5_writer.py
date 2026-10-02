"""Protect bounded active-column persistence and unchanged codec semantics."""

import gc
import tracemalloc

import h5py
import numpy as np
import pytest

import molsysmt as msm
from molsysmt.interactions import _hdf5_writer
from molsysmt.interactions._frame_replacement import _FramePatchedInteractions
from molsysmt.interactions._frame_validity import _FrameFilteredInteractions
from molsysmt.interactions._hdf5_query import query_named_interactions_file
from molsysmt.native import MolSys

from . import test_frame_validity
from .test_frame_validity import record

complex_result = test_frame_validity.result


def _replacement(original):
    return msm.Interactions.from_records(
        [
            record(
                2,
                0.6,
                kind="compound",
                participants=[
                    {"role": "group", "atom_indices": [1, 3, 4]},
                    {"role": "group", "atom_indices": [5, 6]},
                ],
                images=[[0, 0, 0], [-1, 2, 0]],
            ),
            record(3, 0.7, images=[[0, 0, 0], [1, 0, 0], [0, 2, 0]]),
            record(3, 0.8, images=[[0, 0, 0], [-1, 0, 0], [0, -2, 0]]),
        ],
        n_atoms=original.n_atoms,
        n_structures=original.n_structures,
        evaluated_structure_indices=[1, 2, 3],
        method=original.method,
        parameters=original.parameters,
        measure_units=original.measure_units,
        source_id=original.source_id,
        software=original.software,
        atom_source_indices=original.atom_source_indices,
        source_n_atoms=original.source_n_atoms,
        structure_source_indices=original.structure_source_indices,
        source_n_structures=original.source_n_structures,
        execution={"execution": "eager", "execution_chunks": 1},
    )


def _assert_same(original, restored):
    expected, actual = (
        original.query(structure_indices=[4, 2, 3, 1, 0]).to_dict(),
        restored.query(structure_indices=[4, 2, 3, 1, 0]).to_dict(),
    )
    for name in (
        "evaluated_structure_indices",
        "occurrence_indices",
        "structure_indices",
        "relation_indices",
        "evidence",
        "image_offsets",
        "image_vectors",
    ):
        np.testing.assert_array_equal(actual[name], expected[name])
    for name in expected["measurements"]:
        np.testing.assert_allclose(
            actual["measurements"][name], expected["measurements"][name]
        )
    for name in (
        "participant_atoms",
        "participant_atom_offsets",
        "relation_participant_offsets",
        "atom_source_indices",
        "structure_source_indices",
    ):
        np.testing.assert_array_equal(getattr(restored, name), getattr(original, name))
    for name in (
        "relation_types",
        "participant_roles",
        "parameters",
        "software",
        "source_id",
        "measure_units",
    ):
        assert getattr(restored, name) == getattr(original, name)
    assert [
        (row["structure_indices"].tolist(), row["details"])
        for row in restored.execution_records
    ] == [
        (row["structure_indices"].tolist(), row["details"])
        for row in original.execution_records
    ]


@pytest.mark.parametrize(
    "kind", ["packed", "filtered", "patched", "patched_filtered", "empty"]
)
@pytest.mark.parametrize("cached", [False, True])
def test_all_public_writers_preserve_semantics_without_packing(
    complex_result, kind, cached, tmp_path, monkeypatch
):
    original = complex_result
    if kind != "packed":
        original = original.invalidate_structures([0])
    if kind in {"patched", "patched_filtered"}:
        original = original.replace_structures(_replacement(complex_result))
    if kind == "patched_filtered":
        original = original.invalidate_structures([3])
    if kind == "empty":
        original = original.invalidate_structures([2, 4])
    if cached and hasattr(original, "_packed_result"):
        original.occurrence_structures
    cached_result = getattr(original, "_packed_result", None)

    def forbidden(*args, **kwargs):
        raise AssertionError(
            "HDF5 writing must not materialize complete active columns"
        )

    monkeypatch.setattr(_FrameFilteredInteractions, "_packed", forbidden)
    monkeypatch.setattr(_FramePatchedInteractions, "_packed", forbidden)
    monkeypatch.setattr(_hdf5_writer, "_WINDOW_BYTES", 16)
    writes = []
    setitem = h5py.Dataset.__setitem__

    def bounded_write(dataset, selection, value):
        if dataset.dtype.kind in "biuf":
            writes.append(np.asarray(value).nbytes)
            assert writes[-1] <= 16
        return setitem(dataset, selection, value)

    monkeypatch.setattr(h5py.Dataset, "__setitem__", bounded_write)
    standalone, layered, converted = [
        tmp_path / name for name in ("result.h5i", "layers.h5msm", "system.h5msm")
    ]
    original.save(standalone)
    msm.h5msm.write_layers(
        layered, interactions={"first": original, "second": original}
    )
    molsys = MolSys._from_partial_domains(interactions={"analysis": original})
    msm.convert(molsys, to_form="file:h5msm", output_filename=converted)
    assert writes
    assert getattr(original, "_packed_result", None) is cached_result
    candidates = [
        msm.Interactions.load(standalone),
        msm.h5msm.read_layers(layered, layers="interactions")["interactions"]["second"],
        msm.convert(converted, to_form="molsysmt.MolSys").interactions["analysis"],
    ]
    for candidate in candidates:
        _assert_same(original, candidate)
    projection = query_named_interactions_file(converted, "analysis", [4, 2, 3, 1, 0])
    expected = original.query(structure_indices=[4, 2, 3, 1, 0]).to_dict()
    for name in ("occurrence_indices", "evidence", "image_offsets", "image_vectors"):
        np.testing.assert_array_equal(projection[name], expected[name])


def _dense(count, images):
    frames = np.repeat([0, 2], count // 2)
    return msm.Interactions(
        n_atoms=4,
        n_structures=3,
        evaluated_structure_indices=[0, 1, 2],
        relation_types=("pair",),
        relation_participant_offsets=[0, 2],
        participant_roles=("a", "b"),
        participant_atom_offsets=[0, 1, 2],
        participant_atoms=[0, 1],
        occurrence_structures=frames,
        occurrence_relations=np.zeros(count, dtype=np.int64),
        occurrence_evidence=np.zeros(count, dtype=np.int32),
        evidence_labels=("synthetic",),
        measurements={
            "distance": np.full(count, 0.2),
            "occurrence_structures": np.arange(count, dtype=float),
        },
        measure_units={"distance": "nm", "occurrence_structures": "dimensionless"},
        method="memory-test",
        occurrence_image_offsets=np.arange(count + 1) * 2 if images else None,
        image_vectors=np.zeros((count * 2, 3), dtype=np.int32) if images else None,
    )


@pytest.mark.parametrize("patched", [False, True])
@pytest.mark.parametrize("images", [False, True])
def test_dense_single_frame_write_allocations_do_not_grow_with_occurrence_count(
    patched, images, tmp_path, monkeypatch
):
    monkeypatch.setattr(_hdf5_writer, "_WINDOW_BYTES", 16 * 1024)
    peaks = []
    for count in (20_000, 300_000):
        original = _dense(count, images).invalidate_structures([0])
        if patched:
            fresh = _dense(2, images).invalidate_structures([1, 2])
            original = original.replace_structures(fresh)
        gc.collect()
        tracemalloc.start()
        try:
            original.save(tmp_path / f"{count}.h5i")
            peaks.append(tracemalloc.get_traced_memory()[1])
        finally:
            tracemalloc.stop()
        assert original._packed_result is None
        assert original.n_interactions == count // 2 + int(patched)
        with h5py.File(tmp_path / f"{count}.h5i", "r") as file:
            assert file["occurrence_structures"].shape == (original.n_interactions,)
            assert file["measurements/occurrence_structures"][-1] == count - 1
    assert max(peaks) < 1_000_000
    assert peaks[1] < peaks[0] + 200_000


def test_measurement_names_cannot_overwrite_structural_columns(tmp_path):
    analysis = _dense(10, False)
    path = tmp_path / "names.h5i"
    analysis.save(path)
    restored = msm.Interactions.load(path)
    np.testing.assert_array_equal(restored.occurrence_structures, [0] * 5 + [2] * 5)
    np.testing.assert_array_equal(
        restored.measurements["occurrence_structures"], np.arange(10)
    )
