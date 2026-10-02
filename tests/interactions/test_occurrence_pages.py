"""Bound inspection copies independently of retained query and trajectory size."""

import tracemalloc

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError


def parallel(count=50001, *, n_atoms=2, participant_atoms=None):
    atoms = [0, 1] if participant_atoms is None else participant_atoms
    return msm.Interactions(
        n_atoms=n_atoms,
        n_structures=4,
        evaluated_structure_indices=[0, 1, 3],
        relation_types=["compound"],
        relation_participant_offsets=[0, 2],
        participant_roles=["ring", "cation"],
        participant_atom_offsets=[0, len(atoms) - 1, len(atoms)],
        participant_atoms=atoms,
        occurrence_structures=np.zeros(count, dtype=np.int64),
        occurrence_relations=np.zeros(count, dtype=np.int64),
        occurrence_evidence=np.zeros(count, dtype=np.int32),
        evidence_labels=["synthetic"],
        measurements={"distance": np.arange(count, dtype=float)},
        measure_units={"distance": "nm"},
        occurrence_image_offsets=np.arange(count + 1) * 2,
        image_vectors=np.tile([[0, 0, 0], [1, 0, 0]], (count, 1)),
        method="synthetic",
        software={"producer": "1.2"},
        source_id="declared-fixture",
    )


def test_one_row_page_does_not_materialize_selected_occurrences(monkeypatch):
    view = parallel().query(structure_indices=[0])

    def full_projection(self):
        pytest.fail("Paging called a complete public projection")

    monkeypatch.setattr(msm.Interactions, "to_dict", full_projection)
    view.to_page(limit=1)  # Warm argument plan separately from allocation measurement.
    tracemalloc.start()
    page = view.to_page(offset=25000, limit=1)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert peak < 100000
    assert page["total_count"] == 50001
    assert page["next_offset"] == 25001
    assert page["occurrence_indices"].tolist() == [25000]
    assert page["measurements"]["distance"].tolist() == [25000]
    assert page["relation_indices"].tolist() == [0]
    assert page["relation_catalog_indices"].tolist() == [0]
    assert page["participant_roles"] == ("ring", "cation")
    assert page["image_vectors"].tolist() == [[0, 0, 0], [1, 0, 0]]
    assert page["image_offsets"].tolist() == [0, 2]
    assert page["measure_units"] == {"distance": "nm"}
    assert page["evidence"].tolist() == ["synthetic"]
    assert page["software"] == {"producer": "1.2"}
    assert page["method"] == "synthetic"
    assert page["schema"] == "molsysmt.interactions.page@1"


@pytest.mark.parametrize("offset,limit", [(0, 0), (3, 5), (100, 1)])
def test_empty_pages_have_typed_shapes_and_complete_coverage(offset, limit):
    result = parallel(3)
    page = result.to_page(offset=offset, limit=limit)
    assert page["occurrence_indices"].shape == (0,)
    assert page["occurrence_indices"].dtype == np.int64
    assert page["participant_atoms"].shape == (0,)
    assert page["relation_participant_offsets"].tolist() == [0]
    assert page["participant_atom_offsets"].tolist() == [0]
    assert page["image_vectors"].shape == (0, 3)
    assert page["next_offset"] is None
    assert page["total_count"] == 3
    assert page["evaluated_structure_indices"].tolist() == [0, 1, 3]
    assert not page["evaluated_structure_indices"].flags.writeable
    assert np.shares_memory(page["atom_source_indices"], result.atom_source_indices)
    assert result.query(structure_indices=[1]).to_page()[
        "evaluated_structure_indices"
    ].tolist() == [1]
    assert (
        result.query(structure_indices=[2])
        .to_page()["evaluated_structure_indices"]
        .tolist()
        == []
    )


@pytest.mark.parametrize("name", ["offset", "limit", "max_participant_atoms"])
@pytest.mark.parametrize("value", [-1, 1.5, True, np.bool_(False), "1", None])
def test_invalid_page_bounds_are_rejected(name, value):
    with pytest.raises(ArgumentError):
        parallel(1).to_page(**{name: value})


def test_oversized_participant_fails_before_copying_definitions(monkeypatch):
    result = parallel(1, n_atoms=100001, participant_atoms=np.arange(100001))
    import molsysmt.interactions._pages as pages

    def copied(*args, **kwargs):
        pytest.fail("An oversized page copied its relation catalog")

    monkeypatch.setattr(pages, "_catalog", copied)
    monkeypatch.setattr(msm.Interactions, "_occurrence_dict", copied)
    with pytest.raises(ValueError, match="100001 participant atoms"):
        result.to_page(limit=1, max_participant_atoms=1000)


def test_reused_relations_count_toward_each_occurrence_atom_budget():
    result = parallel(3)
    with pytest.raises(ValueError, match="6 participant atoms"):
        result.to_page(limit=3, max_participant_atoms=5)
    assert (
        len(result.to_page(limit=2, max_participant_atoms=4)["occurrence_indices"]) == 2
    )


