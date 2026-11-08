"""Periodic GUI admission and image truth through actual owner/host adapters."""

import numpy as np
import pytest

import molsysmt as msm
from tests.molsysviewer_molsysmt.test_geometry_panel import act, coords
from tests.molsysviewer_molsysmt.test_geometry_panel import case as case
from tests.molsysviewer_molsysmt.test_pbc_edit_tools import cell, nearest, wrapped

puw = msm.pyunitwizard


def _prepare(view, *, skew=False, varying=False, boxes=None, offsets=None):
    if boxes is None:
        boxes = np.repeat(cell(skew)[None], 3, axis=0)
        if varying:
            boxes *= np.array([1.0, 1.1, 0.8])[:, None, None]
    values = coords(view) + [8.0, 7.0, 6.0]
    if offsets is not None:
        values += np.einsum("si,sij->sj", offsets, boxes)[:, None]
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


def _general_cells():
    # Literal row bases: rotated orthogonal, rotated triclinic, larger orthogonal.
    return np.array(
        [
            [[0.0, 3, 0], [-4, 0, 0], [0, 0, 5]],
            [[0.0, 0, 3], [4, 0, 0.7], [0.6, 5, 0.2]],
            [[0.0, -6, 0], [8, 0, 0], [0, 0, 10]],
        ]
    )


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


@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize("effect", ["update", "result"])
@pytest.mark.parametrize("mode", ["primary", "centered", "nearest"])
@pytest.mark.parametrize("structures", [[2, 0], [1]])
def test_gui_general_wrapping_uses_the_stored_row_basis(
    case, unit, effect, mode, structures
):
    view, sent = case
    before, boxes, revision = _prepare(view, boxes=_general_cells())
    atoms, origin = [2, 4], np.array([0.2, -0.4, 0.7])
    method = "wrap_to_mic" if mode == "nearest" else "wrap_to_pbc"
    expected = before.copy()
    for structure in structures:
        expected[structure, atoms] = wrapped(
            before[structure, atoms],
            boxes[structure],
            method,
            origin,
            centered=mode == "centered",
        )
    with puw.context(standard_units=[unit, "ps", "radians"]):
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
                "indices": ",".join(map(str, structures)),
                "effect": effect,
            },
            draft={"source": "indices", "indices": "2,4"},
        )
    output = _output(view, packet, effect)
    np.testing.assert_allclose(coords(output), expected, atol=5e-12, rtol=0)
    np.testing.assert_array_equal(
        puw.get_value(output.molsys.structures.box, to_unit="nm"), boxes
    )
    np.testing.assert_array_equal(
        output.molsys.interactions["scope"].evaluated_structure_indices,
        sorted(set(range(3)) - set(structures)),
    )
    if effect == "result":
        np.testing.assert_array_equal(coords(view), before)
        np.testing.assert_array_equal(
            view.molsys.interactions["scope"].evaluated_structure_indices, [0, 1, 2]
        )
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision + int(
        effect == "update"
    )


@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize("effect", ["update", "result"])
@pytest.mark.parametrize("structures", [[0, 1, 2], [2, 1, 0], [2, 0]])
def test_gui_general_unwrap_uses_each_previous_selected_cell(
    case, unit, effect, structures
):
    view, sent = case
    before, boxes, revision = _prepare(
        view,
        boxes=_general_cells(),
        offsets=np.array([[0.8, -0.4, 0.3], [-1.2, 0.7, 1.6], [0.4, -1.6, 0.9]]),
    )
    atoms = [2, 4, 7]
    expected, wrong_cell = before.copy(), before.copy()
    for previous, current in zip(structures, structures[1:]):
        expected[current, atoms] = expected[previous, atoms] + nearest(
            before[current, atoms] - expected[previous, atoms], boxes[previous]
        )
        wrong_cell[current, atoms] = wrong_cell[previous, atoms] + nearest(
            before[current, atoms] - wrong_cell[previous, atoms], boxes[current]
        )
    assert np.max(np.abs(expected - wrong_cell)) > 0.1, (
        "The oracle must distinguish previous/current cells."
    )
    with puw.context(standard_units=[unit, "ps", "radians"]):
        packet = _apply(
            view,
            sent,
            {
                "task": "unwrap",
                "structures": "indices",
                "indices": ",".join(map(str, structures)),
                "effect": effect,
            },
            draft={"source": "indices", "indices": "2,4,7"},
        )
    output = _output(view, packet, effect)
    np.testing.assert_allclose(coords(output), expected, atol=5e-12, rtol=0)
    untouched = np.setdiff1d(np.arange(view.molsys.get_n_atoms()), atoms)
    np.testing.assert_array_equal(coords(output)[:, untouched], before[:, untouched])
    np.testing.assert_array_equal(
        puw.get_value(output.molsys.structures.box, to_unit="nm"), boxes
    )
    if effect == "result":
        np.testing.assert_array_equal(coords(view), before)
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision + int(
        effect == "update"
    )


