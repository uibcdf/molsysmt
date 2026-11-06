"""Check general row-vector wrapping against independent lattice truth (#607)."""

from itertools import product

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private import rust_backend as kernels
from molsysmt.native import MolSys


def _cell(kind):
    if kind == "quarter-turn":
        return np.array([[0.0, 3, 0], [-4, 0, 0], [0, 0, 5]])
    theta = 0.37
    rotation = np.array(
        [
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1],
        ]
    )
    base = (
        np.diag([3.0, 4, 5])
        if kind == "rotated-orthogonal"
        else np.array([[3.0, 0, 0], [1.2, 4, 0], [0.7, 0.9, 5]])
    )
    return base @ rotation


def _minimum_image(vector, box):
    # Wide independent enumeration around the containing primitive cell.
    fractional = vector @ np.linalg.inv(box)
    translations = np.floor(fractional) + np.array(
        list(product(range(-4, 5), repeat=3))
    )
    candidates = vector - translations @ box
    return candidates[np.argmin(np.einsum("ij,ij->i", candidates, candidates))]


def _wrapped(vector, box, mode):
    if mode == "mic":
        return _minimum_image(vector, box)
    fractional = vector @ np.linalg.inv(box)
    return (
        fractional - np.floor(fractional + (0.5 if mode == "centered" else 0))
    ) @ box


def _system(box, coordinates):
    source = MolSys(n_atoms=coordinates.shape[1])
    source.structures.coordinates = puw.quantity(coordinates, "nm")
    source.structures.box = puw.quantity(
        np.repeat(box[None], len(coordinates), axis=0), "nm"
    )
    return source


def _apply(source, mode, *, in_place=False, compact=False, structure_indices="all"):
    if mode == "mic":
        return msm.pbc.wrap_to_mic(
            source,
            compact=compact,
            in_place=in_place,
            structure_indices=structure_indices,
        )
    options = (
        {"box_center": puw.quantity(np.zeros(3), "nm")} if mode == "centered" else {}
    )
    return msm.pbc.wrap_to_pbc(
        source,
        compact=compact,
        in_place=in_place,
        structure_indices=structure_indices,
        **options,
    )


@pytest.mark.parametrize(
    "kind", ["quarter-turn", "rotated-orthogonal", "rotated-triclinic"]
)
@pytest.mark.parametrize("mode", ["primary", "centered", "mic"])
@pytest.mark.parametrize("unit", ["nm", "pm", "m"])
@pytest.mark.parametrize("in_place", [False, True])
def test_public_wrap_uses_the_actual_row_basis(kind, mode, unit, in_place):
    box = _cell(kind)
    coordinates = np.array(
        [
            # Keep cross-unit assertions away from exact primitive-cell faces;
            # the literal [5, 6, 7] face case has a separate vector guard.
            [[5.1, 6.2, 7.3], [-4.7, 3.8, -2.3]],
            [[1.1, 2.2, 3.3], [6.8, -4.2, 1.7]],
            [[-5.8, 7.3, 6.1], [4.9, 8.2, -7.4]],
        ]
    )
    source = _system(box, coordinates)
    expected = coordinates.copy()
    for s in (2, 0):
        for a in range(2):
            expected[s, a] = _wrapped(coordinates[s, a], box, mode)

    with puw.context(standard_units=[unit, "ps"]):
        returned = _apply(source, mode, in_place=in_place, structure_indices=[2, 0])
    result = source if in_place else returned

    assert (returned is None) == in_place
    actual = puw.get_value(result.structures.coordinates, to_unit="nm")
    np.testing.assert_allclose(actual, expected, rtol=0, atol=1e-11)
    np.testing.assert_array_equal(
        puw.get_value(result.structures.box, to_unit="nm"),
        np.repeat(box[None], 3, axis=0),
    )
    shifts = (coordinates - actual) @ np.linalg.inv(box)
    np.testing.assert_allclose(shifts, np.rint(shifts), rtol=0, atol=1e-11)
    if not in_place:
        np.testing.assert_array_equal(
            puw.get_value(source.structures.coordinates, to_unit="nm"), coordinates
        )


@pytest.mark.parametrize(
    "kind", ["quarter-turn", "rotated-orthogonal", "rotated-triclinic"]
)
@pytest.mark.parametrize("mode", ["primary", "centered", "mic"])
def test_single_vector_kernel_uses_the_general_basis(kind, mode):
    box, vector = _cell(kind), np.array([5.0, 6, 7])
    function = {
        "primary": kernels.wrap_to_pbc_vector_single_structure,
        "centered": kernels.wrap_to_pbc_center_vector_single_structure,
        "mic": kernels.wrap_to_mic_vector_single_structure,
    }[mode]
    np.testing.assert_allclose(
        function(vector, box), _wrapped(vector, box, mode), rtol=0, atol=1e-12
    )


@pytest.mark.parametrize(
    "kind", ["quarter-turn", "rotated-orthogonal", "rotated-triclinic"]
)
@pytest.mark.parametrize("mode", ["primary", "centered", "mic"])
@pytest.mark.parametrize("unit", ["nm", "m"])
def test_covalent_component_reconstruction_keeps_the_observed_row_basis(
    kind, mode, unit
):
    box = _cell(kind)
    # Straddle a cell face with a component center away from that face.
    coordinates = np.array([[[0.96, 0.2, 0.3], [0.08, 0.2, 0.3]]]) @ box
    source = _system(box, coordinates)
    source.chemical_states.add_bonds([[0, 1]])
    whole = coordinates[0].copy()
    whole[1] = whole[0] + _minimum_image(coordinates[0, 1] - coordinates[0, 0], box)
    center = whole.mean(axis=0)
    expected = whole + _wrapped(center, box, mode) - center

    with puw.context(standard_units=[unit, "ps"]):
        result = _apply(source, mode, compact="component")

    np.testing.assert_allclose(
        puw.get_value(result.structures.coordinates, to_unit="nm"),
        expected[None],
        rtol=0,
        atol=1e-11,
    )
