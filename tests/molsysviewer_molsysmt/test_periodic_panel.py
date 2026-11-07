"""Periodic GUI admission and image truth through actual owner/host adapters."""

import numpy as np
import pytest

import molsysmt as msm
from tests.molsysviewer_molsysmt.test_geometry_panel import act, coords
from tests.molsysviewer_molsysmt.test_geometry_panel import case as case
from tests.molsysviewer_molsysmt.test_pbc_edit_tools import cell, nearest, wrapped

puw = msm.pyunitwizard


def _prepare(view, *, skew=False, varying=False):
    boxes = np.repeat(cell(skew)[None], 3, axis=0)
    if varying:
        boxes *= np.array([1.0, 1.1, 0.8])[:, None, None]
    values = coords(view) + [8.0, 7.0, 6.0]
    view.addons.molsysmt.basic.set(
        box=puw.quantity(boxes, "nm"), coordinates=puw.quantity(values, "nm")
    )
    analysis = msm.Interactions.from_records(
        [],
        n_atoms=view.molsys.get_n_atoms(),
        n_structures=3,
        evaluated_structure_indices=[0, 1, 2],
        method="gui.periodic.receiving",
    )
    view.interactions.attach(analysis, name="scope", assume_aligned=True)
    return values, boxes, view.addons.molsysmt.get_sync_status()["target_revision"]


def _apply(view, sent, parameters, *, draft=None):
    reviewed = act(
        view, sent, "review", draft=draft or {"source": "all"}, parameters=parameters
    )
    assert reviewed["stage"] == "review", reviewed["message"]
    applied = act(view, sent, "apply", token=reviewed["review"]["token"])
    assert applied["stage"] == (
        "result" if parameters.get("effect") == "result" else "done"
    ), applied["message"]
    return applied


def _output(view, packet, effect):
    return (
        view.addons.manager.presentations.get(packet["result"]["id"])
        if effect == "result"
        else view
    )


@pytest.mark.parametrize("mode", ["primary", "centered", "nearest"])
@pytest.mark.parametrize("skew", [False, True])
@pytest.mark.parametrize("varying", [False, True])
@pytest.mark.parametrize("effect", ["update", "result"])
def test_gui_atomwise_periodic_images_match_lattice_truth(
    case, mode, skew, varying, effect
):
    view, sent = case
    before, boxes, revision = _prepare(view, skew=skew, varying=varying)
    atoms = [2, 4]
    origin = np.array([0.2, -0.4, 0.7])
    expected = before.copy()
    method = "wrap_to_mic" if mode == "nearest" else "wrap_to_pbc"
    for frame in [2, 0]:
        expected[frame, atoms] = wrapped(
            before[frame, atoms],
            boxes[frame],
            method,
            origin,
            centered=mode == "centered",
        )
    with puw.context(standard_units=["pm", "ps", "radians"]):
        packet = _apply(
            view,
            sent,
            {
                "task": "wrap",
                "wrap_mode": mode,
                "wrap_compact": "atom",
                "ox": "2",
                "oy": "-4",
                "oz": "7",
                "origin_unit": "angstrom",
                "structures": "indices",
                "indices": "2,0",
                "effect": effect,
            },
            draft={"source": "indices", "indices": "2,4"},
        )
    output = _output(view, packet, effect)
    np.testing.assert_allclose(coords(output), expected, atol=4e-12, rtol=0)
    np.testing.assert_array_equal(
        puw.get_value(output.molsys.structures.box, to_unit="nm"), boxes
    )
    np.testing.assert_array_equal(
        output.molsys.interactions["scope"].evaluated_structure_indices, [1]
    )
    if effect == "result":
        np.testing.assert_array_equal(coords(view), before)
        np.testing.assert_array_equal(
            view.molsys.interactions["scope"].evaluated_structure_indices, [0, 1, 2]
        )
        assert packet["result"]["operation"] == "molsysmt.pbc." + method
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision + int(
        effect == "update"
    )