@pytest.mark.parametrize("task", ["wrap", "unwrap"])
@pytest.mark.parametrize("problem", ["missing", "nonfinite", "singular"])
def test_gui_periodic_invalid_box_rejects_before_confirmation_without_writes(
    case, task, problem
):
    view, sent = case
    _prepare(view)
    if problem == "missing":
        box = None
    elif problem == "nonfinite":
        values = np.repeat(np.eye(3)[None], 3, axis=0)
        values[1, 1, 1] = np.nan
        box = puw.quantity(values, "nm")
    else:
        box = puw.quantity(np.zeros((3, 3, 3)), "nm")
    # Inject malformed stored input without projecting it to the scene.
    view.molsys.structures.box = box
    before_status = view.addons.molsysmt.get_sync_status()
    before, revision = (
        coords(view),
        view.addons.molsysmt.get_sync_status()["target_revision"],
    )
    packet = act(
        view, sent, "review", draft={"source": "all"}, parameters={"task": task}
    )
    assert packet["stage"] == "error", packet
    assert {"missing": "stored box", "nonfinite": "finite", "singular": "non-singular"}[
        problem
    ] in packet["message"]
    np.testing.assert_array_equal(coords(view), before)
    status = view.addons.molsysmt.get_sync_status()
    assert status["state"] == before_status["state"]
    assert status["pending_operations"] == before_status["pending_operations"]
    assert status["target_revision"] == revision
    assert not view.addons.manager.presentations.records()


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


def _cell_request(*, length_unit="nm", angle_unit="degree", skew=False, **kwargs):
    lengths = [2.0, 3.0, 4.0]
    angles = [90.0, 90.0, 60.0 if skew else 90.0]
    if length_unit == "angstrom":
        lengths = [10 * v for v in lengths]
    if angle_unit == "radian":
        angles = np.deg2rad(angles).tolist()
    return {
        "task": "cell",
        **{f"cell_{key}": str(value) for key, value in zip(("a", "b", "c"), lengths)},
        **{
            f"cell_{key}": str(value)
            for key, value in zip(("alpha", "beta", "gamma"), angles)
        },
        "cell_length_unit": length_unit,
        "cell_angle_unit": angle_unit,
        **kwargs,
    }


