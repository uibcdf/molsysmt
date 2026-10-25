"""Check reference centering against independently weighted coordinate means."""

import numpy as np
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError
from molsysmt.native import MolSys, Structures

XYZ = np.array(
    [
        [
            [0.1, 1.2, 0.3],
            [1.4, 0.2, 0.8],
            [2.5, 1.6, 0.9],
            [0.4, 2.7, 1.1],
            [3.2, 0.6, 2.3],
        ],
        [
            [0.4, 1.1, 0.8],
            [1.8, 0.5, 1.2],
            [2.1, 1.3, 0.6],
            [0.7, 2.4, 1.6],
            [3.8, 0.9, 2.0],
        ],
        [
            [0.7, 1.5, 0.2],
            [1.1, 0.7, 1.4],
            [2.8, 1.0, 0.5],
            [0.2, 2.9, 1.8],
            [3.4, 0.3, 2.8],
        ],
        [
            [0.3, 1.9, 0.6],
            [1.6, 0.1, 1.0],
            [2.3, 1.8, 0.4],
            [0.9, 2.0, 1.7],
            [3.7, 0.8, 2.5],
        ],
    ]
)


def system(form="molsys", unit="nm"):
    structures = Structures(
        coordinates=puw.convert(puw.quantity(XYZ.copy(), "nm"), to_unit=unit)
    )
    if form == "structures":
        return structures
    molsys = MolSys(n_atoms=5)
    molsys.topology.atoms["atom_type"] = ["C", "N", "O", "S", "H"]
    molsys.structures = structures
    return molsys


def coordinates(molsys):
    return puw.get_value(
        msm.get(molsys, element="atom", coordinates=True), to_unit="nm"
    )


@pytest.mark.parametrize("form", ["molsys", "structures"])
@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("structures", [[0], [3, 0, 2], [3, 0, 3]])
@pytest.mark.parametrize(
    "moving,reference,weights",
    [
        ([0, 1, 2, 3, 4], [0, 2], None),
        ([4, 2, 0], [2, 0], [3.0, 1.0]),
        ([0, 2, 0, 4], [2, 0, 2], [1.0, 3.0, 4.0]),
    ],
)
@pytest.mark.parametrize("target_kind", ["origin", "point", "per_structure"])
def test_included_reference_reaches_target_and_preserves_scope(
    form, in_place, structures, moving, reference, weights, target_kind
):
    source = system(form, "angstrom")
    before = coordinates(source).copy()
    if target_kind == "origin":
        target, argument = np.zeros((len(structures), 1, 3)), None
    elif target_kind == "point":
        target = np.tile([0.1, 0.2, 0.3], (len(structures), 1, 1))
        argument = puw.quantity([1.0, 2.0, 3.0], "angstrom")
    else:
        target = np.array([[[0.1 + 0.05 * index, 0.2, 0.3]] for index in structures])
        argument = puw.quantity(target * 1000.0, "pm")
    before_weights = None if weights is None else list(weights)
    original_centers = np.average(
        before[structures][:, reference], axis=1, weights=weights
    )
    expected = before.copy()
    for position, index in enumerate(structures):
        expected[index, np.unique(moving)] = (
            before[index, np.unique(moving)]
            + target[position, 0]
            - original_centers[position]
        )
    result = msm.structure.center(
        source,
        selection=moving,
        source_center_selection=reference,
        weights=weights,
        target_coordinates=argument,
        structure_indices=structures,
        in_place=in_place,
    )
    output = source if in_place else result
    if in_place:
        assert result is None
    else:
        assert output is not source
        np.testing.assert_array_equal(coordinates(source), before)
    np.testing.assert_allclose(coordinates(output), expected, atol=1e-12)
    np.testing.assert_allclose(
        np.average(
            coordinates(output)[structures][:, reference], axis=1, weights=weights
        ),
        target[:, 0],
        atol=1e-12,
    )
    assert weights == before_weights


@pytest.mark.parametrize("presentation", ["nm", "angstrom", "pm"])
def test_centering_respects_application_units(presentation):
    previous = list(puw.configure.get_standard_units())
    with puw.context(standard_units=[presentation, "ps", "radians"]):
        source = system(unit="pm")
        before = coordinates(source).copy()
        result = msm.structure.center(
            source, target_coordinates=puw.quantity([1.0, 2.0, 3.0], "angstrom")
        )
        np.testing.assert_allclose(
            coordinates(result).mean(axis=1),
            np.tile([0.1, 0.2, 0.3], (4, 1)),
            atol=1e-12,
        )
        np.testing.assert_array_equal(coordinates(source), before)
    assert list(puw.configure.get_standard_units()) == previous


