"""Compare reflection with independent plane matrices and geometric invariants."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.native import MolSys, Structures

BASE = np.array([[0.1, 0.2, 0.3], [1.1, 0.3, 0.5], [0.2, 1.2, 0.4], [0.4, 0.5, 1.4]])
XYZ = np.stack([BASE, BASE * 1.3 + [0.2, -0.1, 0.5], BASE + [0.3, 0.2, -0.4]])


def system(form="molsys", unit="nm"):
    structures = Structures(
        coordinates=puw.convert(puw.quantity(XYZ.copy(), "nm"), to_unit=unit),
        box=puw.quantity(np.tile(np.eye(3) * 5, (3, 1, 1)), "nm"),
    )
    if form == "structures":
        return structures
    source = MolSys(n_atoms=4)
    source.structures = structures
    source.interactions = {
        "evaluated": msm.Interactions.from_records(
            [],
            n_atoms=4,
            n_structures=3,
            evaluated_structure_indices=[0, 1, 2],
            method="synthetic_reflection_guard",
        )
    }
    return source


def values(source, attribute="coordinates"):
    return puw.get_value(msm.get(source, **{attribute: True}), to_unit="nm")


@pytest.mark.parametrize("form", ["molsys", "structures"])
@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize(
    "normal,scale",
    [
        ([1, 0, 0], 2),
        ([2, 3, -1], 1),
        ([2, 3, -1], -2),
        ([2, 3, -1], 1e300),
        ([2, 3, -1], 1e-300),
    ],
)
def test_scaled_normal_reflection_preserves_plane_distances_scope_and_ownership(
    form, in_place, unit, normal, scale
):
    source = system(form, unit)
    before, box = values(source).copy(), values(source, "box").copy()
    vector = np.array(normal, dtype=float) * scale
    vector_before = vector.copy()
    point_nm = np.array([0.2, -0.3, 0.4])
    point = puw.convert(puw.quantity(point_nm, "nm"), to_unit=unit)
    point_before = puw.get_value(point).copy()
    n = np.array(normal, dtype=float)
    n /= np.linalg.norm(n)
    householder = np.eye(3) - 2 * np.outer(n, n)
    expected = before.copy()
    for index in [2, 0]:
        expected[index, [1, 3]] = (
            before[index, [1, 3]] - point_nm
        ) @ householder + point_nm
    analysis = source.interactions["evaluated"] if isinstance(source, MolSys) else None
    with puw.context(standard_units=[unit, "ps", "radians"]):
        result = msm.structure.flip(
            source,
            vector=vector,
            point=point,
            selection=[3, 1, 3],
            structure_indices=[2, 0, 2],
            in_place=in_place,
        )
    output = source if in_place else result
    assert result is None if in_place else result is not source
    np.testing.assert_allclose(values(output), expected, atol=1e-12, rtol=0)
    np.testing.assert_allclose(
        np.linalg.norm(values(output)[:, 1] - values(output)[:, 3], axis=1),
        np.linalg.norm(before[:, 1] - before[:, 3], axis=1),
        atol=1e-12,
    )
    np.testing.assert_array_equal(values(output, "box"), box)
    np.testing.assert_array_equal(vector, vector_before)
    np.testing.assert_array_equal(puw.get_value(point), point_before)
    if isinstance(output, MolSys):
        np.testing.assert_array_equal(
            output.interactions["evaluated"].evaluated_structure_indices, [1]
        )
        np.testing.assert_array_equal(analysis.evaluated_structure_indices, [0, 1, 2])
    if not in_place:
        np.testing.assert_array_equal(values(source), before)
        if analysis is not None:
            assert source.interactions["evaluated"] is analysis


@pytest.mark.parametrize("in_place", [False, True])
def test_default_normal_reflects_z_and_double_reflection_restores_coordinates(in_place):
    source = system()
    expected = XYZ.copy()
    expected[..., 2] *= -1
    result = msm.structure.flip(source, in_place=in_place)
    output = source if in_place else result
    np.testing.assert_array_equal(values(output), expected)
    restored = msm.structure.flip(output)
    np.testing.assert_array_equal(values(restored), XYZ)
    # The signed tetrahedral volume changes sign, while its magnitude is fixed.
    original_volume = np.linalg.det(XYZ[0, 1:] - XYZ[0, 0])
    mirrored_volume = np.linalg.det(expected[0, 1:] - expected[0, 0])
    np.testing.assert_allclose(mirrored_volume, -original_volume)


@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize(
    "arguments",
    [
        {"vector": [0, 0, 0]},
        {"vector": [np.nan, 0, 1]},
        {"vector": [np.inf, 1, 0]},
        {"vector": [1 + 2j, 0, 0]},
        {"point": "[nan, 0, 0] nm"},
        {"point": "[inf, 0, 0] nm"},
        {"point": "[[0, 0, 0], [1, 0, 0]] nm"},
        {"point": None},
    ],
)
def test_invalid_plane_rejects_before_coordinate_or_interaction_publication(
    in_place, arguments
):
    source = system()
    before, box = values(source).copy(), values(source, "box").copy()
    analysis = source.interactions["evaluated"]
    with pytest.raises(msm.ArgumentError):
        msm.structure.flip(source, in_place=in_place, **arguments)
    np.testing.assert_array_equal(values(source), before)
    np.testing.assert_array_equal(values(source, "box"), box)
    assert source.interactions["evaluated"] is analysis
    np.testing.assert_array_equal(analysis.evaluated_structure_indices, [0, 1, 2])


def test_offset_plane_points_are_fixed_and_double_reflection_is_identity():
    source = system("structures")
    vector, point = [2, 3, -1], [0.2, -0.3, 0.4]
    first = msm.structure.flip(source, vector=vector, point=puw.quantity(point, "nm"))
    second = msm.structure.flip(first, vector=vector, point=puw.quantity(point, "nm"))
    np.testing.assert_allclose(values(second), XYZ, atol=1e-12, rtol=0)
    anchor = Structures(coordinates=puw.quantity([[point]], "nm"))
    fixed = msm.structure.flip(anchor, vector=vector, point=puw.quantity(point, "nm"))
    np.testing.assert_allclose(values(fixed), [[point]], atol=1e-12, rtol=0)


@pytest.mark.parametrize("value", [np.nan, np.inf, 1 + 2j])
def test_nonfinite_quantity_point_rejects_before_publication(value):
    source = system()
    before = values(source).copy()
    analysis = source.interactions["evaluated"]
    with pytest.raises(msm.ArgumentError):
        msm.structure.flip(
            source, point=puw.quantity([value, 0, 0], "nm"), in_place=True
        )
    np.testing.assert_array_equal(values(source), before)
    assert source.interactions["evaluated"] is analysis
