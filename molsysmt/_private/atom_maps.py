"""Normalize and compose sparse partial atom correspondences on declared axes."""

from copy import deepcopy

import numpy as np

from molsysmt._private.smonitor import (
    ArgumentError,
    FormatError,
    StructuralInconsistencyError,
)

CALLER = "molsysmt.form.compose_atom_maps"
SCHEMA = "molsysmt.atom_map@1"
_DIRECT = {SCHEMA, "molsysmt.atom_projection@1", "molsysmt.atom_export@1"}
_CREATION = {"molsysmt.terminal_attachment@1", "molsysmt.hydrogen_addition@1"}
_LABELS = (
    "source_atom_ids",
    "source_atom_names",
    "output_atom_ids",
    "output_atom_names",
)
_METADATA = (
    "method",
    "engine",
    "parameters",
    "coordinate_evidence",
    "coordinate_unit",
    "operation",
    "software",
    "references",
    "attribution",
    "typing_scheme",
    "chemical_state_index",
    "chemical_state_id",
    "source_chemical_digest",
    "input_axis",
    "input_export_sha256",
    "output_payload_sha256",
    "origin_schema",
    "torsion_tree",
    "ordered_root_source_atom_indices",
    "first_root_source_atom_index",
    "branch_source_atom_pairs",
    "source_structure_indices",
    "structure_indices",
    "input_structure_indices",
)
_CHARGE_SCALARS = (
    "source_total_charge",
    "selected_total_charge",
    "output_total_charge",
    "charge_conservation_tolerance",
    "total_charge_before_rounding",
    "written_total_charge",
    "charge_rounding_error_bound",
)


def fail(reason):
    raise StructuralInconsistencyError(reason=reason, caller=CALLER)


def count(value, field):
    if (
        isinstance(value, (bool, np.bool_))
        or not isinstance(value, (int, np.integer))
        or not 0 <= value <= np.iinfo(np.int64).max
    ):
        fail(f"{field} must be a nonnegative integer count.")
    return int(value)


def array(value, field, dtype=None):
    if hasattr(value, "unit") or hasattr(value, "units"):
        fail(
            f"{field} requires serialized numbers/indices, not a quantity with an additional unit."
        )
    try:
        return np.asarray(value, dtype=dtype)
    except (TypeError, ValueError, OverflowError) as error:
        fail(f"{field} is not a rectangular typed array: {error}.")


def integers(value, field, shape):
    values = array(value, field)
    if values.size == 0 and 0 in shape and values.shape in {(0,), shape}:
        return np.empty(shape, dtype=np.int64)
    if (
        values.shape != shape
        or values.dtype.kind not in "iu"
        or np.any(values > np.iinfo(np.int64).max)
    ):
        fail(f"{field} must have integer shape {shape}.")
    return values.astype(np.int64, copy=True)


def pairs(value, field):
    values = array(value, field)
    if values.size == 0:
        return integers(value, field, (0, 2))
    if values.ndim != 2 or values.shape[1] != 2:
        fail(f"{field} requires two index columns.")
    return integers(value, field, values.shape)


