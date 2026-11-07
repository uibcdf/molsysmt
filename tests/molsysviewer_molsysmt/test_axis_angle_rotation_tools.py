"""Receive explicit native rotation construction without binding molecular data."""

import inspect
from copy import deepcopy

import molsysviewer as msv
import numpy as np
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError

puw = msm.pyunitwizard
NAME = "get_rotation_matrix_from_axis_angle"
QUARTER_TURN_Z = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=float)


def snapshot(view):
    status = view.addons.molsysmt.get_sync_status()
    return (
        view.molsys,
        deepcopy(view.export_state()) if status["state"] != "pending" else None,
        status,
        (list(view.history._undo), list(view.history._redo)),
        deepcopy(view.widget.initial_messages),
    )


def unchanged(view, before):
    target, scene, status, history, messages = before
    assert view.molsys is target
    if scene is not None:
        assert view.export_state() == scene
    assert view.addons.molsysmt.get_sync_status() == status
    assert (view.history._undo, view.history._redo) == history
    assert view.widget.initial_messages == messages


def arguments(skip):
    if skip:
        # The native trusted boundary requires a normalized axis and radians.
        return np.array([0.0, 0.0, 1.0]), np.pi / 2
    return np.array([0.0, 0.0, 2.0]), puw.quantity(90.0, "degree")


@pytest.mark.parametrize("skip", [False, True])
def test_explicit_signature_help_and_open_empty_view(skip):
    with msv.new_view() as view:
        method = getattr(view.addons.molsysmt.structure, NAME)
        assert inspect.signature(method) == inspect.signature(
            getattr(msm.structure, NAME)
        )
        assert method.digestion_plan is not None
        assert NAME in dir(view.addons.molsysmt.structure)
        assert not hasattr(view.addons.molsysmt, NAME)
        for phrase in (
            "explicit scientific inputs",
            "An open empty view is sufficient",
            "not read or synchronized",
            "caller-owned",
        ):
            assert phrase in inspect.getdoc(method)
        before = snapshot(view)
        axis, angle = arguments(skip)
        source_axis = axis.copy()
        result = method(axis, angle, skip_digestion=skip)
        assert type(result) is np.ndarray
        assert result.dtype == np.dtype("float64") and result.shape == (3, 3)
        np.testing.assert_allclose(result, QUARTER_TURN_Z, rtol=0, atol=1e-14)
        np.testing.assert_array_equal(axis, source_axis)
        assert not np.shares_memory(result, axis)
        if not skip:
            assert puw.get_value(angle, to_unit="degree") == 90.0
        unchanged(view, before)


@pytest.mark.parametrize("skip", [False, True])
def test_explicit_factory_preserves_pending_primary_without_read_or_sync(
    skip, monkeypatch
):
    with msv.demo["pentalanine"] as seed:
        with msv.new_view(seed.molsys, structure_indices=[0, 8, 3]) as view:
            view.addons.molsysmt.structure.translate(
                translation=puw.quantity([0.1, 0.0, 0.0], "nm"),
                in_place=True,
                update_view=False,
            )
            assert view.addons.molsysmt.get_sync_status()["state"] == "pending"
            before = snapshot(view)
            scientific = view.molsys.copy()
            coordinator = view.addons.manager.system_edits

            def unexpected(*args, **kwargs):
                raise AssertionError(
                    "Explicit rotation construction must not read or synchronize the primary."
                )

            with monkeypatch.context() as isolated:
                for operation in ("read", "execute", "synchronize"):
                    isolated.setattr(coordinator, operation, unexpected)
                result = getattr(view.addons.molsysmt.structure, NAME)(
                    *arguments(skip), skip_digestion=skip
                )
            np.testing.assert_allclose(result, QUARTER_TURN_Z, rtol=0, atol=1e-14)
            unchanged(view, before)
            assert view.molsys.topology.atoms.equals(scientific.topology.atoms)
            assert view.molsys.chemical_states._inventory_equals(
                scientific.chemical_states
            )
            for field in ("coordinates", "box"):
                actual = getattr(view.molsys.structures, field)
                expected = getattr(scientific.structures, field)
                if expected is None:
                    assert actual is None
                else:
                    np.testing.assert_array_equal(
                        puw.get_value(actual, to_unit="nm"),
                        puw.get_value(expected, to_unit="nm"),
                    )


@pytest.mark.parametrize("skip", [False, True])
def test_bound_factory_rejects_invented_primary_and_edit_controls(skip):
    with msv.new_view() as view:
        method = getattr(view.addons.molsysmt.structure, NAME)
        before = snapshot(view)
        for control in (
            "molecular_system",
            "selection",
            "structure_indices",
            "in_place",
            "update_view",
        ):
            with pytest.raises(TypeError if skip else UnknownArgumentError):
                method(*arguments(skip), skip_digestion=skip, **{control: None})
        unchanged(view, before)


@pytest.mark.parametrize("axis,angle", [([0, 0, 0], "90 degree"), ([0, 0, 1], 90.0)])
def test_native_rejections_preserve_the_empty_view(axis, angle):
    with msv.new_view() as view:
        before = snapshot(view)
        with pytest.raises(ArgumentError):
            getattr(view.addons.molsysmt.structure, NAME)(axis, angle)
        unchanged(view, before)


def test_cached_factory_rejects_closed_owner_and_preserves_returned_matrix():
    view = msv.new_view()
    method = getattr(view.addons.molsysmt.structure, NAME)
    result = method([0, 0, 1], "90 degree")
    view.close()
    with pytest.raises(RuntimeError, match="closed"):
        method([0, 0, 1], "90 degree")
    np.testing.assert_allclose(result, QUARTER_TURN_Z, rtol=0, atol=1e-14)
