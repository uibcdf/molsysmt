"""Check wrapping against orthogonal-cell arithmetic and original edit ownership."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import MolSys

MOVING = np.array([0, 1, 2, 3])
REFERENCE = [0, 1]
WEIGHTS = [1.0, 3.0]
MODES = ["pbc", "pbc_origin", "pbc_center", "mic"]


def system(form):
    source = MolSys(n_atoms=6)
    source.topology.atoms["atom_type"] = ["C"] * 6
    source.chemical_states.add_bonds([[0, 1], [2, 3]])
    xyz = np.array(
        [
            [6.10, -4.30, 9.20],
            [6.35, -4.15, 9.45],
            [8.80, -3.20, 8.60],
            [6.10, -3.10, 8.80],
            [9.10, -8.30, 6.70],
            [10.4, -7.2, 5.3],
        ]
    )
    coordinates = np.stack([xyz + [i * 0.17, -i * 0.23, i * 0.11] for i in range(4)])
    boxes = np.tile(np.diag([3.0, 4.0, 5.0]), (4, 1, 1))
    source.structures.coordinates = puw.quantity(coordinates, "nm")
    source.structures.box = puw.quantity(boxes, "nm")
    source.interactions = {
        "guard": msm.Interactions.from_records(
            [
                {
                    "structure_index": i,
                    "interaction_type": "pair",
                    "participants": [
                        {"role": "first", "atom_indices": [0]},
                        {"role": "second", "atom_indices": [1]},
                    ],
                    "evidence": "synthetic",
                }
                for i in [0, 2]
            ],
            n_atoms=6,
            n_structures=4,
            evaluated_structure_indices=[0, 1, 2, 3],
            method="ownership_guard",
        )
    }
    if form == "structures":
        return source.structures
    if form == "dictionary":
        return msm.convert(source.structures, to_form="molsysmt.StructuresDict")
    return source


def values(source, attribute="coordinates"):
    return puw.get_value(msm.get(source, **{attribute: True}), to_unit="nm")


def options(mode):
    if mode == "pbc":
        return msm.pbc.wrap_to_pbc, {}, np.zeros(3), False
    point = np.array([0.13, -0.24, 0.31])
    if mode == "pbc_origin":
        return (
            msm.pbc.wrap_to_pbc,
            {"box_origin": puw.quantity(point, "nm")},
            point,
            False,
        )
    if mode == "pbc_center":
        return (
            msm.pbc.wrap_to_pbc,
            {"box_center": puw.quantity(point, "nm")},
            point,
            True,
        )
    return msm.pbc.wrap_to_mic, {"mic_origin": puw.quantity(point, "nm")}, point, True


def expected_values(before, boxes, indices, centered, compact, origin, symmetric):
    expected = before.copy()
    for structure in np.unique(indices):
        xyz = before[structure, MOVING].copy()
        lengths = np.diag(boxes[structure])
        if centered:
            reference = np.average(
                before[structure, REFERENCE], axis=0, weights=WEIGHTS
            )
            xyz += np.array([0.1, 0.2, 0.3]) - reference
        lower = origin - lengths / 2 if symmetric else origin
        if compact:
            for a, b in [(0, 1), (2, 3)]:
                displacement = xyz[b] - xyz[a]
                xyz[b] = (
                    xyz[a] + displacement - np.rint(displacement / lengths) * lengths
                )
                center = (xyz[a] + xyz[b]) / 2
                shift = -np.floor((center - lower) / lengths) * lengths
                xyz[[a, b]] += shift
        else:
            xyz -= np.floor((xyz - lower) / lengths) * lengths
        expected[structure, MOVING] = xyz
    return expected


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize(
    "form,compact",
    [
        ("molsys", False),
        ("molsys", "component"),
        ("structures", False),
        ("dictionary", False),
    ],
)
@pytest.mark.parametrize("centered", [False, True])
@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize("indices", [[3, 1, 3], [2, 0]])
def test_original_target_receives_the_analytic_wrapped_coordinates(
    mode, form, compact, centered, in_place, unit, indices
):
    with puw.context(standard_units=[unit, "fs", "e"]):
        source = system(form)
        before, boxes = values(source).copy(), values(source, "box").copy()
        function, kwargs, origin, symmetric = options(mode)
        if centered:
            kwargs.update(
                center_of_selection=REFERENCE,
                weights=WEIGHTS,
                center_coordinates=puw.quantity([0.1, 0.2, 0.3], "nm"),
            )
        topology = source.topology if form == "molsys" else None
        if topology is not None:
            atoms, bonds = (
                topology.copy().atoms,
                source.chemical_states.get_bonds().copy(deep=True),
            )
            previous = source.interactions["guard"]
        expected = expected_values(
            before, boxes, indices, centered, compact, origin, symmetric
        )
        result = function(
            source,
            selection=MOVING,
            structure_indices=indices,
            compact=compact,
            in_place=in_place,
            **kwargs,
        )
        output = source if in_place else result
        assert (result is None) == in_place
        assert msm.get_form(output) == msm.get_form(source)
        np.testing.assert_allclose(values(output), expected, rtol=0, atol=1e-12)
        np.testing.assert_array_equal(values(output, "box"), boxes)
        np.testing.assert_array_equal(values(source, "box"), boxes)
        if not in_place:
            np.testing.assert_array_equal(values(source), before)
        if topology is not None:
            assert source.topology is topology
            pd.testing.assert_frame_equal(source.topology.atoms, atoms)
            pd.testing.assert_frame_equal(
                source.chemical_states._resolve_chemical_state().bonds, bonds
            )
            pd.testing.assert_frame_equal(output.topology.atoms, atoms)
            pd.testing.assert_frame_equal(
                output.chemical_states._resolve_chemical_state().bonds, bonds
            )
            retained = sorted(set(range(4)) - set(indices))
            np.testing.assert_array_equal(
                output.interactions["guard"].evaluated_structure_indices, retained
            )
            assert output.interactions["guard"].n_interactions == len(
                set(retained) & {0, 2}
            )
            np.testing.assert_array_equal(
                previous.evaluated_structure_indices, [0, 1, 2, 3]
            )
            assert previous.n_interactions == 2
            if not in_place:
                assert source.interactions["guard"] is previous


@pytest.mark.parametrize("mode", ["pbc", "mic"])
@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("failure", ["box", "reference"])
def test_centered_validation_failure_preserves_input_and_analysis(
    mode, in_place, failure
):
    source = system("molsys")
    reference = REFERENCE
    if failure == "box":
        source.structures.box = puw.quantity(np.zeros((4, 3, 3)), "nm")
    else:
        reference = [4]
    before, boxes = values(source).copy(), values(source, "box").copy()
    previous = source.interactions["guard"]
    previous_count = previous.n_interactions
    previous_coverage = previous.evaluated_structure_indices.copy()
    function, kwargs, _, _ = options(mode)
    with pytest.raises((ArgumentError, StructuralInconsistencyError)):
        function(
            source,
            selection=MOVING,
            center_of_selection=reference,
            structure_indices=[3, 1],
            compact=False,
            in_place=in_place,
            **kwargs,
        )
    np.testing.assert_array_equal(values(source), before)
    np.testing.assert_array_equal(values(source, "box"), boxes)
    assert source.interactions["guard"] is previous
    assert previous.n_interactions == previous_count
    np.testing.assert_array_equal(
        previous.evaluated_structure_indices, previous_coverage
    )


@pytest.mark.parametrize("mode", ["pbc", "mic"])
@pytest.mark.parametrize("in_place", [False, True])
def test_centered_result_uses_one_working_system_copy(mode, in_place, monkeypatch):
    source = system("molsys")
    copy = msm.basic.copy
    calls = []

    def counted_copy(*args, **kwargs):
        calls.append(args[0])
        return copy(*args, **kwargs)

    monkeypatch.setattr(msm.basic, "copy", counted_copy)
    function, kwargs, _, _ = options(mode)
    function(
        source,
        selection=MOVING,
        structure_indices=[3, 1],
        center_of_selection=REFERENCE,
        compact=False,
        in_place=in_place,
        **kwargs,
    )
    assert len(calls) == 1
    assert calls[0] is source