def rooted_metadata(stage):
    """Restore the existing PDBQT tree codec on this stage's output atom axis."""
    tree = stage.get("torsion_tree")
    if tree is None:
        if "ordered_root_source_atom_indices" in stage:
            stage["ordered_root_source_atom_indices"] = integers(
                stage["ordered_root_source_atom_indices"],
                "ordered_root_source_atom_indices",
                (0,),
            )
        if "branch_source_atom_pairs" in stage:
            stage["branch_source_atom_pairs"] = integers(
                stage["branch_source_atom_pairs"], "branch_source_atom_pairs", (0, 2)
            )
        if stage.get("first_root_source_atom_index") is not None:
            fail("A ROOT origin requires a declared torsion tree.")
        return
    if not isinstance(tree, dict):
        fail("torsion_tree must be a typed record or None.")
    from molsysmt._private.pdbqt_writer import validate_tree

    n_output = stage["n_output_atoms"]
    tree = deepcopy(tree)
    ids = array(tree.get("atom_ids"), "torsion_tree.atom_ids", dtype=object)
    if ids.shape != (n_output,) or any(not isinstance(value, str) for value in ids):
        fail("torsion_tree atom IDs must be aligned string labels.")
    tree["atom_ids"] = ids
    tree["fragment_atom_indices"] = integers(
        tree.get("fragment_atom_indices"),
        "torsion_tree.fragment_atom_indices",
        (n_output,),
    )
    offsets = array(tree.get("fragment_offsets"), "torsion_tree.fragment_offsets")
    if offsets.ndim != 1:
        fail("torsion_tree.fragment_offsets must be one-dimensional.")
    tree["fragment_offsets"] = integers(
        offsets, "torsion_tree.fragment_offsets", offsets.shape
    )
    for field in ("branch_atom_pairs", "branch_fragment_pairs"):
        tree[field] = pairs(tree.get(field), "torsion_tree." + field)
    try:
        validate_tree(tree, stage.get("output_atom_ids", ids))
    except FormatError as error:
        fail(f"Invalid declared torsion_tree: {error}")
    stage["torsion_tree"] = tree
    inverse = stage["output_to_source_atom_indices"]
    root = inverse[tree["fragment_atom_indices"][: tree["fragment_offsets"][1]]]
    expected = dict(
        ordered_root_source_atom_indices=root,
        first_root_source_atom_index=int(root[0]),
        branch_source_atom_pairs=inverse[tree["branch_atom_pairs"]],
    )
    for field, value in expected.items():
        if field in stage:
            declared = (
                count(stage[field], field)
                if field == "first_root_source_atom_index"
                else integers(stage[field], field, value.shape)
            )
            if not np.array_equal(declared, value):
                fail(f"Rooted export metadata disagrees with the stage map: {field}.")
            stage[field] = value.copy() if isinstance(value, np.ndarray) else value


def direct(raw):
    n_source = count(raw.get("n_source_atoms"), "n_source_atoms")
    n_output = count(raw.get("n_output_atoms"), "n_output_atoms")
    forward = integers(
        raw.get("source_to_output_atom_indices"),
        "source_to_output_atom_indices",
        (n_source,),
    )
    inverse = integers(
        raw.get("output_to_source_atom_indices"),
        "output_to_source_atom_indices",
        (n_output,),
    )
    if (
        np.any(forward < -1)
        or np.any(forward >= n_output)
        or np.any(inverse < -1)
        or np.any(inverse >= n_source)
    ):
        fail("Direct map indices must be -1 or within the declared opposite axis.")
    kept_source = np.flatnonzero(forward >= 0)
    kept_output = np.flatnonzero(inverse >= 0)
    if not np.array_equal(
        inverse[forward[kept_source]], kept_source
    ) or not np.array_equal(forward[inverse[kept_output]], kept_output):
        fail("Direct atom-map directions are not inverse partial correspondences.")
    representatives = integers(
        raw.get("source_to_representative_atom_indices", forward),
        "source_to_representative_atom_indices",
        (n_source,),
    )
    if (
        np.any(representatives < -1)
        or np.any(representatives >= n_output)
        or not np.array_equal(representatives[kept_source], forward[kept_source])
    ):
        fail(
            "Representative indices must agree with directly retained atoms and remain in bounds."
        )
    stage = dict(
        schema=SCHEMA,
        origin_schema=raw.get("origin_schema", raw["schema"]),
        n_source_atoms=n_source,
        n_output_atoms=n_output,
        source_to_output_atom_indices=forward,
        output_to_source_atom_indices=inverse,
        source_to_representative_atom_indices=representatives,
    )
    for name in _LABELS:
        if name in raw:
            labels = array(raw[name], name, dtype=object)
            size = n_source if name.startswith("source") else n_output
            if labels.shape != (size,) or any(
                value is not None and not isinstance(value, str) for value in labels
            ):
                fail(f"{name} requires one string or None label per declared atom.")
            stage[name] = labels.copy()
    for name in _METADATA:
        if name in raw:
            stage[name] = deepcopy(raw[name])
    rooted_metadata(stage)
    for name in ("selected_atom_indices", "renamed_atom_indices"):
        if name in raw:
            values = array(raw[name], name)
            if values.ndim != 1:
                fail(f"{name} must have one index axis.")
            values = integers(raw[name], name, values.shape)
            if (
                np.any(values < 0)
                or np.any(values >= n_source)
                or len(np.unique(values)) != len(values)
            ):
                fail(
                    f"{name} must contain unique indices within the stage source axis."
                )
            stage[name] = values
    if "renamed_atom_indices" in stage and "selected_atom_indices" in stage:
        if not np.isin(
            stage["renamed_atom_indices"], stage["selected_atom_indices"]
        ).all():
            fail("Renamed atom indices must belong to the stage's selected atom scope.")
    if any(name in raw for name in _CHARGE_SCALARS):
        if raw.get("charge_unit") != "elementary_charge":
            fail(
                "Charge totals and precision bounds require explicit elementary_charge units."
            )
        stage["charge_unit"] = "elementary_charge"
        for name in _CHARGE_SCALARS:
            if name not in raw:
                continue
            value = raw[name]
            if (
                isinstance(value, (bool, np.bool_))
                or not isinstance(value, (int, float, np.integer, np.floating))
                or not np.isfinite(value)
            ):
                fail(f"{name} must be a finite scalar charge value.")
            if ("tolerance" in name or "bound" in name) and value < 0:
                fail(f"{name} must be nonnegative.")
            stage[name] = float(value)
        if "charge_decimal_places" in raw:
            stage["charge_decimal_places"] = count(
                raw["charge_decimal_places"], "charge_decimal_places"
            )
    return stage


