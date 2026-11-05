"""Receive explicit water construction without reading or adopting a primary."""

import inspect

import molsysviewer as msv
import numpy as np
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from tests.build.make_water_box.test_cell_membership import (
    BOXES,
    SKEWED,
    reference_water_coordinates,
)
from tests.molsysviewer_molsysmt.test_build_assignment_tools import (
    snapshot,
    unchanged,
)

puw = msm.pyunitwizard


@pytest.mark.parametrize("skip", [False, True])
def test_native_signature_help_digestion_and_explicit_only_inputs(skip):
    with msv.new_view() as view:
        method = view.addons.molsysmt.build.make_water_box
        assert inspect.signature(method) == inspect.signature(msm.build.make_water_box)
        assert method.digestion_plan is not None
        assert "make_water_box" in dir(view.addons.molsysmt.build)
        assert not hasattr(view.addons.molsysmt, "make_water_box")
        doc = inspect.getdoc(method)
        for parameter in inspect.signature(method).parameters:
            assert f"{parameter} :" in doc
        for phrase in (
            "explicit scientific inputs",
            "An open empty view is sufficient",
            "without replacing view.molsys",
            "no update_view control",
            "packing",
            "force-field",
        ):
            assert phrase in doc
        box = puw.quantity(2 * np.eye(3), "nm")
        for extra in ("molecular_system", "in_place", "update_view", "selection"):
            with pytest.raises(TypeError if skip else UnknownArgumentError):
                method(box, skip_digestion=skip, **{extra: None})


@pytest.mark.parametrize("matrix", BOXES)
@pytest.mark.parametrize("skip", [False, True])
def test_requested_cell_and_intact_reference_water_geometry(matrix, skip):
    with msv.new_view() as view:
        before = snapshot(view)
        result = view.addons.molsysmt.build.make_water_box(
            puw.quantity(matrix[None].copy() if skip else matrix.copy(), "nm"),
            skip_digestion=skip,
        )
        unchanged(view, before)
    xyz = puw.get_value(result.structures.coordinates, to_unit="nm")[0]
    oxygen = xyz[::3]
    fractional = np.linalg.solve(matrix.T, oxygen.T).T
    assert len(oxygen) > 0
    assert np.all(fractional >= -1e-12)
    assert np.all(fractional < 1 + 1e-12)
    np.testing.assert_array_equal(
        puw.get_value(result.structures.box, to_unit="nm"), matrix[None]
    )
    reference = reference_water_coordinates()
    allowed = {
        tuple(row)
        for row in np.round((reference[:, 1:] - reference[:, :1]).reshape(-1, 6), 9)
    }
    vectors = xyz.reshape(-1, 3, 3)[:, 1:] - oxygen[:, None]
    assert all(tuple(row) in allowed for row in np.round(vectors.reshape(-1, 6), 9))
    assert msm.get(result, n_waters=True, n_bonds=True) == [
        len(oxygen),
        2 * len(oxygen),
    ]
    assert result.topology.atoms["atom_name"].tolist() == ["OW", "HW1", "HW2"] * len(
        oxygen
    )
    bonds = result.chemical_states.get_bonds()
    assert bonds[["atom1_index", "atom2_index"]].values.tolist() == [
        pair
        for i in range(len(oxygen))
        for pair in ([3 * i, 3 * i + 1], [3 * i, 3 * i + 2])
    ]


@pytest.mark.parametrize(
    "input_unit,scale", [("nm", 1), ("angstrom", 10), ("pm", 1000)]
)
@pytest.mark.parametrize("presentation_unit", ["nm", "angstrom"])
def test_equivalent_units_native_parity_and_unchanged_unit_policy(
    input_unit, scale, presentation_unit
):
    native = msm.build.make_water_box(puw.quantity(SKEWED, "nm"))
    with msv.new_view() as view:
        with puw.context(standard_units=[presentation_unit, "ps", "radians"]):
            policy = puw.configure.get_standard_units()
            result = view.addons.molsysmt.build.make_water_box(
                puw.quantity(SKEWED[None] * scale, input_unit)
            )
            assert puw.configure.get_standard_units() == policy
            for field in ("coordinates", "box"):
                value = getattr(result.structures, field)
                assert puw.get_unit(value) == puw.unit("nm")
                assert puw.get_unit(puw.standardize(value)) == puw.unit(
                    presentation_unit
                )
                np.testing.assert_allclose(
                    puw.get_value(value, to_unit="nm"),
                    puw.get_value(getattr(native.structures, field), to_unit="nm"),
                    atol=2e-15,
                    rtol=0,
                )


