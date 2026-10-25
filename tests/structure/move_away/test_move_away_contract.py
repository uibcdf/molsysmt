"""Protect finite single-structure displacement and rejection before publication."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError, NotImplementedMethodError
from molsysmt.native import MolSys, Structures

XYZ = np.array(
    [
        [[0, 0, 0], [2, 1, 0], [3, 0, 1], [4, 2, 0], [5, 1, 2]],
        [[1, 0, 2], [3, 2, 1], [4, 1, 3], [6, 3, 1], [7, 2, 4]],
        [[0, 2, 1], [3, 3, 2], [2, 1, 4], [5, 4, 3], [6, 2, 5]],
    ],
    dtype=float,
)


def system(form="molsys", unit="nm"):
    structures = Structures(
        coordinates=puw.convert(puw.quantity(XYZ.copy(), "nm"), to_unit=unit),
        box=puw.quantity(np.tile(np.eye(3) * 12, (3, 1, 1)), "nm"),
    )
    if form == "structures":
        return structures
    source = MolSys(n_atoms=5)
    source.topology.atoms["atom_type"] = ["C", "N", "O", "S", "H"]
    source.structures = structures
    source.interactions = {
        "synthetic": msm.Interactions.from_records(
            [
                {
                    "structure_index": index,
                    "interaction_type": "hbond",
                    "participants": [
                        {"role": role, "atom_indices": [atom]}
                        for role, atom in [
                            ("donor", 0),
                            ("hydrogen", 1),
                            ("acceptor", 2),
                        ]
                    ],
                    "evidence": "synthetic",
                }
                for index in [0, 2]
            ],
            n_atoms=5,
            n_structures=3,
            evaluated_structure_indices=[0, 1, 2],
            method="synthetic_move_away_guard",
        )
    }
    return source


def values(source, attribute="coordinates"):
    return puw.get_value(msm.get(source, **{attribute: True}), to_unit="nm")


def snapshot(source):
    analysis = source.interactions["synthetic"] if isinstance(source, MolSys) else None
    return values(source).copy(), values(source, "box").copy(), analysis


def unchanged(source, before):
    np.testing.assert_array_equal(values(source), before[0])
    np.testing.assert_array_equal(values(source, "box"), before[1])
    if before[2] is not None:
        assert source.interactions["synthetic"] is before[2]
        np.testing.assert_array_equal(before[2].evaluated_structure_indices, [0, 1, 2])
        assert before[2].n_interactions == 2


@pytest.mark.parametrize("form", ["molsys", "structures"])
@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("distance", ["0 nm", "0.3 nm"])
def test_coincident_default_centers_reject_without_publication(
    form, in_place, distance
):
    source = system(form)
    before = snapshot(source)
    with pytest.raises(ArgumentError):
        msm.structure.move_away(source, distance=distance, in_place=in_place)
    unchanged(source, before)


@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize(
    "direction",
    [[0, 0, 0], [np.nan, 0, 1], [np.inf, 1, 0], [1, -np.inf, 2], [], [[0, 0, 0]]],
)
def test_undefined_explicit_direction_rejects_without_publication(in_place, direction):
    source = system()
    before = snapshot(source)
    with pytest.raises(ArgumentError):
        msm.structure.move_away(source, direction=direction, in_place=in_place)
    unchanged(source, before)


@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("mode", ["auto", "explicit"])
@pytest.mark.parametrize("structures", [[2, 0], [0, 1, 2], [2, 2], "all"])
def test_multiple_structures_reject_before_any_write(in_place, mode, structures):
    source = system()
    before = snapshot(source)
    with pytest.raises(NotImplementedMethodError):
        msm.structure.move_away(
            source,
            selection=[0, 2, 4],
            center_of_selection=[0, 2],
            reference_center_of_selection=[1, 3],
            structure_indices=structures,
            direction=None if mode == "auto" else [1, 0, 0],
            in_place=in_place,
        )
    unchanged(source, before)


@pytest.mark.parametrize("mode", ["auto", "explicit"])
@pytest.mark.parametrize("structures", [[0, 2], [1, 1], "all"])
def test_multiple_reference_structures_reject_without_publication(mode, structures):
    source = system()
    reference = system()
    before, ref_before = snapshot(source), snapshot(reference)
    with pytest.raises(NotImplementedMethodError):
        msm.structure.move_away(
            source,
            reference_molecular_system=reference,
            reference_structure_indices=structures,
            direction=None if mode == "auto" else [1, 0, 0],
            in_place=True,
        )
    unchanged(source, before)
    unchanged(reference, ref_before)


@pytest.mark.parametrize("form", ["molsys", "structures"])
@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("mode", ["auto", "explicit"])
@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize("structure", [2, [2]])
def test_weighted_displacement_matches_independent_cartesian_oracle(
    form, in_place, mode, unit, structure
):
    source = system(form, unit)
    reference = system("structures", "angstrom")
    before = snapshot(source)
    ref_before = snapshot(reference)
    weights, ref_weights = np.array([1.0, 3.0]), np.array([2.0, 1.0])
    source_center = np.average(XYZ[2, [0, 2]], axis=0, weights=weights)
    target_center = np.average(XYZ[1, [1, 3]], axis=0, weights=ref_weights)
    axis = source_center - target_center if mode == "auto" else np.array([2, -1, 2])
    axis = axis / np.linalg.norm(axis)
    delta = 0.3 * axis
    if mode == "explicit":
        delta += target_center - source_center
    expected = XYZ.copy()
    expected[2, [0, 2, 4]] += delta
    with puw.context(standard_units=[unit, "ps", "radians"]):
        result = msm.structure.move_away(
            source,
            selection=[0, 2, 4],
            center_of_selection=[0, 2],
            weights=weights,
            reference_molecular_system=reference,
            reference_center_of_selection=[1, 3],
            reference_weights=ref_weights,
            structure_indices=structure,
            reference_structure_indices=[1],
            direction=None if mode == "auto" else [2, -1, 2],
            distance="3 angstrom",
            in_place=in_place,
        )
    output = source if in_place else result
    assert result is None if in_place else result is not source
    np.testing.assert_allclose(values(output), expected, rtol=0, atol=1e-12)
    np.testing.assert_array_equal(values(output, "box"), before[1])
    np.testing.assert_allclose(
        values(output)[2, [0, 2, 4]][:, None] - values(output)[2, [0, 2, 4]][None, :],
        XYZ[2, [0, 2, 4]][:, None] - XYZ[2, [0, 2, 4]][None, :],
        atol=1e-12,
    )
    if isinstance(output, MolSys):
        np.testing.assert_array_equal(
            output.interactions["synthetic"].evaluated_structure_indices, [0, 1]
        )
        assert before[2].n_interactions == 2
    if not in_place:
        unchanged(source, before)
    unchanged(reference, ref_before)
    np.testing.assert_array_equal(weights, [1, 3])
    np.testing.assert_array_equal(ref_weights, [2, 1])


@pytest.mark.parametrize("magnitude", [1e-300, 1e300])
def test_finite_nonzero_direction_normalization_is_scale_safe(magnitude):
    source = system()
    before = values(source).copy()
    result = msm.structure.move_away(source, direction=[magnitude, 0, 0])
    expected = before.copy()
    expected[0, :, 0] += 0.3
    np.testing.assert_allclose(values(result), expected, atol=1e-12)
    np.testing.assert_array_equal(values(source), before)


@pytest.mark.parametrize("mode", ["auto", "explicit"])
@pytest.mark.parametrize("distance", ["nan nm", "inf nm", "[1, 2, 3] nm"])
def test_distance_must_be_one_finite_length_before_publication(mode, distance):
    source = system()
    before = snapshot(source)
    with pytest.raises(ArgumentError):
        msm.structure.move_away(
            source,
            center_of_selection=[0, 2],
            reference_center_of_selection=[1, 3],
            direction=None if mode == "auto" else [1, 0, 0],
            distance=distance,
            in_place=True,
        )
    unchanged(source, before)


@pytest.mark.parametrize("mode", ["auto", "explicit"])
@pytest.mark.parametrize(
    "arguments",
    [
        {"structure_indices": []},
        {"structure_indices": [-1]},
        {"structure_indices": [99]},
        {"structure_indices": [[0], [2]]},
        {"reference_structure_indices": []},
        {"reference_structure_indices": [-1]},
        {"reference_structure_indices": [99]},
        {"weights": [0, 0]},
        {"weights": [-1, 2]},
        {"weights": [np.nan, 1]},
        {"reference_weights": [0, 0]},
        {"reference_weights": [1, np.inf]},
        {"center_of_selection": []},
        {"reference_center_of_selection": []},
        {"selection": []},
    ],
)
def test_invalid_populations_axes_and_weights_preserve_scientific_state(
    mode, arguments
):
    source = system()
    before = snapshot(source)
    parameters = dict(
        selection=[0, 2, 4],
        center_of_selection=[0, 2],
        reference_center_of_selection=[1, 3],
        direction=None if mode == "auto" else [1, 0, 0],
        in_place=True,
    )
    parameters.update(arguments)
    with pytest.raises(ArgumentError):
        msm.structure.move_away(source, **parameters)
    unchanged(source, before)


@pytest.mark.parametrize("mode", ["auto", "explicit"])
@pytest.mark.parametrize("distance", [0.0, -0.3])
def test_zero_and_signed_finite_distances_retain_mode_semantics(mode, distance):
    source = system()
    before = values(source).copy()
    src = before[0, [0, 2]].mean(axis=0)
    ref = before[0, [1, 3]].mean(axis=0)
    axis = src - ref if mode == "auto" else np.array([1.0, 0.0, 0.0])
    axis /= np.linalg.norm(axis)
    delta = distance * axis
    if mode == "explicit":
        delta += ref - src
    result = msm.structure.move_away(
        source,
        selection=[0, 2, 4],
        center_of_selection=[0, 2],
        reference_center_of_selection=[1, 3],
        direction=None if mode == "auto" else [1, 0, 0],
        distance=puw.quantity(distance, "nm"),
    )
    expected = before.copy()
    expected[0, [0, 2, 4]] += delta
    np.testing.assert_allclose(values(result), expected, rtol=0, atol=1e-12)
    np.testing.assert_array_equal(values(source), before)


@pytest.mark.parametrize("mode", ["auto", "explicit"])
def test_external_reference_h5msm_is_read_only_and_uses_original_structure(
    tmp_path, mode
):
    source = system()
    path = tmp_path / "reference.h5msm"
    msm.convert(source, to_form=str(path))
    file_before = path.read_bytes()
    before = snapshot(source)
    result = msm.structure.move_away(
        source,
        selection=[0, 2, 4],
        center_of_selection=[0, 2],
        reference_molecular_system=str(path),
        reference_center_of_selection=[1, 3],
        structure_indices=[2],
        reference_structure_indices=[1],
        direction=None if mode == "auto" else [1, 0, 0],
    )
    axis = XYZ[2, [0, 2]].mean(axis=0) - XYZ[1, [1, 3]].mean(axis=0)
    axis = axis / np.linalg.norm(axis) if mode == "auto" else np.array([1, 0, 0])
    expected = XYZ.copy()
    delta = 0.3 * axis
    if mode == "explicit":
        delta += XYZ[1, [1, 3]].mean(axis=0) - XYZ[2, [0, 2]].mean(axis=0)
    expected[2, [0, 2, 4]] += delta
    np.testing.assert_allclose(values(result), expected, atol=1e-12)
    assert path.read_bytes() == file_before
    unchanged(source, before)


@pytest.mark.parametrize("mode", ["auto", "explicit"])
def test_mass_weights_and_repeated_atoms_respect_the_source_population(mode):
    source = system()
    moving, center_atoms, ref_atoms = [4, 0, 2, 0], [2, 0, 2], [3, 1, 3]
    masses = puw.get_value(
        msm.physchem.get_mass(source, element="atom", selection=center_atoms)
    )
    ref_masses = puw.get_value(
        msm.physchem.get_mass(source, element="atom", selection=ref_atoms)
    )
    src = np.average(XYZ[0, center_atoms], axis=0, weights=masses)
    ref = np.average(XYZ[0, ref_atoms], axis=0, weights=ref_masses)
    axis = src - ref if mode == "auto" else np.array([1.0, 0.0, 0.0])
    axis /= np.linalg.norm(axis)
    delta = 0.3 * axis
    if mode == "explicit":
        delta += ref - src
    result = msm.structure.move_away(
        source,
        selection=moving,
        center_of_selection=center_atoms,
        weights="masses",
        reference_center_of_selection=ref_atoms,
        reference_weights="masses",
        direction=None if mode == "auto" else [1, 0, 0],
    )
    expected = XYZ.copy()
    expected[0, np.unique(moving)] += delta
    np.testing.assert_allclose(values(result), expected, atol=1e-12)


@pytest.mark.parametrize("mode", ["auto", "explicit"])
def test_only_one_direction_and_one_reference_center_are_supported(mode):
    source = system()
    before = snapshot(source)
    params = (
        {"direction": [[1, 0, 0], [0, 1, 0]]}
        if mode == "explicit"
        else {"reference_center_of_selection": [[0, 1], [2, 3]]}
    )
    with pytest.raises(NotImplementedMethodError):
        msm.structure.move_away(source, **params, in_place=True)
    unchanged(source, before)


def test_rejected_bundled_reproductions_preserve_coordinates_and_box():
    for params, error in [
        ({}, ArgumentError),
        ({"direction": [0, 0, 0]}, ArgumentError),
        (
            {
                "selection": [0, 2, 4],
                "center_of_selection": [0, 2],
                "reference_center_of_selection": [1, 3],
                "structure_indices": [2, 0],
                "direction": [1, 0, 0],
            },
            NotImplementedMethodError,
        ),
    ]:
        source = msm.convert(
            msm.systems["pentalanine"]["traj_pentalanine.h5msm"],
            structure_indices=[0, 8, 3],
        )
        before = values(source).copy()
        with pytest.raises(error):
            msm.structure.move_away(source, **params, in_place=True)
        np.testing.assert_array_equal(values(source), before)


@pytest.mark.parametrize("mode", ["auto", "explicit"])
def test_requested_external_selection_syntax_is_used_for_all_populations(mode):
    pytest.importorskip("mdtraj")
    source = msm.convert(
        msm.systems["pentalanine"]["traj_pentalanine.h5msm"], structure_indices=[0]
    )
    before = values(source).copy()
    src, ref = before[0, [0, 2]].mean(axis=0), before[0, [1, 3]].mean(axis=0)
    axis = src - ref if mode == "auto" else np.array([1.0, 0.0, 0.0])
    axis /= np.linalg.norm(axis)
    delta = 0.3 * axis
    if mode == "explicit":
        delta += ref - src
    output = msm.structure.move_away(
        source,
        selection="index 0 or index 2 or index 4",
        center_of_selection="index 0 or index 2",
        reference_center_of_selection="index 1 or index 3",
        direction=None if mode == "auto" else [1, 0, 0],
        syntax="MDTraj",
    )
    expected = before.copy()
    expected[0, [0, 2, 4]] += delta
    np.testing.assert_allclose(values(output), expected, rtol=0, atol=1e-12)
    np.testing.assert_array_equal(values(source), before)


@pytest.mark.parametrize("mode", ["auto", "explicit"])
@pytest.mark.parametrize("bad_reference", [False, True])
def test_nonfinite_centers_reject_before_publishing(mode, bad_reference):
    bad, good = system("structures"), system()
    coordinates = puw.get_value(msm.get(bad, coordinates=True), to_unit="nm").copy()
    coordinates[0, 0, 0] = np.nan
    msm.set(bad, coordinates=puw.quantity(coordinates, "nm"))
    source, reference = (good, bad) if bad_reference else (bad, good)
    before, ref_before = snapshot(source), snapshot(reference)
    with pytest.raises(ArgumentError):
        msm.structure.move_away(
            source,
            reference_molecular_system=reference,
            direction=None if mode == "auto" else [1, 0, 0],
            in_place=True,
        )
    unchanged(source, before)
    unchanged(reference, ref_before)


def test_explicit_direction_normalization_does_not_mutate_input_array():
    source = system()
    direction = np.array([[2.0, -1.0, 2.0]])
    before = direction.copy()
    msm.structure.move_away(source, direction=direction)
    np.testing.assert_array_equal(direction, before)


def test_direction_with_length_units_is_not_silently_stripped():
    source = system()
    before = snapshot(source)
    with pytest.raises(ArgumentError):
        msm.structure.move_away(
            source, direction=puw.quantity([1, 0, 0], "nm"), in_place=True
        )
    unchanged(source, before)


@pytest.mark.parametrize("in_place", [False, True])
def test_explicit_offset_does_not_create_an_intermediate_system_copy(
    monkeypatch, in_place
):
    source = system()
    original = msm.basic.copy
    copies = []

    def counted_copy(*args, **kwargs):
        copies.append(1)
        return original(*args, **kwargs)

    monkeypatch.setattr(msm.basic, "copy", counted_copy)
    msm.structure.move_away(source, direction=[1, 0, 0], in_place=in_place)
    assert len(copies) == (0 if in_place else 1)