def creation(raw):
    source = raw.get("source")
    if not isinstance(source, dict):
        fail("A creation report requires its original source counts.")
    n_source = count(source.get("n_atoms"), "source.n_atoms")
    field = (
        "parent_hydrogen_pairs"
        if raw["schema"] == "molsysmt.hydrogen_addition@1"
        else "parent_atom_pairs"
    )
    parents = pairs(raw.get(field), field)
    n_output = n_source + len(parents)
    correspondence = integers(
        raw.get("atom_correspondence"), "atom_correspondence", (n_source, 2)
    )
    if (
        not np.array_equal(np.sort(correspondence[:, 0]), np.arange(n_source))
        or np.any(correspondence[:, 1] < 0)
        or np.any(correspondence[:, 1] >= n_output)
        or len(np.unique(correspondence[:, 1])) != n_source
    ):
        fail("Creation correspondence must retain each original atom exactly once.")
    generated = np.setdiff1d(np.arange(n_output), correspondence[:, 1])
    if (
        np.any(parents[:, 0] < 0)
        or np.any(parents[:, 0] >= n_source)
        or not np.array_equal(np.sort(parents[:, 1]), generated)
    ):
        fail(
            "Creation parent pairs must link existing source parents to every new output atom exactly once."
        )
    forward, inverse = (
        np.empty(n_source, dtype=np.int64),
        np.full(n_output, -1, dtype=np.int64),
    )
    forward[correspondence[:, 0]] = correspondence[:, 1]
    inverse[correspondence[:, 1]] = correspondence[:, 0]
    stage = direct(
        dict(
            raw,
            n_source_atoms=n_source,
            n_output_atoms=n_output,
            source_to_output_atom_indices=forward,
            output_to_source_atom_indices=inverse,
        )
    )
    stage["parent_atom_pairs"] = parents
    if "generated_atom_ids" in raw:
        labels = raw["generated_atom_ids"]
        if (
            not isinstance(labels, (list, tuple, np.ndarray))
            or len(labels) != len(parents)
            or any(not isinstance(label, str) for label in labels)
        ):
            fail(
                "Generated atom IDs must be aligned string labels, not source indices."
            )
        stage["generated_atom_ids"] = deepcopy(labels)
    return stage


