"""Receiving coordinate-only queries and declared native coordinate assignment."""

import re
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import NotWithThisFormError


@pytest.mark.parametrize("units", [["nm", "ps"], ["pm", "fs"]])
@pytest.mark.parametrize("rank", [1, 2, 3])
def test_explicit_atom_query_and_direct_assignment_preserve_physical_axes(units, rank):
    shape = (3,) if rank == 1 else (3, 3) if rank == 2 else (2, 3, 3)
    values = np.arange(np.prod(shape), dtype=float).reshape(shape) + 0.25
    pose = puw.quantity(values, "angstrom")
    original = puw.get_value(pose).copy()
    canonical = values.reshape(1, 1, 3) if rank == 1 else values.reshape(-1, 3, 3)
    with puw.context(standard_units=units):
        assert msm.get_form(pose) == "XYZ"
        coordinates = msm.get(pose, element="atom", coordinates=True)
        assert coordinates.shape == canonical.shape
        np.testing.assert_allclose(
            puw.get_value(coordinates, to_unit="angstrom"), canonical
        )
        molsys = msm.convert(
            puw.quantity(np.zeros(canonical.shape), "nm"), to_form="molsysmt.MolSys"
        )
        for value in (pose, coordinates):
            msm.set(molsys, coordinates=value)
            actual = msm.get(molsys, element="atom", coordinates=True)
            np.testing.assert_allclose(
                puw.get_value(actual, to_unit="angstrom"), canonical
            )
        np.testing.assert_array_equal(puw.get_value(pose), original)
        assert puw.get_unit(pose) == puw.unit("angstrom")


@pytest.mark.parametrize("units", [["nm", "ps"], ["pm", "fs"]])
def test_selected_xyz_query_retains_nonconsecutive_order_and_repetitions(units):
    values = np.arange(36, dtype=float).reshape(4, 3, 3) + 0.5
    pose = puw.quantity(values, "angstrom")
    with puw.context(standard_units=units):
        result = msm.get(
            pose,
            element="atom",
            selection=[2, 0, 2],
            structure_indices=[3, 1, 3],
            coordinates=True,
        )
        np.testing.assert_allclose(
            puw.get_value(result, to_unit="angstrom"), values[[3, 1, 3]][:, [2, 0, 2]]
        )
        empty = msm.get(pose, element="atom", structure_indices=[], coordinates=True)
        assert empty.shape == (0, 3, 3)


def test_default_system_xyz_coordinates_refuse_without_mutating_the_source():
    pose = puw.quantity(np.arange(9, dtype=float).reshape(3, 3), "angstrom")
    original = puw.get_value(pose).copy()
    with pytest.raises(NotWithThisFormError, match="get_coordinates_from_system"):
        msm.get(pose, coordinates=True)
    np.testing.assert_array_equal(puw.get_value(pose), original)


@pytest.mark.parametrize("shape", [(), (2,), (2, 4), (1, 1, 1, 3)])
def test_unsupported_shapes_are_not_xyz(shape):
    assert not msm.is_form(puw.quantity(np.zeros(shape), "nm"), "XYZ")


def test_bare_arrays_and_nonlength_quantities_are_not_xyz():
    assert not msm.is_form(np.zeros((2, 3)), "XYZ")
    assert not msm.is_form(puw.quantity(np.zeros((2, 3)), "ps"), "XYZ")


@pytest.mark.parametrize("units", [["nm", "ps"], ["pm", "fs"]])
def test_coordinate_delivery_recipe_runs_with_literal_axes_and_units(units):
    page = (
        Path(__file__).resolve().parents[3]
        / "docs/content/user/cookbook/delivering_coordinates.md"
    )
    blocks = re.findall(r"```python\n(.*?)```", page.read_text(), re.S)
    assert len(blocks) == 2
    namespace = {}
    with puw.context(standard_units=units):
        for block in blocks:
            exec(compile(block, str(page), "exec"), namespace)
        actual = puw.get_value(namespace["actual"], to_unit="angstrom")
        assert actual.shape == (2, 2, 3)
        np.testing.assert_allclose(actual[0], 0.0)
        np.testing.assert_allclose(actual[1], [[1, 2, 3], [4, 5, 6]])
        np.testing.assert_allclose(
            puw.get_value(namespace["selected"], to_unit="angstrom")[0],
            [[4, 5, 6], [1, 2, 3]],
        )