@pytest.mark.parametrize("bad", [np.nan, np.inf, -np.inf])
def test_nonfinite_target_rejects_without_mutating_input(bad):
    source = system()
    with pytest.raises(ArgumentError):
        msm.structure.center(
            source,
            target_coordinates=puw.quantity([bad, 0.0, 0.0], "nm"),
            in_place=True,
        )
    np.testing.assert_array_equal(coordinates(source), XYZ)


def test_single_target_cannot_broadcast_to_multiple_atom_centers():
    source = system()
    with pytest.raises(ArgumentError):
        msm.structure.center(
            source,
            target_coordinates=puw.quantity(np.ones((1, 5, 3)), "nm"),
            in_place=True,
        )
    np.testing.assert_array_equal(coordinates(source), XYZ)


def test_conflicting_targets_for_repeated_structures_reject_before_editing():
    source = system()
    with pytest.raises(ArgumentError):
        msm.structure.center(
            source,
            structure_indices=[2, 0, 2],
            target_coordinates=puw.quantity(
                [[[0.0, 0.0, 0.0]], [[0.0, 0.0, 0.0]], [[1.0, 0.0, 0.0]]], "nm"
            ),
            in_place=True,
        )
    np.testing.assert_array_equal(coordinates(source), XYZ)


@pytest.mark.parametrize("in_place", [False, True])
def test_roundoff_correction_preserves_return_ownership_and_one_copy_limit(
    in_place, monkeypatch
):
    values = XYZ + 1e8
    weights = [1.0, 2.0, 3.0, 4.0, 5.0]
    initial = np.average(values, axis=1, weights=weights)
    residual = np.average(values - initial[:, None, :], axis=1, weights=weights)
    assert np.max(np.abs(residual)) > 1e-12
    source = Structures(coordinates=puw.quantity(values, "nm"))
    original = coordinates(source).copy()
    calls = []
    copy = msm.basic.copy

    def tracked_copy(*args, **kwargs):
        calls.append(1)
        return copy(*args, **kwargs)

    monkeypatch.setattr(msm.basic, "copy", tracked_copy)
    result = msm.structure.center(source, weights=weights, in_place=in_place)
    assert len(calls) <= (0 if in_place else 1)
    if in_place:
        assert result is None
    else:
        assert result is not source
        np.testing.assert_array_equal(coordinates(source), original)
    np.testing.assert_allclose(
        np.average(
            coordinates(source if in_place else result), axis=1, weights=weights
        ),
        0.0,
        atol=1e-12,
    )


def trajectory():
    md = pytest.importorskip("mdtraj")
    topology = md.Topology()
    group = topology.add_residue("ALA", topology.add_chain())
    for name, element in zip(
        ["CA", "N", "O", "SG", "H"],
        [
            md.element.carbon,
            md.element.nitrogen,
            md.element.oxygen,
            md.element.sulfur,
            md.element.hydrogen,
        ],
    ):
        topology.add_atom(name, element, group)
    return md.Trajectory(XYZ, topology)


def test_general_get_center_honors_the_requested_selection_syntax():
    source = trajectory()
    before = coordinates(source).copy()
    result = msm.structure.get_center(
        source, selection="index 0 or index 2", weights=[1.0, 3.0], syntax="MDTraj"
    )
    np.testing.assert_allclose(
        puw.get_value(result, to_unit="nm")[:, 0],
        np.average(before[:, [0, 2]], axis=1, weights=[1.0, 3.0]),
        atol=1e-12,
    )
    np.testing.assert_array_equal(coordinates(source), before)


@pytest.mark.parametrize("in_place", [False, True])
def test_center_honors_external_selection_syntax_on_a_writable_native_system(in_place):
    pytest.importorskip("mdtraj")
    builder = msm.MolSysBuilder()
    for name, kind in zip(["CA", "N", "O", "SG", "H"], ["C", "N", "O", "S", "H"]):
        builder.add_atom(atom_name=name, atom_type=kind)
    builder.add_group(list(range(5)), group_name="ALA")
    builder.set_coordinates(puw.quantity(XYZ.copy(), "nm"))
    source = builder.build()
    before = coordinates(source).copy()
    expected = before.copy()
    reference = np.average(before[:, [0, 2]], axis=1, weights=[1.0, 3.0])
    expected[:, [0, 2, 4]] -= reference[:, None, :]
    result = msm.structure.center(
        source,
        selection="index 0 or index 2 or index 4",
        source_center_selection="index 0 or index 2",
        weights=[1.0, 3.0],
        syntax="MDTraj",
        in_place=in_place,
    )
    if in_place:
        assert result is None
    else:
        np.testing.assert_array_equal(coordinates(source), before)
    output = source if in_place else result
    np.testing.assert_allclose(coordinates(output), expected, atol=1e-12)