def test_pages_preserve_nonconsecutive_order_and_round_trip(tmp_path):
    records = []
    for frame, atoms in ((0, [0, 1]), (3, [2, 3, 4]), (3, [2, 3, 4])):
        records.append(
            dict(
                structure_index=frame,
                interaction_type="pair",
                participants=[
                    dict(role="a", atom_indices=atoms[:-1]),
                    dict(role="b", atom_indices=atoms[-1:]),
                ],
            )
        )
    result = msm.Interactions.from_records(
        records,
        n_atoms=5,
        n_structures=5,
        evaluated_structure_indices=[0, 1, 3],
        method="synthetic",
    )
    filename = str(tmp_path / "pages.h5msm")
    msm.h5msm.write_layers(filename, interactions={"synthetic": result})
    loaded = msm.h5msm.read(filename).interactions["synthetic"]
    for source in (result, loaded):
        view = source.query(structure_indices=[3, 1, 0, 3])
        first = view.to_page(limit=1)
        second = view.to_page(offset=first["next_offset"], limit=2)
        assert first["occurrence_indices"].tolist() == [1]
        assert second["occurrence_indices"].tolist() == [2, 0]
        assert second["structure_indices"].tolist() == [3, 0]
        assert second["relation_catalog_indices"].tolist() == [0, 1]
        assert second["participant_atom_offsets"].tolist() == [0, 1, 2, 4, 5]
        assert second["participant_atoms"].tolist() == [0, 1, 2, 3, 4]
        assert second["next_offset"] is None


@pytest.mark.parametrize(
    "edited", ["invalidated", "replaced", "replaced_invalidated", "twice_replaced"]
)
def test_edited_pages_do_not_pack_complete_columns(monkeypatch, edited):
    original = parallel(50001)
    if edited == "invalidated":
        # Invalidating an evaluated-empty frame leaves all observations active.
        source = original.invalidate_structures([1])
    else:
        fresh = msm.Interactions.from_records(
            [
                dict(
                    structure_index=3,
                    interaction_type="new",
                    evidence="new",
                    participants=[
                        dict(role="a", atom_indices=[0]),
                        dict(role="b", atom_indices=[1]),
                    ],
                    measurements={"distance": 7.0},
                    images=[[0, 0, 0], [-1, 0, 0]],
                )
            ],
            n_atoms=2,
            n_structures=4,
            evaluated_structure_indices=[3],
            method=original.method,
            software=original.software,
            source_id=original.source_id,
            measure_units=original.measure_units,
        )
        source = original.replace_structures(fresh)
        if edited == "replaced_invalidated":
            source = source.invalidate_structures([1])
        if edited == "twice_replaced":
            source.to_page(
                limit=1
            )  # Populate any optional page cache before editing again.
            source = source.replace_structures(fresh)
    expected = source.query(structure_indices=[0, 3]).to_dict()

    def pack(self):
        pytest.fail("Paging packed the complete edited analysis")

    monkeypatch.setattr(type(source), "_packed", pack)
    page = source.to_page(offset=50000, limit=2)
    assert (
        page["occurrence_indices"].tolist()
        == expected["occurrence_indices"][50000:50002].tolist()
    )
    assert (
        page["relation_indices"].tolist()
        == expected["relation_indices"][50000:50002].tolist()
    )
    assert (
        page["measurements"]["distance"].tolist()
        == expected["measurements"]["distance"][50000:50002].tolist()
    )
    assert source._packed_result is None


def test_page_offsets_after_removing_occupied_frames_and_editing_again(monkeypatch):
    records = [
        dict(
            structure_index=frame,
            interaction_type="pair",
            participants=[
                dict(role="a", atom_indices=[0]),
                dict(role="b", atom_indices=[1]),
            ],
        )
        for frame in [0, 0, 2, 2, 2, 4]
    ]
    original = msm.Interactions.from_records(
        records,
        n_atoms=2,
        n_structures=6,
        evaluated_structure_indices=[0, 1, 2, 4],
        method="synthetic",
    )
    invalidated = original.invalidate_structures([2])
    assert invalidated.to_page(offset=1, limit=2)["occurrence_indices"].tolist() == [
        1,
        2,
    ]
    # Repeated edits must not reuse an obsolete frame-offset cache.
    invalidated_again = invalidated.invalidate_structures([0])
    assert invalidated_again.to_page(limit=1)["structure_indices"].tolist() == [4]
    fresh = msm.Interactions.from_records(
        records[:1],
        n_atoms=2,
        n_structures=6,
        evaluated_structure_indices=[0],
        method="synthetic",
    )
    patched = original.replace_structures(fresh)
    patched.to_page(limit=1)
    patched_again = patched.replace_structures(fresh).invalidate_structures([2])

    def pack(self):
        pytest.fail("Paging packed edited columns")

    monkeypatch.setattr(type(patched_again), "_packed", pack)
    page = patched_again.to_page(offset=1, limit=2)
    assert page["occurrence_indices"].tolist() == [1]
    assert page["structure_indices"].tolist() == [4]
    assert page["total_count"] == 2
