"""Qualifying immutable row compaction, identities and storage release."""

import gc
import pickle
import tracemalloc
import weakref

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from molsysmt.interactions import _hdf5_writer
from molsysmt.interactions._frame_replacement import _FramePatchedInteractions
from molsysmt.interactions._frame_validity import _FrameFilteredInteractions
from molsysmt.native import MolSys

from . import test_frame_validity
from .test_bounded_hdf5_writer import _assert_same, _dense, _replacement

complex_result = test_frame_validity.result


@pytest.mark.parametrize(
    "kind", ["packed", "filtered", "patched", "patched_filtered", "empty"]
)
@pytest.mark.parametrize("cached", [False, True])
def test_compaction_preserves_full_queries_and_codecs(
    complex_result, kind, cached, monkeypatch, tmp_path
):
    source = complex_result
    if kind != "packed":
        source = source.invalidate_structures([0])
    if kind in {"patched", "patched_filtered"}:
        source = source.replace_structures(_replacement(complex_result))
    if kind == "patched_filtered":
        source = source.invalidate_structures([3])
    if kind == "empty":
        source = source.invalidate_structures([2, 4])
    old_view = source.query(structure_indices=[4, 2, 4])
    expected_view = old_view.to_dict()
    if cached and hasattr(source, "_packed_result"):
        source.occurrence_structures
    cache = getattr(source, "_packed_result", None)

    def forbidden(*args, **kwargs):
        raise AssertionError("Compaction must not pack through a whole-result query")

    monkeypatch.setattr(_FrameFilteredInteractions, "_packed", forbidden)
    monkeypatch.setattr(_FramePatchedInteractions, "_packed", forbidden)
    monkeypatch.setattr(_hdf5_writer, "_WINDOW_BYTES", 16)
    compacted = source.compact()
    assert type(compacted) is msm.Interactions
    assert compacted is not source
    assert getattr(source, "_packed_result", None) is cache
    assert not {
        "_root",
        "_segments",
        "_packed_result",
        "_public_occurrence_indices",
    }.intersection(vars(compacted))
    _assert_same(source, compacted)
    for mode in ("internal", "incident", "cross"):
        for key in (
            "structure_indices",
            "relation_indices",
            "occurrence_indices",
            "image_vectors",
        ):
            np.testing.assert_array_equal(
                source.query(atom_indices=[0, 3], mode=mode).to_dict()[key],
                compacted.query(atom_indices=[0, 3], mode=mode).to_dict()[key],
            )
    np.testing.assert_array_equal(
        source.between([0, 1], [2]).to_dict()["occurrence_indices"],
        compacted.between([0, 1], [2]).to_dict()["occurrence_indices"],
    )
    for key in ("occurrence_indices", "image_vectors"):
        np.testing.assert_array_equal(old_view.to_dict()[key], expected_view[key])
    for array in (
        compacted.occurrence_structures,
        compacted._positions,
        compacted.image_vectors,
        *compacted.measurements.values(),
    ):
        if array is not None:
            with pytest.raises(ValueError):
                array.setflags(write=True)
    standalone = tmp_path / "compact.h5i"
    compacted.save(standalone)
    molecular_file = tmp_path / "compact.h5msm"
    molsys = MolSys._from_partial_domains(interactions={"analysis": compacted})
    msm.convert(molsys, to_form="file:h5msm", output_filename=molecular_file)
    converted = msm.convert(compacted, to_form="molsysmt.InteractionsDict")
    candidates = [
        msm.Interactions.load(standalone),
        pickle.loads(pickle.dumps(compacted)),
        msm.convert(converted, to_form="molsysmt.Interactions"),
        msm.convert(molecular_file, to_form="molsysmt.MolSys").interactions["analysis"],
    ]
    for candidate in candidates:
        _assert_same(compacted, candidate)


@pytest.mark.parametrize("patched", [False, True])
@pytest.mark.parametrize("keep_view", [False, True])
def test_releasing_old_snapshots_frees_retired_source_buffers(patched, keep_view):
    base = _dense(100, True)
    view = base.query(structure_indices=[0]) if keep_view else None
    source = base.invalidate_structures([0])
    refs = [
        weakref.ref(base),
        weakref.ref(base.occurrence_structures),
        weakref.ref(base.image_vectors),
    ]
    if patched:
        incoming = _dense(2, True).invalidate_structures([1, 2])
        source = source.replace_structures(incoming)
        del incoming
    compacted = source.compact()
    del base, source
    gc.collect()
    if keep_view:
        assert all(reference() is not None for reference in refs[1:])
        assert view.n_interactions == 50
        del view
        gc.collect()
    assert all(reference() is None for reference in refs)
    assert compacted.n_interactions == 50 + int(patched)
    assert compacted.measurements["occurrence_structures"][-1] == 99


@pytest.mark.parametrize("images", [False, True])
def test_compaction_peak_is_output_plus_one_column_workspace(images, monkeypatch):
    monkeypatch.setattr(_hdf5_writer, "_WINDOW_BYTES", 16 * 1024)
    source = _dense(300_000, images).invalidate_structures([0])
    source = source.replace_structures(_dense(2, images).invalidate_structures([1, 2]))
    gc.collect()
    tracemalloc.start()
    try:
        compacted = source.compact()
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    assert compacted.n_interactions == 150_001
    assert compacted.measurements["occurrence_structures"][-1] == 299_999
    largest = max(
        array.nbytes
        for array in (
            compacted.occurrence_structures,
            compacted.image_vectors if images else compacted._positions,
        )
    )
    assert peak < compacted.numeric_nbytes + largest + 500_000
    assert compacted.numeric_nbytes < source.numeric_nbytes
    assert source._packed_result is None


def test_compaction_rejects_query_views_and_validates_skip_flag(complex_result):
    with pytest.raises(ValueError, match="full"):
        complex_result.query(structure_indices=[2]).compact()
    with pytest.raises(ArgumentError):
        complex_result.compact(skip_digestion="yes")
    assert complex_result.compact(skip_digestion=True).n_interactions == 4


def test_compaction_translates_evidence_and_keeps_four_body_images():
    def build(frame, evidence):
        return msm.Interactions.from_records(
            [
                dict(
                    structure_index=frame,
                    interaction_type="four_body",
                    participants=[
                        dict(role=f"role_{index}", atom_indices=[index])
                        for index in range(4)
                    ],
                    evidence=evidence,
                    images=[[0, 0, 0], [1, 0, 0], [0, 2, 0], [0, 0, -3]],
                )
            ],
            n_atoms=4,
            n_structures=3,
            evaluated_structure_indices=[frame],
            method="synthetic",
        )

    old = build(0, "first")
    source = old.replace_structures(build(2, "second"))
    compacted = source.compact()
    data = compacted.query(structure_indices=[2, 0, 1]).to_dict()
    np.testing.assert_array_equal(data["evidence"], ["second", "first"])
    np.testing.assert_array_equal(data["image_offsets"], [0, 4, 8])
    np.testing.assert_array_equal(
        data["image_vectors"], [[0, 0, 0], [1, 0, 0], [0, 2, 0], [0, 0, -3]] * 2
    )
    np.testing.assert_array_equal(data["occurrence_indices"], [1, 0])
    assert compacted.between([0, 1], [2, 3], exclusive=True).n_interactions == 2