@pytest.mark.parametrize("mode", ["primary", "centered", "nearest"])
@pytest.mark.parametrize("skew", [False, True])
@pytest.mark.parametrize("effect", ["update", "result"])
def test_gui_component_default_reconstructs_the_real_peptide(case, mode, skew, effect):
    view, sent = case
    original, boxes, _ = _prepare(view, skew=skew)
    split = np.stack(
        [wrapped(points, boxes[i], "wrap_to_pbc") for i, points in enumerate(original)]
    )
    view.addons.molsysmt.basic.set(coordinates=puw.quantity(split, "nm"))
    expected = split.copy()
    method = "wrap_to_mic" if mode == "nearest" else "wrap_to_pbc"
    for frame in [2, 0]:
        centroid = original[frame].mean(axis=0)
        target = wrapped(
            centroid[None], boxes[frame], method, centered=mode == "centered"
        )[0]
        expected[frame] = original[frame] - centroid + target
    packet = _apply(
        view,
        sent,
        {
            "task": "wrap",
            "wrap_mode": mode,
            "structures": "indices",
            "indices": "2,0",
            "effect": effect,
        },
    )
    output = _output(view, packet, effect)
    np.testing.assert_allclose(coords(output), expected, atol=5e-12, rtol=0)
    np.testing.assert_array_equal(coords(output)[1], split[1])
    if effect == "result":
        np.testing.assert_array_equal(coords(view), split)


@pytest.mark.parametrize("skew", [False, True])
@pytest.mark.parametrize("effect", ["update", "result"])
def test_gui_temporal_unwrap_uses_fixed_cell_and_explicit_sequence(case, skew, effect):
    view, sent = case
    original, boxes, revision = _prepare(view, skew=skew)
    offsets = np.array([[0.1, 0.1, 0.1], [0.7, 0.15, 0.2], [0.9, 0.2, 0.3]]) @ boxes[0]
    data = original - original[:, :1] + offsets[:, None]
    data = np.stack(
        [wrapped(points, boxes[i], "wrap_to_pbc") for i, points in enumerate(data)]
    )
    view.addons.molsysmt.basic.set(coordinates=puw.quantity(data, "nm"))
    revision = view.addons.molsysmt.get_sync_status()["target_revision"]
    atoms = [2, 4, 7]
    expected = data.copy()
    expected[0, atoms] = data[2, atoms] + nearest(
        data[0, atoms] - data[2, atoms], boxes[0]
    )
    with puw.context(standard_units=["angstrom", "ps", "radians"]):
        packet = _apply(
            view,
            sent,
            {
                "task": "unwrap",
                "structures": "indices",
                "indices": "2,0",
                "effect": effect,
            },
            draft={"source": "indices", "indices": "2,4,7"},
        )
    output = _output(view, packet, effect)
    np.testing.assert_allclose(coords(output), expected, atol=4e-12, rtol=0)
    # Selected coordinates pass the native angstrom/nm conversion even for the
    # first temporal sample; anchoring is numerical, not a bitwise guarantee.
    np.testing.assert_allclose(
        coords(output)[2, atoms], data[2, atoms], atol=1e-14, rtol=0
    )
    others = np.setdiff1d(np.arange(view.molsys.get_n_atoms()), atoms)
    np.testing.assert_array_equal(coords(output)[:, others], data[:, others])
    np.testing.assert_array_equal(coords(output)[1], data[1])
    np.testing.assert_array_equal(
        puw.get_value(output.molsys.structures.box, to_unit="nm"), boxes
    )
    if effect == "result":
        np.testing.assert_array_equal(coords(view), data)
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision + int(
        effect == "update"
    )