def pose(raw):
    # Reader source indices refer to the known molecular graph. Its sequential
    # input for this tool is instead the writer's actual PDBQT line-order axis.
    known = direct(raw)
    exported = raw.get("export_map")
    if (
        not isinstance(exported, dict)
        or exported.get("schema") != "molsysmt.atom_export@1"
    ):
        fail("A pose report requires the completed export_map it validated.")
    writer = direct(exported)
    if np.any(writer["output_to_source_atom_indices"] < 0):
        fail("An export map cannot invent output atoms absent from its source.")
    n_written, n_output = writer["n_output_atoms"], known["n_output_atoms"]
    written_to_output = integers(
        raw.get("pdbqt_to_output_atom_indices"),
        "pdbqt_to_output_atom_indices",
        (n_written,),
    )
    if (
        writer["n_source_atoms"] != known["n_source_atoms"]
        or n_written != n_output
        or not np.array_equal(np.sort(written_to_output), np.arange(n_output))
    ):
        fail(
            "Pose written/native axes must be complete permutations of the same exported atoms."
        )
    if not np.array_equal(
        known["source_to_output_atom_indices"][writer["output_to_source_atom_indices"]],
        written_to_output,
    ):
        fail(
            "Pose written-to-native map disagrees with the known-source/export correspondences."
        )
    inverse = np.argsort(written_to_output)
    adapted = dict(
        schema=raw["schema"],
        n_source_atoms=n_written,
        n_output_atoms=n_output,
        source_to_output_atom_indices=written_to_output,
        output_to_source_atom_indices=inverse,
        input_axis="pdbqt_written_atoms",
        input_export_sha256=exported.get("payload_sha256"),
        software=raw.get("software", {}),
    )
    for name in _METADATA:
        if name in raw and name not in adapted:
            adapted[name] = raw[name]
    for suffix in ("ids", "names"):
        written_labels = writer.get("output_atom_" + suffix)
        if written_labels is not None:
            adapted["source_atom_" + suffix] = written_labels
            adapted["output_atom_" + suffix] = written_labels[inverse]
    return direct(adapted)


def normalize(raw):
    schema = raw.get("schema")
    if not isinstance(schema, str):
        fail("An atom-map report requires a string schema identifier.")
    if schema in _CREATION:
        stage = creation(raw)
    elif schema in _DIRECT:
        stage = direct(raw)
    elif schema == "molsysmt.pdbqt_pose_read@1":
        stage = pose(raw)
    else:
        fail(f"Unsupported atom-map report schema {schema!r}.")
    if schema == "molsysmt.atom_export@1":
        stage["output_payload_sha256"] = raw.get("payload_sha256")
    if schema in {"molsysmt.atom_export@1", "molsysmt.atom_projection@1"} and np.any(
        stage["output_to_source_atom_indices"] < 0
    ):
        fail(
            "Export and projection reports cannot declare newly generated output atoms."
        )
    if "parent_atom_pairs" in raw and schema == SCHEMA:
        parents = pairs(raw["parent_atom_pairs"], "parent_atom_pairs")
        if (
            np.any(parents[:, 0] < 0)
            or np.any(parents[:, 0] >= stage["n_source_atoms"])
            or not np.array_equal(
                np.sort(parents[:, 1]),
                np.flatnonzero(stage["output_to_source_atom_indices"] < 0),
            )
        ):
            fail(
                "Normalized parent evidence must identify every new output and valid source parents."
            )
        stage["parent_atom_pairs"] = parents
        if "generated_atom_ids" in raw:
            stage["generated_atom_ids"] = deepcopy(raw["generated_atom_ids"])
    if "merged_source_atom_pairs" in raw:
        merged = pairs(raw["merged_source_atom_pairs"], "merged_source_atom_pairs")
        forward = stage["source_to_output_atom_indices"]
        if (
            np.any(merged < 0)
            or np.any(merged >= len(forward))
            or len(np.unique(merged[:, 0])) != len(merged)
        ):
            fail(
                "Merged atom pairs require unique removed source atoms and valid source indices."
            )
        if np.any(forward[merged[:, 0]] != -1) or np.any(forward[merged[:, 1]] < 0):
            fail(
                "Merged sources must be absent directly and their source parents retained."
            )
        targets = forward[merged[:, 1]]
        representatives = stage["source_to_representative_atom_indices"]
        if schema == SCHEMA and not np.array_equal(
            representatives[merged[:, 0]], targets
        ):
            fail("Normalized merge evidence disagrees with representative indices.")
        representatives[merged[:, 0]] = targets
        stage["merged_source_atom_pairs"] = merged
        if "charge_transfers" in raw:
            charges = array(raw["charge_transfers"], "charge_transfers")
            if (
                raw.get("charge_unit") != "elementary_charge"
                or charges.shape != (len(merged),)
                or charges.dtype.kind not in "fiu"
                or not np.isfinite(charges).all()
            ):
                fail(
                    "Merge charge transfers require finite aligned values in elementary_charge."
                )
            stage["charge_transfers"] = charges.astype(np.float64, copy=True)
            stage["charge_unit"] = "elementary_charge"
        elif schema == "molsysmt.atom_projection@1" and len(merged):
            fail("A hydrogen projection report requires its declared charge transfers.")
    if "source_atom_status" in raw:
        expected = np.where(
            stage["source_to_output_atom_indices"] >= 0,
            "retained",
            np.where(
                stage["source_to_representative_atom_indices"] >= 0, "merged", "omitted"
            ),
        )
        if not np.array_equal(
            array(raw["source_atom_status"], "source_atom_status"), expected
        ):
            fail(
                "source_atom_status disagrees with direct and representative correspondence."
            )
    return stage


