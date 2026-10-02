#!/usr/bin/env python3
"""Exercise interaction index maps, per-analysis coverage, and local edits.

This plain-record oracle is a design probe, not a public Interactions backend.
Its analysis keys identify method blocks only within the synthetic fixture.
"""

from __future__ import annotations

import copy
import json
from collections import Counter

from benchmark_interactions_contract import UNITS, _signature, materialize

import molsysmt as msm


def _record(
    frame, kind, participants, distance, *, evidence="observed_geometry", image_shift=0
):
    images = [[0, 0, 0] for _ in participants]
    images[0][0] = image_shift
    return {
        "structure_index": frame,
        "interaction_type": kind,
        "participants": [
            {"role": role, "atom_indices": atoms} for role, atoms in participants
        ],
        "evidence": evidence,
        "measurements": {"distance": distance, "angle": -1.0},
        "images": images,
    }


def _unique_map(mapping, limit, label):
    if len(set(mapping)) != len(mapping) or any(
        not isinstance(index, int) or not 0 <= index < limit for index in mapping
    ):
        raise ValueError(f"{label} must contain unique valid source indices")
    return tuple(mapping)


def normalize_analysis(
    *,
    key,
    method,
    atom_map,
    structure_map,
    evaluated_local,
    rows,
    n_atoms,
    n_structures,
):
    """Map local analysis indices to one explicit source index space."""
    atom_map = _unique_map(atom_map, n_atoms, "atom_map")
    structure_map = _unique_map(structure_map, n_structures, "structure_map")
    if len(set(evaluated_local)) != len(evaluated_local) or any(
        not 0 <= index < len(structure_map) for index in evaluated_local
    ):
        raise ValueError("evaluated_local must select unique local structures")
    coverage = [structure_map[index] for index in evaluated_local]
    converted = []
    for row in rows:
        local_frame = row["structure_index"]
        if local_frame not in evaluated_local:
            raise ValueError("a local observation belongs to an unevaluated structure")
        normalized = copy.deepcopy(row)
        normalized["structure_index"] = structure_map[local_frame]
        normalized["analysis_key"] = key
        for participant in normalized["participants"]:
            participant["atom_indices"] = [
                atom_map[index] for index in participant["atom_indices"]
            ]
        converted.append(normalized)
    return {
        "key": key,
        "method": method,
        "parameters": {"synthetic": True},
        "units": dict(UNITS),
        "source_atom_map": list(atom_map),
        "source_structure_map": list(structure_map),
        "coverage": coverage,
        "rows": converted,
    }


def _selected(coverage, requested):
    if requested is None:
        return list(coverage)
    known = set(coverage)
    return [index for index in dict.fromkeys(requested) if index in known]


def _atoms(row):
    return {
        atom
        for participant in row["participants"]
        for atom in participant["atom_indices"]
    }


def query(
    model,
    *,
    structures=None,
    atoms=None,
    mode="incident",
    between=None,
    exclusive=False,
    analyses=None,
):
    """Return per-analysis coverage and source-index records without indexes."""
    if mode not in {"incident", "internal", "cross"}:
        raise ValueError("unknown atom-set mode")
    if between is not None and set(between[0]) & set(between[1]):
        raise ValueError("two-set queries require disjoint atom sets")
    keys = list(model["analyses"]) if analyses is None else list(analyses)
    coverage = {
        key: _selected(model["analyses"][key]["coverage"], structures) for key in keys
    }
    selected = []
    atom_set = None if atoms is None else set(atoms)
    for key in keys:
        block = model["analyses"][key]
        covered = set(coverage[key])
        for row in block["rows"]:
            if row["structure_index"] not in covered:
                continue
            involved = _atoms(row)
            if atom_set is not None:
                incident = bool(involved & atom_set)
                internal = involved <= atom_set
                if not (
                    incident
                    if mode == "incident"
                    else internal
                    if mode == "internal"
                    else incident and not internal
                ):
                    continue
            if between is not None:
                a, b = set(between[0]), set(between[1])
                if not (
                    involved & a
                    and involved & b
                    and (not exclusive or involved <= a | b)
                ):
                    continue
            selected.append(copy.deepcopy(row))
    frame_order = (
        list(dict.fromkeys(structures))
        if structures is not None
        else sorted({frame for frames in coverage.values() for frame in frames})
    )
    frame_rank = {frame: rank for rank, frame in enumerate(frame_order)}
    analysis_rank = {key: rank for rank, key in enumerate(keys)}
    selected.sort(
        key=lambda row: (
            frame_rank[row["structure_index"]],
            analysis_rank[row["analysis_key"]],
            _signature(row),
        )
    )
    return coverage, selected