@pytest.mark.parametrize("effect", ["update", "result"])
@pytest.mark.parametrize("standard", ["nm", "pm"])
@pytest.mark.parametrize("length_unit", ["nm", "angstrom"])
@pytest.mark.parametrize("angle_unit", ["degree", "radian"])
@pytest.mark.parametrize(
    "scope,indices,selected",
    [("all", "", [0, 1, 2]), ("current", "", [0]), ("indices", "2,0", [2, 0])],
)
@pytest.mark.parametrize("skew", [False, True])
def test_gui_cell_assignment_preserves_positions_and_owns_its_effect(
    case, effect, standard, length_unit, angle_unit, scope, indices, selected, skew
):
    view, sent = case
    before, boxes, revision = _prepare(view)
    expected = boxes.copy()
    # Closed-form 90/90/gamma cell, including the native six-decimal-nm contract.
    assigned = (
        np.array([[2.0, 0, 0], [1.5, 2.598076, 0], [0, 0, 4]])
        if skew
        else np.diag([2.0, 3, 4])
    )
    expected[selected] = assigned
    with puw.context(standard_units=[standard, "ps", "radians"]):
        packet = _apply(
            view,
            sent,
            _cell_request(
                length_unit=length_unit,
                angle_unit=angle_unit,
                skew=skew,
                effect=effect,
                structures=scope,
                indices=indices,
            ),
            draft={"source": "none"},
        )
    output = _output(view, packet, effect)
    np.testing.assert_array_equal(coords(output), before)
    np.testing.assert_allclose(
        puw.get_value(output.molsys.structures.box, to_unit="nm"),
        expected,
        rtol=0,
        atol=1e-12,
    )
    np.testing.assert_array_equal(
        output.molsys.interactions["scope"].evaluated_structure_indices,
        sorted(set(range(3)) - set(selected)),
    )
    if effect == "result":
        np.testing.assert_array_equal(coords(view), before)
        np.testing.assert_array_equal(
            puw.get_value(view.molsys.structures.box, to_unit="nm"), boxes
        )
        np.testing.assert_array_equal(
            view.molsys.interactions["scope"].evaluated_structure_indices, [0, 1, 2]
        )
        assert output.molsys is not view.molsys
        assert packet["result"]["operation"] == "molsysmt.basic.set"
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision + int(
        effect == "update"
    )


@pytest.mark.parametrize("effect", ["update", "result"])
def test_gui_cell_assignment_initializes_the_complete_missing_box_series(case, effect):
    view, sent = case
    _prepare(view)
    view.addons.molsysmt.basic.set(box=None)
    before = coords(view)
    chemistry = msm.convert(
        view.molsys.chemical_states, to_form="molsysmt.ChemicalStatesDict"
    ).to_dict()
    packet = _apply(view, sent, _cell_request(effect=effect), draft={"source": "none"})
    result = _output(view, packet, effect)
    np.testing.assert_array_equal(coords(result), before)
    np.testing.assert_allclose(
        puw.get_value(result.molsys.structures.box, to_unit="nm"),
        np.tile(np.diag([2.0, 3.0, 4.0]), (3, 1, 1)),
        rtol=0,
        atol=1e-12,
    )
    np.testing.assert_equal(
        msm.convert(
            result.molsys.chemical_states, to_form="molsysmt.ChemicalStatesDict"
        ).to_dict(),
        chemistry,
    )
    if effect == "result":
        assert view.molsys.structures.box is None


@pytest.mark.parametrize(
    "scope,indices", [("current", ""), ("indices", "2,0"), ("indices", "2,0,1")]
)
def test_gui_cell_subset_cannot_invent_missing_boxes_for_other_structures(
    case, scope, indices
):
    view, sent = case
    _prepare(view)
    view.addons.molsysmt.basic.set(box=None)
    revision = view.addons.molsysmt.get_sync_status()["target_revision"]
    before = coords(view)
    packet = act(
        view,
        sent,
        "review",
        parameters=_cell_request(structures=scope, indices=indices),
    )
    assert packet["stage"] == "error" and "All structures" in packet["message"]
    assert view.molsys.structures.box is None
    np.testing.assert_array_equal(coords(view), before)
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision
    assert not view.addons.manager.presentations.records()


@pytest.mark.parametrize(
    "change",
    [
        {"cell_a": "0"},
        {"cell_b": "-1"},
        {"cell_c": "nan"},
        {"cell_a": "inf"},
        {"cell_a": "x"},
        {"cell_alpha": "0"},
        {"cell_beta": "180"},
        {"cell_alpha": "1", "cell_beta": "1", "cell_gamma": "179"},
        {"cell_alpha": "140", "cell_beta": "140", "cell_gamma": "140"},
        {"cell_length_unit": "ps"},
        {"cell_angle_unit": "nm"},
    ],
)
def test_gui_cell_invalid_physics_and_units_reject_before_writes(case, change):
    view, sent = case
    before, boxes, revision = _prepare(view)
    analysis = view.molsys.interactions["scope"]
    packet = act(view, sent, "review", parameters=_cell_request(**change))
    assert packet["stage"] == "error", packet
    assert "review" not in packet
    np.testing.assert_array_equal(coords(view), before)
    np.testing.assert_array_equal(
        puw.get_value(view.molsys.structures.box, to_unit="nm"), boxes
    )
    assert view.molsys.interactions["scope"] is analysis
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision
    assert not view.addons.manager.presentations.records()