def aggregate(stages):
    first = stages[0]
    n_source = first["n_source_atoms"]
    forward = inverse = representatives = np.arange(n_source, dtype=np.int64)
    previous = None
    for stage in stages:
        if len(inverse) != stage["n_source_atoms"]:
            fail("Adjacent atom-map axis counts disagree.")
        if previous is not None:
            for suffix in ("ids", "names"):
                left, right = (
                    previous.get("output_atom_" + suffix),
                    stage.get("source_atom_" + suffix),
                )
                if left is not None and right is not None:
                    known = (left != None) & (right != None)  # noqa: E711
                    if not np.array_equal(left[known], right[known]):
                        fail(
                            f"Adjacent atom-map {suffix} disagree in their declared index order."
                        )
            left, right = (
                previous.get("output_payload_sha256"),
                stage.get("input_export_sha256"),
            )
            if left is not None and right is not None and left != right:
                fail(
                    "The pose reader's declared export binding disagrees with the previous writer map."
                )

        def advance(values, mapping):
            result = np.full(len(values), -1, dtype=np.int64)
            present = values >= 0
            result[present] = mapping[values[present]]
            return result

        forward = advance(forward, stage["source_to_output_atom_indices"])
        representatives = advance(
            representatives, stage["source_to_representative_atom_indices"]
        )
        inverse = advance(stage["output_to_source_atom_indices"], inverse)
        previous = stage
    result = dict(
        schema=SCHEMA,
        n_source_atoms=n_source,
        n_output_atoms=len(inverse),
        source_to_output_atom_indices=forward,
        output_to_source_atom_indices=inverse,
        source_to_representative_atom_indices=representatives,
        source_atom_status=np.where(
            forward >= 0,
            "retained",
            np.where(representatives >= 0, "merged", "omitted"),
        ),
        generated_output_atom_indices=np.flatnonzero(inverse < 0),
        stages=stages,
    )
    for name in _LABELS:
        stage = first if name.startswith("source") else stages[-1]
        if name in stage:
            result[name] = stage[name].copy()
    return result


def flatten(raw, depth=0):
    if depth > 32:
        fail("Atom-map stage nesting is too deep or cyclic.")
    atomic = normalize(raw)
    if raw.get("schema") != SCHEMA or "stages" not in raw:
        return [atomic]
    if (
        not isinstance(raw["stages"], (list, tuple))
        or not raw["stages"]
        or not all(isinstance(stage, dict) for stage in raw["stages"])
    ):
        fail("A composed map requires nonempty normalized stage dictionaries.")
    stages = [stage for entry in raw["stages"] for stage in flatten(entry, depth + 1)]
    restored = aggregate(stages)
    for field in (
        "n_source_atoms",
        "n_output_atoms",
        "source_to_output_atom_indices",
        "output_to_source_atom_indices",
        "source_to_representative_atom_indices",
    ):
        if not np.array_equal(atomic[field], restored[field]):
            fail(
                f"Composed atom-map aggregate disagrees with its stored stages: {field}."
            )
    for field in _LABELS:
        if field in atomic and (
            field not in restored or not np.array_equal(atomic[field], restored[field])
        ):
            fail(
                f"Composed atom-map labels disagree with their stored stages: {field}."
            )
    return stages


def compose(atom_maps):
    from molsysmt import __version__

    if (
        not isinstance(atom_maps, (list, tuple))
        or not atom_maps
        or not all(isinstance(item, dict) for item in atom_maps)
    ):
        raise ArgumentError("atom_maps", value=atom_maps, caller=CALLER)
    result = aggregate([stage for raw in atom_maps for stage in flatten(raw)])
    result["software"] = {"molsysmt": __version__}
    return result
