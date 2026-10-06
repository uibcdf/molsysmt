"""Frame selection must bound relation tests before scanning trajectory chemistry."""

import numpy as np
import pytest

import molsysmt as msm


@pytest.mark.parametrize(
    "mode", ["involving_selection", "within_selection", "across_selection_boundary"]
)
@pytest.mark.parametrize("frames", [0, [4, 1, 0, 4, 3]])
@pytest.mark.parametrize("reused", [False, True])
def test_frame_queries_inspect_only_relevant_relations(
    monkeypatch, mode, frames, reused
):
    records = []
    for frame in range(100):
        if frame in (1, 3):
            continue
        atoms = [0, 1, 2] if reused else [0, frame + 1, frame + 2]
        records.append(
            dict(
                structure_index=frame,
                interaction_type="compound",
                participants=[
                    dict(role="ring", atom_indices=atoms[:2]),
                    dict(role="cation", atom_indices=atoms[2:]),
                ],
            )
        )
    records.insert(1, records[0].copy())  # Parallel observations are distinct rows.
    result = msm.Interactions.from_records(
        records,
        n_atoms=102,
        n_structures=101,
        evaluated_structure_indices=np.arange(100),
        method="synthetic",
    )
    requested = list(dict.fromkeys(np.asarray(frames).reshape(-1).tolist()))
    selection = {0, 1, 2}
    expected = []
    for frame in requested:
        for index, record in enumerate(records):
            atoms = {
                atom
                for participant in record["participants"]
                for atom in participant["atom_indices"]
            }
            matches = (
                bool(atoms & selection)
                if mode == "involving_selection"
                else atoms <= selection
                if mode == "within_selection"
                else bool(atoms & selection) and not atoms <= selection
            )
            if record["structure_index"] == frame and matches:
                expected.append(index)
    # Construction sorts occurrences by frame; use its stable sorted row mapping.
    row_map = np.argsort(
        [record["structure_index"] for record in records], kind="stable"
    )
    inverse = np.argsort(row_map)
    candidates = result.query(structure_indices=frames)
    relevant = set(result.occurrence_relations[candidates._positions])
    inspected = []
    relation_atoms = msm.Interactions._relation_atoms

    def bounded(self, index):
        assert index in relevant, "An unrelated frame's relation was inspected"
        inspected.append(index)
        return relation_atoms(self, index)

    def unnecessary_index(self):
        pytest.fail("A frame query built whole-trajectory atom postings")

    monkeypatch.setattr(msm.Interactions, "_relation_atoms", bounded)
    monkeypatch.setattr(msm.Interactions, "_build_indexes", unnecessary_index)
    selected = result.query(
        structure_indices=frames,
        atom_indices=list(selection),
        mode=mode,
        interaction_types="compound",
    )
    np.testing.assert_array_equal(
        selected.to_dict()["occurrence_indices"], inverse[expected]
    )
    assert len(inspected) <= len(relevant)
    # Chained views must intersect rather than reintroduce omitted occurrences.
    chained = candidates.query(
        structure_indices=frames, atom_indices=list(selection), mode=mode
    )
    np.testing.assert_array_equal(
        chained.to_dict()["occurrence_indices"], inverse[expected]
    )