def replace_incident(
    model, *, analysis_key, structure_index, atom_indices, replacements
):
    """Replace one analysis's affected observations without touching other frames."""
    changed = copy.deepcopy(model)
    block = changed["analyses"][analysis_key]
    if structure_index not in block["coverage"]:
        raise ValueError("replace only an evaluated structure")
    atoms = set(atom_indices)
    block["rows"] = [
        row
        for row in block["rows"]
        if row["structure_index"] != structure_index or not (_atoms(row) & atoms)
    ]
    for replacement in replacements:
        if replacement["structure_index"] != structure_index or any(
            not 0 <= atom < changed["n_atoms"] for atom in _atoms(replacement)
        ):
            raise ValueError("replacement is outside the source index space")
        row = copy.deepcopy(replacement)
        row["analysis_key"] = analysis_key
        block["rows"].append(row)
    return changed


def remove_atoms(model, removed):
    """Prune incident rows and remap surviving positional source atom indices."""
    changed = copy.deepcopy(model)
    removed = set(removed)
    if any(not 0 <= atom < model["n_atoms"] for atom in removed):
        raise ValueError("removed atom is outside the source index space")
    kept = [atom for atom in range(model["n_atoms"]) if atom not in removed]
    old_to_new = {old: new for new, old in enumerate(kept)}
    changed["n_atoms"] = len(kept)
    for block in changed["analyses"].values():
        block["source_atom_map"] = [
            old_to_new.get(atom) for atom in block["source_atom_map"]
        ]
        block["rows"] = [row for row in block["rows"] if not (_atoms(row) & removed)]
        for row in block["rows"]:
            for participant in row["participants"]:
                participant["atom_indices"] = [
                    old_to_new[atom] for atom in participant["atom_indices"]
                ]
    return changed


def reorder_structures(model, retained_old_indices):
    """Remove omitted structures and map retained positional indices in order."""
    changed = copy.deepcopy(model)
    retained = _unique_map(
        retained_old_indices, model["n_structures"], "retained_old_indices"
    )
    old_to_new = {old: new for new, old in enumerate(retained)}
    changed["n_structures"] = len(retained)
    for block in changed["analyses"].values():
        block["source_structure_map"] = [
            old_to_new.get(index) for index in block["source_structure_map"]
        ]
        block["coverage"] = [
            old_to_new[index] for index in block["coverage"] if index in old_to_new
        ]
        block["rows"] = [
            row for row in block["rows"] if row["structure_index"] in old_to_new
        ]
        for row in block["rows"]:
            row["structure_index"] = old_to_new[row["structure_index"]]
    return changed


def append_structure(model, evaluated_analyses=()):
    """Append an empty source structure, evaluated only by named analyses."""
    changed = copy.deepcopy(model)
    index = changed["n_structures"]
    changed["n_structures"] += 1
    for key in evaluated_analyses:
        changed["analyses"][key]["coverage"].append(index)
    return changed


def fixture():
    analysis_a = normalize_analysis(
        key="buch",
        method="buch",
        n_atoms=12,
        n_structures=6,
        atom_map=[3, 1, 5, 0, 2, 4, 6, 7, 8, 9, 10, 11],
        structure_map=[4, 1, 5],
        evaluated_local=[0, 1, 2],
        rows=[
            _record(
                0, "hbond", [("donor", [3]), ("hydrogen", [1]), ("acceptor", [4])], 0.20
            ),
            _record(
                0,
                "hbond",
                [("donor", [3]), ("hydrogen", [1]), ("acceptor", [4])],
                0.21,
                image_shift=1,
            ),
            _record(1, "pi_pi", [("ring", [0, 2, 5]), ("ring", [6, 7, 8])], 0.36),
            _record(
                1,
                "four_body",
                [("site", [3]), ("site", [5]), ("site", [6]), ("site", [9])],
                0.47,
            ),
        ],
    )
    analysis_b = normalize_analysis(
        key="luzard",
        method="luzard_chandler",
        n_atoms=12,
        n_structures=6,
        atom_map=[0, 1, 2, 6, 8, 10],
        structure_map=[4, 5],
        evaluated_local=[0, 1],
        rows=[
            _record(
                0, "hbond", [("donor", [0]), ("hydrogen", [1]), ("acceptor", [2])], 0.22
            ),
            _record(
                1,
                "declared_disulfide",
                [("sulfur", [3]), ("sulfur", [4])],
                0.19,
                evidence="declared_topology",
            ),
        ],
    )
    return {
        "n_atoms": 12,
        "n_structures": 6,
        "analyses": {"buch": analysis_a, "luzard": analysis_b},
    }


