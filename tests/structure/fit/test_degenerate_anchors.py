"""Public fit contracts for translated anchors with underdetermined rotations."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.native import Structures

ORIGINS = [[0.0, 0.0, 0.0], [10.961, 1.2027, 2.2746], [-100.0, 200.0, -300.0]]


def _system(points_nm, unit="nm"):
    coordinates = puw.convert(puw.quantity(points_nm, "nm"), to_unit=unit)
    system = Structures(coordinates=coordinates)
    # Keep the requested input unit, independently of the session standard.
    system.coordinates = coordinates
    return system


@pytest.mark.parametrize("origin", ORIGINS)
@pytest.mark.parametrize("order", [[0, 1, 2], [2, 0, 1], [1, 2, 0]])
@pytest.mark.parametrize(
    "units", [("nm", "nm"), ("angstrom", "nm"), ("nm", "angstrom")]
)
@pytest.mark.parametrize("degenerate_side", ["source", "reference"])
@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("precision", ["single", "double"])
def test_translated_coincident_anchors_are_rejected_before_mutation(
    origin, order, units, degenerate_side, in_place, precision
):
    origin = np.asarray(origin)
    degenerate = np.array(
        [origin, origin, origin + [-0.6796666666666666, 0.4689333333333333, 0.17735]]
    )[order]
    assert len(np.unique(degenerate, axis=0)) == 2
    triangle = (origin + np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]))[
        order
    ]
    source = _system(
        [degenerate if degenerate_side == "source" else triangle], units[0]
    )
    reference = _system(
        [degenerate if degenerate_side == "reference" else triangle], units[1]
    )
    source_before = puw.get_value(source.coordinates).copy()
    reference_before = puw.get_value(reference.coordinates).copy()

    expected_selection = (
        "selection_fit" if degenerate_side == "source" else "reference_selection_fit"
    )
    with pytest.raises(StructuralInconsistencyError, match=expected_selection):
        msm.structure.least_rmsd_fit(
            source,
            selection=[0, 1, 2],
            selection_fit=[0, 1, 2],
            reference_molecular_system=reference,
            reference_selection_fit=[0, 1, 2],
            in_place=in_place,
            use_gpu=False,
            precision=precision,
        )

    np.testing.assert_array_equal(puw.get_value(source.coordinates), source_before)
    np.testing.assert_array_equal(
        puw.get_value(reference.coordinates), reference_before
    )


@pytest.mark.parametrize("origin", ORIGINS)
@pytest.mark.parametrize(
    "points", [np.zeros((3, 3)), [[0, 0, 0], [1, 2, 3], [2, 4, 6]]]
)
def test_translated_coincident_and_distinct_collinear_anchors_are_rejected(
    origin, points
):
    source = _system([np.asarray(points) + origin])
    with pytest.raises(StructuralInconsistencyError):
        msm.structure.least_rmsd_fit(source, selection_fit=[0, 1, 2], use_gpu=False)


def test_later_degenerate_structure_prevents_partial_in_place_fitting():
    triangle = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=float)
    degenerate = np.array([[10.961, 1.2027, 2.2746]] * 3)
    degenerate[2] += [-0.6796666666666666, 0.4689333333333333, 0.17735]
    source = _system([triangle + [3, 4, 5], triangle, degenerate])
    reference = _system([triangle])
    before = puw.get_value(source.coordinates).copy()
    fitted = msm.structure.least_rmsd_fit(
        source,
        selection_fit=[0, 1, 2],
        structure_indices=[1, 0],
        reference_molecular_system=reference,
        reference_selection_fit=[0, 1, 2],
        use_gpu=False,
    )
    np.testing.assert_allclose(
        puw.get_value(fitted.coordinates, to_unit="nm")[:2],
        [triangle, triangle],
        rtol=0,
        atol=1e-12,
    )
    with pytest.raises(StructuralInconsistencyError):
        msm.structure.least_rmsd_fit(
            source,
            selection_fit=[0, 1, 2],
            structure_indices=[0, 2],
            reference_molecular_system=reference,
            reference_selection_fit=[0, 1, 2],
            in_place=True,
            use_gpu=False,
        )
    np.testing.assert_array_equal(puw.get_value(source.coordinates), before)


@pytest.mark.parametrize("origin", ORIGINS)
@pytest.mark.parametrize("output_unit", ["nm", "angstrom"])
def test_valid_translated_triangle_fits_with_mixed_forms_and_units(origin, output_unit):
    reference_points = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=float) + origin
    rotation = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=float)
    source_points = reference_points @ rotation.T + [2, -3, 0.5]
    source = {"coordinates": puw.quantity([source_points * 10], "angstrom")}
    reference = _system([reference_points])
    with puw.context(
        standard_units=[output_unit, "ps", "Da", "kelvin", "e", "mole", "radian"]
    ):
        fitted = msm.structure.least_rmsd_fit(
            source,
            selection=[0, 1, 2],
            selection_fit=[0, 1, 2],
            reference_molecular_system=reference,
            reference_selection_fit=[0, 1, 2],
            use_gpu=False,
            precision="double",
        )
        np.testing.assert_allclose(
            puw.get_value(msm.get(fitted, coordinates=True), to_unit="nm"),
            [reference_points],
            rtol=0,
            atol=1e-12,
        )
    np.testing.assert_array_equal(
        puw.get_value(source["coordinates"]), [source_points * 10]
    )
