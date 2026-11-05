"""Check row-vector cell membership and complete reference water molecules."""

from collections import Counter
from importlib import import_module
from importlib.resources import files

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError

SKEWED = np.array([[2.0, 0.0, 0.0], [0.7, 1.8, 0.0], [0.3, 0.2, 1.7]])
BOXES = [
    SKEWED,
    np.array([[2.0, 0.0, 0.0], [-0.7, 1.8, 0.0], [0.3, -0.2, 1.7]]),
    np.array([[0.0, 2.0, 0.0], [-1.8, 0.7, 0.0], [-0.2, 0.3, 1.7]]),
    2 * np.eye(3),
]


def reference_water_coordinates():
    # Parse the bundled reference independently of the GRO adapter under test.
    lines = files("molsysmt.data.gro").joinpath("spc216.gro").read_text().splitlines()
    return np.array(
        [
            [float(line[start : start + 8]) for start in (20, 28, 36)]
            for line in lines[2:-1]
        ]
    ).reshape(216, 3, 3)


@pytest.mark.parametrize("matrix", BOXES)
def test_oxygen_sites_belong_to_requested_row_vector_cell(matrix):
    box = puw.quantity(matrix.copy(), "nm")
    result = msm.build.make_water_box(box)
    coordinates = puw.get_value(result.structures.coordinates, to_unit="nm")
    n_waters = msm.get(result, n_waters=True)
    assert n_waters > 0
    assert coordinates.shape == (1, 3 * n_waters, 3)
    oxygen = coordinates[0, ::3]
    # Independent solve: B.T f.T = r.T for boxes whose vectors are rows.
    fractional = np.linalg.solve(matrix.T, oxygen.T).T
    assert np.all(fractional >= -1e-12), fractional.min(axis=0)
    assert np.all(fractional < 1 + 1e-12), fractional.max(axis=0)
    np.testing.assert_array_equal(
        puw.get_value(result.structures.box, to_unit="nm"), matrix[None]
    )
    assert (
        result.topology.atoms["atom_name"].tolist() == ["OW", "HW1", "HW2"] * n_waters
    )
    np.testing.assert_array_equal(
        result.topology.atoms["group_index"], np.repeat(np.arange(n_waters), 3)
    )
    bonds = result.chemical_states.get_bonds()
    assert bonds[["atom1_index", "atom2_index"]].values.tolist() == [
        pair
        for i in range(n_waters)
        for pair in ([3 * i, 3 * i + 1], [3 * i, 3 * i + 2])
    ]
    # Translation must preserve each reference O-H-H geometry, including H
    # outside the primary cell. Independent atom wrapping would break this.
    vectors = coordinates[0].reshape(-1, 3, 3)[:, 1:] - oxygen[:, None]
    reference = reference_water_coordinates()
    reference_vectors = reference[:, 1:] - reference[:, :1]
    allowed = {tuple(row) for row in np.round(reference_vectors.reshape(-1, 6), 9)}
    assert all(tuple(row) in allowed for row in np.round(vectors.reshape(-1, 6), 9))


def test_binary_fractional_boundary_fixture_keeps_only_complete_inside_waters(
    monkeypatch,
):
    matrix = np.array([[1.0, 0.0, 0.0], [0.25, 1.0, 0.0], [0.125, 0.25, 1.0]])
    # Known Cartesian points: origin, two interiors, three negative fractional
    # axes, and the three excluded upper faces. The first negative point still
    # has positive Cartesian coordinates and cannot be rejected by an XYZ box.
    oxygen = np.array(
        [
            [0.0, 0.0, 0.0],
            [0.34375, 0.3125, 0.25],
            [1.03125, 0.9375, 0.75],
            [0.0625, 0.625, 0.5],
            [0.53125, 0.0, 0.5],
            [0.609375, 0.46875, -0.125],
            [1.0, 0.0, 0.0],
            [0.25, 1.0, 0.0],
            [0.125, 0.25, 1.0],
        ]
    )
    template_oxygen = np.repeat([[-0.5, -0.5, -0.5]], 216, axis=0)
    template_oxygen[: len(oxygen)] = oxygen
    offsets = np.array([[0.0, 0.0, 0.0], [-0.05, 0.05, 0.0], [0.0, -0.05, 0.05]])
    factory = import_module("molsysmt.build.make_water_box")
    monkeypatch.setattr(
        factory,
        "_load_reference_tile",
        lambda: ((template_oxygen[:, None] + offsets).reshape(-1, 3), 1.86206),
    )
    result = msm.build.make_water_box(puw.quantity(matrix, "nm"))
    expected = (oxygen[:3, None] + offsets).reshape(1, 9, 3)
    np.testing.assert_allclose(
        puw.get_value(result.structures.coordinates, to_unit="nm"),
        expected,
        atol=2e-16,
        rtol=0,
    )
    assert msm.get(result, n_waters=True, n_bonds=True) == [3, 6]