@pytest.mark.parametrize("state", ["empty", "loaded", "pending"])
def test_factory_preserves_owner_scene_and_pending_work_and_returns_owned_output(state):
    view = msv.new_view() if state == "empty" else msv.demo["dialanine"]
    with view:
        if state != "empty":
            view.regions.add(selection=[0], tag="keep")
            view.shapes.add_sphere(atom_indices=[0], tag="anchor")
        if state == "pending":
            view.addons.molsysmt.basic.set(
                box=puw.quantity((3 * np.eye(3))[None], "nm"), update_view=False
            )
            assert view.addons.molsysmt.get_sync_status()["state"] == "pending"
        before = snapshot(view)
        box = puw.quantity(SKEWED[None].copy(), "nm")
        result = view.addons.molsysmt.build.make_water_box(box)
        result.structures.box = puw.quantity((4 * np.eye(3))[None], "nm")
        result.structures.coordinates = result.structures.coordinates + puw.quantity(
            1, "nm"
        )
        np.testing.assert_array_equal(puw.get_value(box, to_unit="nm"), SKEWED[None])
        unchanged(view, before)
    assert msm.get(result, n_waters=True) > 0


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "box",
    [
        None,
        puw.quantity(np.zeros((3, 3)), "nm"),
        puw.quantity(np.diag([1.0, 1.0, np.nan]), "nm"),
        puw.quantity(np.diag([1.0, 1.0, np.inf]), "nm"),
        puw.quantity(np.repeat(np.eye(3)[None], 2, axis=0), "nm"),
        puw.quantity(np.empty((0, 3, 3)), "nm"),
        puw.quantity(np.eye(3), "ps"),
    ],
)
def test_native_rejections_preserve_owner(box, skip):
    with msv.new_view() as view:
        before = snapshot(view)
        with pytest.raises(Exception) as native_error:
            msm.build.make_water_box(box, skip_digestion=skip)
        with pytest.raises(type(native_error.value)):
            view.addons.molsysmt.build.make_water_box(box, skip_digestion=skip)
        unchanged(view, before)


@pytest.mark.parametrize("form", ["molsysmt.MolSys", "molsysmt.Structures"])
def test_output_form_is_native_and_result_is_not_loaded(form):
    with msv.new_view() as view:
        result = view.addons.molsysmt.build.make_water_box(
            puw.quantity(2 * np.eye(3), "nm"), form=form
        )
        assert msm.get_form(result) == form
        assert msm.get(result, n_atoms=True) == 804
        assert view.molsys is None


def test_typed_empty_output_from_small_valid_cell():
    with msv.new_view() as view:
        result = view.addons.molsysmt.build.make_water_box(
            puw.quantity(0.001 * np.eye(3), "nm")
        )
    assert result.structures.coordinates.shape == (1, 0, 3)
    assert result.structures.box.shape == (1, 3, 3)
    assert msm.get(
        result, n_atoms=True, n_groups=True, n_waters=True, n_bonds=True
    ) == [
        0,
        0,
        0,
        0,
    ]


def test_skipping_digestion_keeps_native_normalized_input_requirement():
    box = puw.quantity(np.eye(3), "nm")
    with msv.new_view() as view:
        with pytest.raises(Exception) as native_error:
            msm.build.make_water_box(box, skip_digestion=True)
        with pytest.raises(type(native_error.value)):
            view.addons.molsysmt.build.make_water_box(box, skip_digestion=True)


@pytest.mark.parametrize("skip", [False, True])
def test_cached_factory_rejects_closed_owner_and_keeps_prior_output(skip):
    with msv.new_view() as view:
        factory = view.addons.molsysmt.build.make_water_box
        box = puw.quantity(np.eye(3), "nm")
        result = factory(box)
    with pytest.raises(RuntimeError, match="closed view"):
        factory(box, skip_digestion=skip)
    assert msm.get(result, n_waters=True) > 0


def test_loading_factory_output_is_an_explicit_separate_action():
    with msv.new_view() as view:
        result = view.addons.molsysmt.build.make_water_box(
            puw.quantity(np.eye(3), "nm")
        )
        assert view.molsys is None
        view.load(result)
        assert view.molsys is not None
        assert msm.get(view.molsys, n_waters=True) == msm.get(result, n_waters=True)