def test_gui_cell_review_neither_copies_nor_writes_and_back_expires_it(
    case, monkeypatch
):
    view, sent = case
    before, boxes, revision = _prepare(view)

    def unexpected(*args, **kwargs):
        raise AssertionError("Review must not copy a system or write attributes.")

    with monkeypatch.context() as patch:
        patch.setattr(msm.basic, "copy", unexpected)
        patch.setattr(msm.basic, "set", unexpected)
        reviewed = act(
            view,
            sent,
            "review",
            draft={"source": "expression", "expression": "not a molecular expression"},
            parameters=_cell_request(),
        )
    assert reviewed["stage"] == "review", reviewed["message"]
    assert reviewed["review"]["n_atoms"] == view.molsys.get_n_atoms()
    act(view, sent, "back")
    failed = act(view, sent, "apply", token=reviewed["review"]["token"])
    assert failed["stage"] == "error"
    np.testing.assert_array_equal(coords(view), before)
    np.testing.assert_array_equal(
        puw.get_value(view.molsys.structures.box, to_unit="nm"), boxes
    )
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision


@pytest.mark.parametrize(
    "change",
    [
        {"cell_a": "4"},
        {"cell_gamma": "60"},
        {"cell_length_unit": "angstrom"},
        {"cell_angle_unit": "radian"},
        {"structures": "current"},
        {"effect": "result"},
    ],
)
def test_gui_cell_changed_requests_expire_confirmation(case, change):
    view, sent = case
    before, boxes, revision = _prepare(view)
    reviewed = act(view, sent, "review", parameters=_cell_request())
    assert reviewed["stage"] == "review"
    failed = act(
        view,
        sent,
        "apply",
        parameters=_cell_request(**change),
        token=reviewed["review"]["token"],
    )
    assert failed["stage"] == "error" and "expired" in failed["message"]
    np.testing.assert_array_equal(coords(view), before)
    np.testing.assert_array_equal(
        puw.get_value(view.molsys.structures.box, to_unit="nm"), boxes
    )
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision


def test_gui_cell_projection_retry_does_not_repeat_the_native_write(case, monkeypatch):
    view, sent = case
    before, _, revision = _prepare(view)
    reviewed = act(
        view,
        sent,
        "review",
        parameters=_cell_request(structures="indices", indices="2,0"),
    )
    assert reviewed["stage"] == "review"
    rebuild = view._rebuild_view_from_current_molsys

    def fail(*args, **kwargs):
        raise RuntimeError("Injected projection failure after cell assignment")

    monkeypatch.setattr(view, "_rebuild_view_from_current_molsys", fail)
    packet = act(view, sent, "apply", token=reviewed["review"]["token"])
    assert packet["stage"] == "sync_required", packet
    stored = view.molsys.structures._box
    completed = puw.get_value(view.molsys.structures.box, to_unit="nm").copy()
    coverage = view.molsys.interactions["scope"]
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision + 1
    monkeypatch.setattr(view, "_rebuild_view_from_current_molsys", rebuild)
    view._handle_frontend_event(
        {"event": "interaction_context_action", "action": "sync_system_edits"}
    )
    assert view.molsys.structures._box is stored
    assert view.molsys.interactions["scope"] is coverage
    np.testing.assert_array_equal(
        puw.get_value(view.molsys.structures.box, to_unit="nm"), completed
    )
    np.testing.assert_array_equal(coords(view), before)
    status = view.addons.molsysmt.get_sync_status()
    assert (
        status["state"] == "synchronized" and status["target_revision"] == revision + 1
    )