@pytest.mark.parametrize("task", ["wrap", "unwrap"])
@pytest.mark.parametrize("problem", ["missing", "rotated", "singular"])
def test_gui_periodic_missing_or_unreceived_box_rejects_without_science(
    case, task, problem
):
    view, sent = case
    _prepare(view)
    if problem == "missing":
        box = None
    elif problem == "rotated":
        box = puw.quantity(
            np.repeat(
                np.array([[0.0, 3, 0], [-4.0, 0, 0], [0, 0, 5.0]])[None], 3, axis=0
            ),
            "nm",
        )
    else:
        box = puw.quantity(np.zeros((3, 3, 3)), "nm")
    view.addons.molsysmt.basic.set(box=box)
    before, revision = (
        coords(view),
        view.addons.molsysmt.get_sync_status()["target_revision"],
    )
    packet = act(
        view, sent, "review", draft={"source": "all"}, parameters={"task": task}
    )
    if problem == "singular":
        assert packet["stage"] == "review"
        packet = act(view, sent, "apply", token=packet["review"]["token"])
    assert packet["stage"] == "error", packet
    np.testing.assert_array_equal(coords(view), before)
    status = view.addons.molsysmt.get_sync_status()
    assert status["state"] == "synchronized" and status["target_revision"] == revision
    assert not view.addons.manager.presentations.records()


def test_gui_temporal_varying_cell_remains_explicitly_unreceived(case):
    view, sent = case
    before, _, revision = _prepare(view, varying=True)
    failed = act(
        view, sent, "review", draft={"source": "all"}, parameters={"task": "unwrap"}
    )
    assert failed["stage"] == "error" and "unchanged" in failed["message"]
    np.testing.assert_array_equal(coords(view), before)
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision


@pytest.mark.parametrize(
    "parameters",
    [
        {"ox": "nan"},
        {"origin_unit": "ps"},
        {"wrap_compact": "molecule"},
        {"wrap_mode": "other"},
        {"task": "unwrap", "structures": "current"},
        {"task": "unwrap", "structures": "indices", "indices": "0"},
    ],
)
def test_gui_periodic_invalid_inputs_are_not_implicit_defaults(case, parameters):
    view, sent = case
    before, _, revision = _prepare(view)
    failed = act(
        view,
        sent,
        "review",
        draft={"source": "all"},
        parameters={"task": "wrap", **parameters},
    )
    assert failed["stage"] == "error"
    np.testing.assert_array_equal(coords(view), before)
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision


@pytest.mark.parametrize(
    "change", [{"wrap_mode": "nearest"}, {"ox": "1"}, {"wrap_compact": "atom"}]
)
def test_gui_periodic_parameters_expire_confirmation(case, change):
    view, sent = case
    before, _, revision = _prepare(view)
    parameters = {"task": "wrap"}
    reviewed = act(view, sent, "review", draft={"source": "all"}, parameters=parameters)
    assert reviewed["stage"] == "review"
    failed = act(
        view,
        sent,
        "apply",
        token=reviewed["review"]["token"],
        parameters={**parameters, **change},
    )
    assert failed["stage"] == "error" and "expired" in failed["message"]
    np.testing.assert_array_equal(coords(view), before)
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision


@pytest.mark.parametrize("task", ["wrap", "unwrap"])
def test_gui_periodic_projection_recovery_does_not_repeat_science(
    case, task, monkeypatch
):
    view, sent = case
    before, boxes, revision = _prepare(view)
    review = act(
        view,
        sent,
        "review",
        draft={"source": "all"},
        parameters={"task": task, "wrap_compact": "atom"},
    )
    assert review["stage"] == "review"
    rebuild = view._rebuild_view_from_current_molsys

    def fail(*args, **kwargs):
        raise RuntimeError("Injected projection failure after native periodic science")

    monkeypatch.setattr(view, "_rebuild_view_from_current_molsys", fail)
    packet = act(view, sent, "apply", token=review["review"]["token"])
    assert packet["stage"] == "sync_required"
    completed = coords(view)
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision + 1
    monkeypatch.setattr(view, "_rebuild_view_from_current_molsys", rebuild)
    view._handle_frontend_event(
        {"event": "interaction_context_action", "action": "sync_system_edits"}
    )
    np.testing.assert_array_equal(coords(view), completed)
    status = view.addons.molsysmt.get_sync_status()
    assert (
        status["state"] == "synchronized" and status["target_revision"] == revision + 1
    )