def _check_class_projection(model, key):
    """Check the current class after caller-side remapping of one analysis."""
    block = model["analyses"][key]
    mapped = msm.Interactions.from_records(
        [],
        n_atoms=len(block["source_atom_map"]),
        n_structures=len(block["source_structure_map"]),
        evaluated_structure_indices=[],
        method=block["method"],
        atom_source_indices=block["source_atom_map"],
        structure_source_indices=block["source_structure_map"],
        source_n_atoms=model["n_atoms"],
        source_n_structures=model["n_structures"],
    )
    assert mapped.atom_source_indices.tolist() == block["source_atom_map"]
    assert mapped.structure_source_indices.tolist() == block["source_structure_map"]
    result = msm.Interactions.from_records(
        block["rows"],
        n_atoms=model["n_atoms"],
        n_structures=model["n_structures"],
        evaluated_structure_indices=block["coverage"],
        method=block["method"],
        measure_units=block["units"],
        parameters=block["parameters"],
    )
    specs = (
        {"structures": [5, 4, 5, 1]},
        {"structures": [4], "atoms": [0], "mode": "incident"},
        {"structures": [4], "atoms": [0, 1, 2], "mode": "internal"},
        {"structures": [1], "atoms": [3], "mode": "cross"},
    )
    for spec in specs:
        expected_coverage, expected_rows = query(model, analyses=[key], **spec)
        actual = materialize(
            result.query(
                structure_indices=spec.get("structures"),
                atom_indices=spec.get("atoms"),
                mode=spec.get("mode", "incident"),
            )
        )
        if actual != (
            expected_coverage[key],
            Counter(_signature(row) for row in expected_rows),
        ):
            raise AssertionError(f"class projection differs from oracle: {key}, {spec}")
    return len(specs)


def main():
    model = fixture()
    original = copy.deepcopy(model)
    coverage, rows = query(model, structures=[5, 4, 5, 1])
    assert coverage == {"buch": [5, 4, 1], "luzard": [5, 4]}
    assert Counter(row["structure_index"] for row in rows) == {4: 3, 1: 2, 5: 1}
    assert [row["structure_index"] for row in rows] == [5, 4, 4, 4, 1, 1]
    assert len(query(model, structures=[4], atoms=[0, 1, 2], mode="internal")[1]) == 3
    assert len(query(model, structures=[1], atoms=[3], mode="cross")[1]) == 1
    assert (
        len(query(model, structures=[4], between=([0, 1], [2]), exclusive=True)[1]) == 3
    )
    class_checks = sum(_check_class_projection(model, key) for key in model["analyses"])

    replacement = _record(
        4, "hbond", [("donor", [10]), ("hydrogen", [1]), ("acceptor", [2])], 0.24
    )
    edited = replace_incident(
        model,
        analysis_key="buch",
        structure_index=4,
        atom_indices=[2],
        replacements=[replacement],
    )
    edited = replace_incident(
        edited,
        analysis_key="luzard",
        structure_index=4,
        atom_indices=[2],
        replacements=[replacement],
    )
    edited_hits = query(edited, structures=[4], atoms=[2])[1]
    assert len(edited_hits) == 2 and all(10 in _atoms(row) for row in edited_hits)
    assert len(query(edited, structures=[4], atoms=[10])[1]) == 2
    assert query(edited, structures=[5])[0] == {"buch": [5], "luzard": [5]}
    assert model == original

    pruned = remove_atoms(edited, [6])
    assert pruned["n_atoms"] == 11
    assert len(query(pruned, structures=[1, 5])[1]) == 0
    assert len(query(pruned, structures=[4], atoms=[9])[1]) == 2
    assert pruned["analyses"]["buch"]["source_atom_map"][6] is None

    reordered = reorder_structures(pruned, [5, 4, 1, 0, 2])
    appended = append_structure(reordered, evaluated_analyses=["buch"])
    assert appended["n_structures"] == 6
    assert query(appended, structures=[5, 0, 1, 5])[0] == {
        "buch": [5, 0, 1],
        "luzard": [0, 1],
    }
    assert len(query(appended, structures=[1], atoms=[9])[1]) == 2
    assert len(query(appended, structures=[5])[1]) == 0
    print(
        json.dumps(
            {
                "analyses": list(model["analyses"]),
                "original_coverage": coverage,
                "original_rows": len(rows),
                "class_projection_checks": class_checks,
                "rows_after_ligand_replacement": sum(
                    len(block["rows"]) for block in edited["analyses"].values()
                ),
                "rows_after_atom_removal": sum(
                    len(block["rows"]) for block in pruned["analyses"].values()
                ),
                "final_coverage": query(appended, structures=[5, 0, 1, 5])[0],
                "final_atom_count": appended["n_atoms"],
                "final_structure_count": appended["n_structures"],
                "public_class_supports_combined_analyses": False,
                "public_class_stores_source_maps": True,
                "public_class_has_edit_methods": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
