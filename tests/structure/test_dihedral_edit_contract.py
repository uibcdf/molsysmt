"""Protect torsion edits with independent circular-angle and rotation references."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import (
    ArgumentError,
    ArgumentLengthError,
    StructuralInconsistencyError,
)
from molsysmt.native import MolSys

QUARTETS = np.array([[0, 1, 2, 3], [5, 6, 7, 8]], dtype=np.int64)
BLOCKS = [[2, 3], [7, 8]]
SCOPE = [2, 0, 2]


def system(box_kind="none", form="molsys", degenerate=False):
    first = np.array(
        [[0, 1, 0], [0, 0, 0], [1, 0, 0], [1, 1, 1], [2, 1, 1]], dtype=float
    )
    first = np.concatenate((first, first + [3, 2, 0]))
    coordinates = np.stack([first, first + [0.2, 0.1, 0.3], first + [0.1, 0.3, -0.1]])
    if degenerate:
        coordinates[:, 2] = coordinates[:, 1]
    source = MolSys(n_atoms=10)
    source.topology.atoms["atom_type"] = ["C"] * 10
    source.chemical_states.add_bonds([[i, i + 1] for i in [0, 1, 2, 3, 5, 6, 7, 8]])
    source.structures.coordinates = puw.quantity(coordinates, "nm")
    if box_kind != "none":
        box = (
            np.eye(3) * 12
            if box_kind == "orthogonal"
            else np.array([[12, 0, 0], [1, 13, 0], [0.4, 0.3, 14]])
        )
        source.structures.box = puw.quantity(np.tile(box, (3, 1, 1)), "nm")
        coordinates[0, 3] += box[1]
        source.structures.coordinates = puw.quantity(coordinates, "nm")
    source.interactions = {
        "analysis": msm.Interactions.from_records(
            [
                {
                    "structure_index": s,
                    "interaction_type": "pair",
                    "participants": [
                        {"role": "first", "atom_indices": [0]},
                        {"role": "second", "atom_indices": [3]},
                    ],
                    "evidence": "synthetic",
                }
                for s in [0, 2]
            ],
            n_atoms=10,
            n_structures=3,
            evaluated_structure_indices=[0, 1, 2],
            method="torsion_guard",
        )
    }
    return source if form == "molsys" else source.structures


def values(source, name="coordinates"):
    value = msm.get(source, **{name: True})
    return None if value is None else puw.get_value(value, to_unit="nm")


def snapshot(source):
    return {
        "coordinates": values(source).copy(),
        "box": None if values(source, "box") is None else values(source, "box").copy(),
        "atoms": source.topology.atoms.copy(deep=True),
        "bonds": source.chemical_states._resolve_chemical_state().bonds.copy(deep=True),
        "analysis": source.interactions["analysis"],
    }


def unchanged(source, before):
    np.testing.assert_array_equal(values(source), before["coordinates"])
    if before["box"] is None:
        assert values(source, "box") is None
    else:
        np.testing.assert_array_equal(values(source, "box"), before["box"])
    pd.testing.assert_frame_equal(source.topology.atoms, before["atoms"])
    pd.testing.assert_frame_equal(
        source.chemical_states._resolve_chemical_state().bonds, before["bonds"]
    )
    assert source.interactions["analysis"] is before["analysis"]
    np.testing.assert_array_equal(
        before["analysis"].evaluated_structure_indices, [0, 1, 2]
    )
    assert before["analysis"].n_interactions == 2


def mic(vector, box):
    if box is None:
        return vector
    fractional = vector @ np.linalg.inv(box)
    return (fractional - np.floor(fractional + 0.5)) @ box


def torsion(points, box):
    axis = mic(points[2] - points[1], box)
    axis /= np.linalg.norm(axis)
    first, last = mic(points[0] - points[1], box), mic(points[3] - points[2], box)
    first -= (first @ axis) * axis
    last -= (last @ axis) * axis
    return np.arctan2(np.cross(axis, first) @ last, first @ last)


def rotated(points, quartet, moving, target, box):
    output = points.copy()
    axis = mic(points[quartet[2]] - points[quartet[1]], box)
    axis /= np.linalg.norm(axis)
    delta = target - torsion(points[quartet], box)
    # Independent Rodrigues matrix, applied to row-vector coordinates.
    x, y, z = axis
    cross = np.array([[0, -z, y], [z, 0, -x], [-y, x, 0]])
    rotation = (
        np.cos(delta) * np.eye(3)
        + (1 - np.cos(delta)) * np.outer(axis, axis)
        + np.sin(delta) * cross
    )
    moving = np.asarray(moving)
    relative = mic(points[moving] - points[quartet[2]], box)
    output[moving] = points[quartet[2]] + mic(relative @ rotation.T, box)
    return output


def edit(source, method, value, **kwargs):
    return getattr(msm.structure, method)(
        source,
        **{"angles" if method == "set_dihedral_angles" else "shifts": value},
        **kwargs,
    )


@pytest.mark.parametrize("method", ["set_dihedral_angles", "shift_dihedral_angles"])
@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("bad", [np.nan, np.inf, -np.inf])
@pytest.mark.parametrize("shape", ["scalar", "vector", "matrix"])
@pytest.mark.parametrize("unit", ["radians", "degrees"])
@pytest.mark.parametrize("box_kind", ["none", "triclinic"])
def test_nonfinite_edit_rejects_without_publication(
    method, in_place, bad, shape, unit, box_kind
):
    source = system(box_kind)
    before = snapshot(source)
    payload = {"scalar": bad, "vector": [0.2, bad], "matrix": [[0.2, 0.3], [0.4, bad]]}[
        shape
    ]
    with pytest.raises(ArgumentError):
        edit(
            source,
            method,
            puw.quantity(payload, unit),
            dihedral_quartets=QUARTETS,
            blocks=BLOCKS,
            structure_indices=[2, 0],
            pbc=True,
            in_place=in_place,
        )
    unchanged(source, before)


@pytest.mark.parametrize("method", ["set_dihedral_angles", "shift_dihedral_angles"])
@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("box_kind", ["none", "orthogonal", "triclinic"])
@pytest.mark.parametrize("unit", ["radians", "degrees"])
@pytest.mark.parametrize("automatic", [False, True])
@pytest.mark.parametrize("shape", ["scalar", "full"])
def test_valid_edits_match_rotation_and_preserve_motion_scope(
    method, in_place, box_kind, unit, automatic, shape
):
    source = system(box_kind)
    before = snapshot(source)
    moving = [[2, 3, 4], [7, 8, 9]] if automatic else BLOCKS
    inputs = (
        np.broadcast_to(0.3, (3, 2))
        if shape == "scalar"
        else np.array([[0.2, -0.3], [0.5, 0.6], [-0.4, 0.7]])
    )
    argument = puw.convert(
        puw.quantity(0.3 if shape == "scalar" else inputs.copy(), "radians"),
        to_unit=unit,
    )
    expected = before["coordinates"].copy()
    targets = {}
    for row, s in enumerate(SCOPE):
        box = None if before["box"] is None else before["box"][s]
        target = inputs[row].copy()
        if method == "shift_dihedral_angles":
            target += [torsion(before["coordinates"][s, q], box) for q in QUARTETS]
        pose = before["coordinates"][s].copy()
        for q, block, value in zip(QUARTETS, moving, target, strict=True):
            pose = rotated(pose, q, block, value, box)
        expected[s], targets[s] = pose, target
    with puw.context(standard_units=["pm", "fs", unit]):
        result = edit(
            source,
            method,
            argument,
            dihedral_quartets=QUARTETS,
            blocks=None if automatic else BLOCKS,
            structure_indices=SCOPE,
            pbc=True,
            in_place=in_place,
        )
    output = source if in_place else result
    assert result is None if in_place else result is not source
    np.testing.assert_allclose(values(output), expected, atol=1e-11)
    np.testing.assert_array_equal(values(output)[1], before["coordinates"][1])
    for s, target in targets.items():
        box = None if before["box"] is None else before["box"][s]
        observed = [torsion(values(output)[s, q], box) for q in QUARTETS]
        np.testing.assert_allclose(
            np.arctan2(np.sin(observed - target), np.cos(observed - target)),
            0,
            atol=1e-11,
        )
    pd.testing.assert_frame_equal(output.topology.atoms, before["atoms"])
    pd.testing.assert_frame_equal(
        output.chemical_states._resolve_chemical_state().bonds, before["bonds"]
    )
    if before["box"] is not None:
        np.testing.assert_array_equal(values(output, "box"), before["box"])
    np.testing.assert_array_equal(
        output.interactions["analysis"].evaluated_structure_indices, [1]
    )
    np.testing.assert_array_equal(
        before["analysis"].evaluated_structure_indices, [0, 1, 2]
    )
    if not in_place:
        unchanged(source, before)


@pytest.mark.parametrize("method", ["set_dihedral_angles", "shift_dihedral_angles"])
@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize(
    "blocks",
    [[], [[]], [[2]], [[2, 10]], [[-1, 3]], [[2.0, 3.0]], [[[2, 3]]], [[True, False]]],
)
def test_invalid_explicit_blocks_reject_without_publication(method, in_place, blocks):
    source = system()
    before = snapshot(source)
    with pytest.raises(ArgumentError):
        edit(
            source,
            method,
            ".3 radians",
            dihedral_quartets=QUARTETS[:1],
            blocks=blocks,
            structure_indices=[0],
            in_place=in_place,
        )
    unchanged(source, before)


@pytest.mark.parametrize("method", ["set_dihedral_angles", "shift_dihedral_angles"])
@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize(
    "values", [[], [0.1, 0.2, 0.3], np.ones((3, 3)), [[0.1 + 0.2j]], np.ones((1, 1, 1))]
)
def test_invalid_angular_shapes_or_complex_values_reject_without_publication(
    method, in_place, values
):
    source = system()
    before = snapshot(source)
    with pytest.raises((ArgumentError, ArgumentLengthError)):
        edit(
            source,
            method,
            puw.quantity(values, "radians"),
            dihedral_quartets=QUARTETS,
            blocks=BLOCKS,
            structure_indices=[2, 0],
            in_place=in_place,
        )
    unchanged(source, before)


@pytest.mark.parametrize("method", ["set_dihedral_angles", "shift_dihedral_angles"])
@pytest.mark.parametrize(
    "quartets",
    [[], [[0, 1, 2, 10]], [[-1, 1, 2, 3]], [[0, 1, 1, 3]], [[0.0, 1.0, 2.0, 3.0]]],
)
def test_invalid_quartets_reject_before_rust(method, quartets):
    source = system()
    before = snapshot(source)
    with pytest.raises(ArgumentError):
        edit(
            source,
            method,
            ".3 radians",
            dihedral_quartets=quartets,
            blocks=BLOCKS,
            structure_indices=[0],
            in_place=True,
        )
    unchanged(source, before)


@pytest.mark.parametrize("method", ["set_dihedral_angles", "shift_dihedral_angles"])
@pytest.mark.parametrize("in_place", [False, True])
def test_undefined_geometry_cannot_publish_bad_edit_but_can_be_measured(
    method, in_place
):
    source = system(degenerate=True)
    before = snapshot(source)
    measured = msm.structure.get_dihedral_angles(
        source,
        dihedral_quartets=QUARTETS[:1],
        structure_indices=[0],
        pbc=False,
        use_gpu=False,
    )
    assert np.isnan(puw.get_value(measured)).all()
    with pytest.raises((ArgumentError, StructuralInconsistencyError)):
        edit(
            source,
            method,
            ".3 radians",
            dihedral_quartets=QUARTETS[:1],
            blocks=BLOCKS,
            structure_indices=[0],
            pbc=False,
            in_place=in_place,
        )
    unchanged(source, before)


@pytest.mark.parametrize("method", ["set_dihedral_angles", "shift_dihedral_angles"])
@pytest.mark.parametrize("in_place", [False, True])
def test_explicit_block_pool_uses_union_for_each_terminal_atom(method, in_place):
    source = system()
    before = snapshot(source)
    target = 0.3 + (
        torsion(before["coordinates"][0, QUARTETS[0]], None)
        if method == "shift_dihedral_angles"
        else 0
    )
    expected = rotated(before["coordinates"][0], QUARTETS[0], [2, 3, 4], target, None)
    result = edit(
        source,
        method,
        ".3 radians",
        dihedral_quartets=QUARTETS[0],
        blocks=[[2, 3], [3, 4]],
        structure_indices=[0],
        pbc=False,
        in_place=in_place,
    )
    output = source if in_place else result
    np.testing.assert_allclose(values(output)[0], expected, atol=1e-11)
    np.testing.assert_array_equal(values(output)[1:], before["coordinates"][1:])
    if not in_place:
        unchanged(source, before)


@pytest.mark.parametrize("method", ["set_dihedral_angles", "shift_dihedral_angles"])
@pytest.mark.parametrize("form", ["structures", "structures_dict"])
@pytest.mark.parametrize("in_place", [False, True])
def test_explicit_blocks_need_only_coordinate_form(method, form, in_place):
    source = system(form="structures")
    if form == "structures_dict":
        source = msm.convert(source, to_form="molsysmt.StructuresDict")
    before = values(source).copy()
    target = 0.3 + (
        torsion(before[0, QUARTETS[0]], None)
        if method == "shift_dihedral_angles"
        else 0
    )
    expected = rotated(before[0], QUARTETS[0], BLOCKS[0], target, None)
    result = edit(
        source,
        method,
        ".3 radians",
        dihedral_quartets=QUARTETS[0],
        blocks=BLOCKS,
        structure_indices=[0],
        pbc=False,
        in_place=in_place,
    )
    output = source if in_place else result
    assert msm.get_form(output) == msm.get_form(source)
    np.testing.assert_allclose(values(output)[0], expected, atol=1e-11)
    np.testing.assert_array_equal(values(output)[1:], before[1:])
    if not in_place:
        np.testing.assert_array_equal(values(source), before)