@pytest.mark.parametrize("in_place", [False, True])
def test_coordinate_edit_invalidates_only_selected_structures(in_place):
    source = system()
    analysis = msm.Interactions.from_records(
        [
            {
                "structure_index": index,
                "interaction_type": "hbond",
                "participants": [
                    {"role": role, "atom_indices": [atom]}
                    for role, atom in [("donor", 0), ("hydrogen", 1), ("acceptor", 2)]
                ],
                "measurements": {"distance": 0.2},
                "evidence": "synthetic",
            }
            for index in [0, 2]
        ],
        n_atoms=5,
        n_structures=4,
        evaluated_structure_indices=[0, 1, 2, 3],
        method="synthetic_center_guard",
        measure_units={"distance": "nm"},
    )
    source.interactions = {"test": analysis}
    previous = source.interactions["test"]
    view = previous.query(structure_indices=[0])
    result = msm.structure.center(
        source,
        selection=[0, 2, 4],
        source_center_selection=[0, 2],
        weights=[1.0, 3.0],
        structure_indices=[3, 0, 3],
        in_place=in_place,
    )
    output = source if in_place else result
    np.testing.assert_array_equal(
        output.interactions["test"].evaluated_structure_indices, [1, 2]
    )
    assert output.interactions["test"].query(structure_indices=[2]).n_interactions == 1
    assert previous.n_interactions == 2
    assert view.n_interactions == 1
    if not in_place:
        np.testing.assert_array_equal(
            source.interactions["test"].evaluated_structure_indices, [0, 1, 2, 3]
        )
        np.testing.assert_array_equal(coordinates(source), XYZ)


@pytest.mark.parametrize(
    "weights", [[-1.0, 2.0], [0.0, 0.0], [np.nan, 1.0], [1.0, np.inf], [[1.0, 2.0]]]
)
def test_bad_weights_reject_without_coordinate_changes(weights):
    source = system()
    with pytest.raises(ArgumentError):
        msm.structure.center(
            source, source_center_selection=[0, 2], weights=weights, in_place=True
        )
    np.testing.assert_array_equal(coordinates(source), XYZ)


def test_atomic_masses_use_the_general_chemical_property_owner():
    source = system()
    reference = [2, 0]
    masses = puw.get_value(
        msm.physchem.get_mass(source, element="atom", selection=reference)
    )
    center = np.average(XYZ[:, reference], axis=1, weights=masses)
    expected = XYZ - center[:, None, :]
    result = msm.structure.center(
        source, source_center_selection=reference, weights="masses"
    )
    np.testing.assert_allclose(coordinates(result), expected, atol=1e-12)
    np.testing.assert_array_equal(coordinates(source), XYZ)


@pytest.mark.parametrize("form", ["molsys", "structures"])
@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("structures", [[2, 0], [3, 0, 3]])
@pytest.mark.parametrize(
    "moving,reference,destination,weights",
    [
        ([2, 4], None, [0, 1], None),
        ([0, 2, 4], [2, 0], [1, 3], [3.0, 1.0]),
        ([0, 2, 4], [2, 0], [0, 1], [3.0, 1.0]),
        ([0, 1, 2, 3, 4], [2, 0], [1, 3], None),
        ([4, 2, 4], None, [1, 3, 1], [1.0, 2.0, 3.0]),
    ],
)
def test_selection_target_uses_initial_center_and_preserves_rigid_geometry(
    form, in_place, structures, moving, reference, destination, weights
):
    source = system(form, "pm")
    before = coordinates(source).copy()
    reference = moving if reference is None else reference
    target = before[structures][:, destination].mean(axis=1)
    initial = np.average(before[structures][:, reference], axis=1, weights=weights)
    expected = before.copy()
    for row, index in enumerate(structures):
        expected[index, np.unique(moving)] = (
            before[index, np.unique(moving)] + target[row] - initial[row]
        )
    result = msm.structure.center(
        source,
        selection=moving,
        source_center_selection=reference,
        target_center_selection=destination,
        weights=weights,
        structure_indices=structures,
        in_place=in_place,
    )
    output = source if in_place else result
    assert (result is None) == in_place
    np.testing.assert_allclose(coordinates(output), expected, atol=1e-12)
    np.testing.assert_allclose(
        np.average(
            coordinates(output)[structures][:, reference], axis=1, weights=weights
        ),
        target,
        atol=1e-12,
    )
    unique = np.unique(moving)
    for index in np.unique(structures):
        initial_xyz = before[index, unique]
        initial_vectors = initial_xyz[:, None] - initial_xyz[None, :]
        output_xyz = coordinates(output)[index, unique]
        final_vectors = output_xyz[:, None] - output_xyz[None, :]
        np.testing.assert_allclose(final_vectors, initial_vectors, atol=1e-12)
    if not in_place:
        np.testing.assert_array_equal(coordinates(source), before)