def test_reported_cell_contains_every_reference_lattice_site_from_scalar_oracle():
    expected = []
    # A deliberately wider reference lattice than the factory's Cartesian
    # bounding box. Solve this lower-triangular cell analytically, without its
    # matrix inverse or tiling counts, to check both inclusion and completeness.
    for x, y, z in reference_water_coordinates()[:, 0] + 1.86206 / 2:
        for i in range(-1, 4):
            for j in range(-1, 4):
                for k in range(-1, 4):
                    px, py, pz = x + i * 1.86206, y + j * 1.86206, z + k * 1.86206
                    fz = pz / 1.7
                    fy = (py - 0.2 * fz) / 1.8
                    fx = (px - 0.7 * fy - 0.3 * fz) / 2.0
                    if 0 <= fx < 1 and 0 <= fy < 1 and 0 <= fz < 1:
                        expected.append(tuple(np.round([px, py, pz], 9)))
    result = msm.build.make_water_box(puw.quantity(SKEWED, "nm"))
    actual = puw.get_value(result.structures.coordinates, to_unit="nm")[0, ::3]
    assert expected
    assert Counter(map(tuple, np.round(actual, 9))) == Counter(expected)


@pytest.mark.parametrize(
    "input_unit,scale", [("nm", 1.0), ("angstrom", 10.0), ("pm", 1000.0)]
)
@pytest.mark.parametrize("output_unit", ["nm", "angstrom"])
def test_equivalent_input_units_and_active_output_policy(
    input_unit, scale, output_unit
):
    expected = msm.build.make_water_box(puw.quantity(SKEWED, "nm"))
    with puw.context(standard_units=[output_unit, "ps", "radians"]):
        policy = puw.configure.get_standard_units()
        result = msm.build.make_water_box(puw.quantity(SKEWED * scale, input_unit))
        # Native Structures stores canonical nm. Quantity presentation follows
        # the application policy when explicitly standardized at its boundary.
        assert puw.configure.get_standard_units() == policy
        assert puw.get_unit(result.structures.coordinates) == puw.unit("nm")
        assert puw.get_unit(result.structures.box) == puw.unit("nm")
        assert puw.get_unit(puw.standardize(result.structures.coordinates)) == puw.unit(
            output_unit
        )
    np.testing.assert_allclose(
        puw.get_value(result.structures.coordinates, to_unit="nm"),
        puw.get_value(expected.structures.coordinates, to_unit="nm"),
        atol=2e-15,
        rtol=0,
    )
    np.testing.assert_allclose(
        puw.get_value(result.structures.box, to_unit="nm"),
        SKEWED[None],
        atol=5e-16,
        rtol=0,
    )


@pytest.mark.parametrize(
    "matrix",
    [
        np.zeros((3, 3)),
        np.diag([1.0, 1.0, np.nan]),
        np.diag([1.0, 1.0, np.inf]),
        np.repeat(np.eye(3)[None], 2, axis=0),
        np.empty((0, 3, 3)),
        None,
    ],
)
def test_invalid_cell_is_rejected_before_reference_read(matrix, monkeypatch):
    factory = import_module("molsysmt.build.make_water_box")

    def unexpected(*args, **kwargs):
        pytest.fail("Invalid boxes must be rejected before loading reference water.")

    monkeypatch.setattr(factory, "_load_reference_tile", unexpected)
    with pytest.raises((ArgumentError, StructuralInconsistencyError)):
        msm.build.make_water_box(None if matrix is None else puw.quantity(matrix, "nm"))


def test_output_box_does_not_alias_caller_box():
    box = puw.quantity(SKEWED[None].copy(), "nm")
    original = puw.get_value(box, to_unit="nm").copy()
    result = msm.build.make_water_box(box)
    result.structures.box = puw.quantity((3 * np.eye(3))[None], "nm")
    np.testing.assert_array_equal(puw.get_value(box, to_unit="nm"), original)


def test_small_valid_cell_returns_typed_empty_water_system():
    result = msm.build.make_water_box(puw.quantity(0.001 * np.eye(3), "nm"))
    assert result.structures.coordinates.shape == (1, 0, 3)
    assert result.structures.box.shape == (1, 3, 3)
    assert msm.get(
        result, n_atoms=True, n_groups=True, n_waters=True, n_bonds=True
    ) == [0, 0, 0, 0]


@pytest.mark.parametrize("form", ["molsysmt.MolSys", "molsysmt.Structures"])
def test_requested_output_form_is_honored(form):
    result = msm.build.make_water_box(puw.quantity(2 * np.eye(3), "nm"), form=form)
    assert msm.get_form(result) == form
    assert msm.get(result, n_atoms=True) == 804