@pytest.mark.parametrize("in_place", [False, True])
def test_destination_from_two_atoms_places_a_third_at_their_midpoint(in_place):
    source = Structures(
        coordinates=puw.quantity(
            [[[2.0, 0.0, 0.0], [4.0, 0.0, 0.0], [10.0, 0.0, 0.0]]], "nm"
        )
    )
    result = msm.structure.center(
        source,
        selection=2,
        target_center_selection=[0, 1],
        in_place=in_place,
    )
    np.testing.assert_allclose(
        coordinates(source if in_place else result)[0, :, 0], [2.0, 4.0, 3.0]
    )


@pytest.mark.parametrize("moving", [[2, 4], [4, 2, 4]])
def test_default_source_center_is_the_moving_selection(moving):
    source = system()
    result = msm.structure.center(
        source, selection=moving, target_coordinates="[1, 2, 3] nm"
    )
    expected = XYZ.copy()
    expected[:, np.unique(moving)] += (
        np.array([1.0, 2.0, 3.0]) - XYZ[:, moving].mean(axis=1)
    )[:, None]
    np.testing.assert_allclose(coordinates(result), expected, atol=1e-12)


@pytest.mark.parametrize("reference", [[0, 2, 4], [1, 3]])
def test_partial_or_disjoint_source_population_rejects_before_editing(reference):
    source = system()
    with pytest.raises(ArgumentError, match="contained"):
        msm.structure.center(
            source, selection=[0, 2], source_center_selection=reference, in_place=True
        )
    np.testing.assert_array_equal(coordinates(source), XYZ)


def test_two_destination_modes_reject_before_editing():
    source = system()
    with pytest.raises(ArgumentError, match="either"):
        msm.structure.center(
            source,
            target_center_selection=[0, 1],
            target_coordinates="[1, 2, 3] nm",
            in_place=True,
        )
    np.testing.assert_array_equal(coordinates(source), XYZ)


@pytest.mark.parametrize(
    "argument", ["selection", "source_center_selection", "target_center_selection"]
)
@pytest.mark.parametrize("population", [[], [[0, 1], [2, 3]]])
def test_empty_or_nested_atom_populations_reject_before_editing(argument, population):
    source = system()
    with pytest.raises(ArgumentError):
        msm.structure.center(source, **{argument: population}, in_place=True)
    np.testing.assert_array_equal(coordinates(source), XYZ)


@pytest.mark.parametrize("destination", ["[1, 2, 3] ps", [1.0, 2.0, 3.0]])
def test_target_requires_length_units(destination):
    source = system()
    with pytest.raises(ArgumentError):
        msm.structure.center(source, target_coordinates=destination, in_place=True)
    np.testing.assert_array_equal(coordinates(source), XYZ)


@pytest.mark.parametrize("argument", ["center_coordinates", "center_of_selection"])
def test_retired_keyword_names_reject_instead_of_silently_changing_meaning(argument):
    source = system()
    with pytest.raises(UnknownArgumentError, match=argument):
        msm.structure.center(source, **{argument: None}, in_place=True)
    np.testing.assert_array_equal(coordinates(source), XYZ)


@pytest.mark.parametrize("presentation", ["nm", "angstrom", "pm"])
def test_atom_target_uses_physical_units_under_application_policy(presentation):
    with puw.context(standard_units=[presentation, "ps", "radians"]):
        source = system(unit="angstrom")
        before = coordinates(source).copy()
        result = msm.structure.center(
            source, selection=[2, 4], target_center_selection=[0, 1]
        )
        target = before[:, [0, 1]].mean(axis=1)
        np.testing.assert_allclose(
            coordinates(result)[:, [2, 4]].mean(axis=1), target, atol=1e-12
        )


def test_target_selection_honors_the_requested_external_syntax():
    pytest.importorskip("mdtraj")
    builder = msm.MolSysBuilder()
    for index in range(5):
        builder.add_atom(atom_name=f"C{index}", atom_type="C")
    builder.add_group(list(range(5)), group_name="LIG")
    builder.set_coordinates(puw.quantity(XYZ.copy(), "nm"))
    source = builder.build()
    result = msm.structure.center(
        source,
        selection="index 2 or index 4",
        source_center_selection="index 2",
        target_center_selection="index 0 or index 1",
        syntax="MDTraj",
    )
    expected = XYZ.copy()
    expected[:, [2, 4]] += (XYZ[:, [0, 1]].mean(axis=1) - XYZ[:, 2])[:, None]
    np.testing.assert_allclose(coordinates(result), expected, atol=1e-12)


@pytest.mark.parametrize("indices", [[3, -1], [True], [[0, 1]], [0.5], []])
def test_invalid_structure_axes_reject_before_coordinate_edits(indices):
    source = system()
    with pytest.raises(ArgumentError):
        msm.structure.center(source, structure_indices=indices, in_place=True)
    np.testing.assert_array_equal(coordinates(source), XYZ)
