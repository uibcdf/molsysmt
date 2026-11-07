"""Analytic coordinate checks through actual provider/host panel routing."""

import molsysviewer as msv
import numpy as np
import pytest

import molsysmt as msm
from tests.molsysviewer_molsysmt.test_system_panel import state, transport

puw = msm.pyunitwizard


def mount(view, panel="geometry", endpoint=None):
    view._handle_frontend_event(
        {
            "event": "panel_navigate",
            "addon": "molsysmt",
            "panel": panel,
            "_panel_endpoint_id": endpoint,
        }
    )
    return view._active_panel_widgets[endpoint][2]


def act(view, sent, action, *, endpoint=None, **payload):
    old = state(sent, endpoint)
    view._handle_frontend_event(
        {
            "event": "addon_panel_action",
            "addon": "molsysmt",
            "panel": "geometry",
            "_panel_endpoint_id": endpoint,
            "content": {
                "type": "action",
                "id": action,
                "payload": {
                    "request_id": old["request_id"] + 1,
                    "draft": old["draft"],
                    "parameters": old["parameters"],
                    **payload,
                },
            },
        }
    )
    return state(sent, endpoint)


@pytest.fixture
def case():
    with msv.demo["pentalanine"] as seed:
        with msv.new_view(seed.molsys, structure_indices=[0, 8, 3]) as view:
            view.selections.add("chosen", atom_indices=[2, 4])
            view.regions.add(selection=[2, 4], tag="chosen")
            view.active_selection.set([2, 4])
            view.addons.molsysmt.basic.set(
                box=puw.quantity(np.tile(np.eye(3) * 5, (3, 1, 1)), "nm")
            )
            sent = transport(view)
            mount(view)
            yield view, sent


def coords(view):
    return puw.get_value(view.molsys.structures.coordinates, to_unit="nm").copy()


@pytest.mark.parametrize(
    "source", ["saved", "current", "region", "indices", "expression", "all"]
)
@pytest.mark.parametrize("effect", ["update", "result"])
def test_translation_has_exact_selection_structure_and_result_ownership(
    case, source, effect
):
    view, sent = case
    before, target = coords(view), view.molsys
    box = puw.get_value(target.structures.box, to_unit="nm").copy()
    revision = view.addons.molsysmt.get_sync_status()["target_revision"]
    draft = {
        "source": source,
        "value": "chosen",
        "indices": "2, 4",
        "expression": "atom_index in [2,4]",
    }
    packet = act(
        view,
        sent,
        "review",
        draft=draft,
        parameters={
            "dx": "1",
            "dy": "-2",
            "dz": "3",
            "unit": "angstrom",
            "structures": "indices",
            "indices": "2, 0",
            "effect": effect,
        },
    )
    assert packet["stage"] == "review", packet["message"]
    assert packet["review"]["structure_indices"] == [2, 0]
    assert "indices" not in packet["review"]
    np.testing.assert_array_equal(coords(view), before)
    expected = before.copy()
    atoms = np.arange(target.get_n_atoms()) if source == "all" else [2, 4]
    expected[np.ix_([2, 0], atoms, range(3))] += [0.1, -0.2, 0.3]
    packet = act(view, sent, "apply", token=packet["review"]["token"])
    assert packet["stage"] == ("done" if effect == "update" else "result"), packet[
        "message"
    ]
    assert view.molsys is target
    if effect == "update":
        np.testing.assert_allclose(coords(view), expected, atol=1e-14)
        assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision + 1
        assert act(view, sent, "refresh")["stage"] == "done"
    else:
        np.testing.assert_array_equal(coords(view), before)
        result = view.addons.manager.presentations.get(packet["result"]["id"])
        np.testing.assert_allclose(coords(result), expected, atol=1e-14)
        assert (
            result.molsys is not target
            and result.molsys.get_n_atoms() == target.get_n_atoms()
        )
        assert result.player.n_structures == 3
        assert not np.shares_memory(
            puw.get_value(result.molsys.structures.coordinates),
            puw.get_value(target.structures.coordinates),
        )
        assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision
        assert packet["result"]["affected_structures"] == [2, 0]
        act(view, sent, "result.discard")
        assert result.closed
    np.testing.assert_array_equal(
        puw.get_value(target.structures.box, to_unit="nm"), box
    )
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


@pytest.mark.parametrize(
    "parameters",
    [
        {"dx": "nan"},
        {"dy": "inf"},
        {"dz": ""},
        {"unit": "ps"},
        {"dx": 1},
        {"structures": "indices", "indices": "0,0"},
        {"structures": "indices", "indices": "3"},
        {"structures": "indices", "indices": ""},
        {"effect": "replace"},
        {"unknown": True},
    ],
)
def test_bad_parameters_reject_before_molecular_or_scene_changes(case, parameters):
    view, sent = case
    before, status = coords(view), view.addons.molsysmt.get_sync_status()
    packet = act(view, sent, "review", draft={"source": "all"}, parameters=parameters)
    assert packet["stage"] == "error"
    assert not packet.get("review")
    np.testing.assert_array_equal(coords(view), before)
    assert view.addons.molsysmt.get_sync_status() == status


@pytest.mark.parametrize(
    "change", ["frame", "selection", "parameters", "back", "replacement"]
)
def test_stale_or_cancelled_translation_never_runs(case, change):
    view, sent = case
    packet = act(
        view,
        sent,
        "review",
        draft={"source": "saved", "value": "chosen"},
        parameters={"dx": "1"},
    )
    assert packet["stage"] == "review", packet["message"]
    if change == "frame":
        view.player.go_to_structure(1)
    elif change == "selection":
        view.selections["chosen"].delete()
        view.selections.add("chosen", atom_indices=[1, 3])
    elif change == "back":
        assert act(view, sent, "back")["stage"] == "select"
    elif change == "replacement":
        view.load(view.molsys.copy(), mode="replace")
    before, status = coords(view), view.addons.molsysmt.get_sync_status()
    extra = {"parameters": {"dx": "2"}} if change == "parameters" else {}
    packet = act(view, sent, "apply", token=packet["review"]["token"], **extra)
    assert packet["stage"] == "error"
    np.testing.assert_array_equal(coords(view), before)
    assert view.addons.molsysmt.get_sync_status() == status


def test_token_is_single_use_and_no_match_is_not_an_edit(case):
    view, sent = case
    packet = act(
        view,
        sent,
        "review",
        draft={"source": "expression", "expression": "atom_name=='DOES_NOT_EXIST'"},
    )
    assert packet["stage"] == "no_matches"
    packet = act(
        view,
        sent,
        "review",
        draft={"source": "all"},
        parameters={"dx": "1", "unit": "nm", "structures": "current"},
    )
    token = packet["review"]["token"]
    before = coords(view)
    assert act(view, sent, "apply", token=token)["stage"] == "done"
    expected = before.copy()
    expected[0] += [1, 0, 0]
    np.testing.assert_allclose(coords(view), expected)
    revision = view.addons.molsysmt.get_sync_status()["target_revision"]
    assert act(view, sent, "apply", token=token)["stage"] == "error"
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision


def test_unmount_discards_unpresented_result_and_restores_only_bounded_draft(case):
    view, sent = case
    packet = act(
        view,
        sent,
        "review",
        draft={"source": "all"},
        parameters={"dx": "1", "effect": "result"},
    )
    result = act(view, sent, "apply", token=packet["review"]["token"])["result"]
    child = view.addons.manager.presentations.get(result["id"])
    mount(view, "system")
    assert child.closed
    mount(view)
    assert state(sent)["parameters"]["dx"] == "1"
    assert not state(sent).get("review") and state(sent)["result"] is None


@pytest.mark.parametrize("policy", ["angstrom", "pm"])
@pytest.mark.parametrize("task", ["translate", "rotate", "center", "fit"])
def test_gui_units_and_native_coverage_survive_nondefault_application_policy(
    case, policy, task
):
    view, sent = case
    analysis = msm.interactions.hbonds.get_buch_hbonds(
        view.molsys,
        structure_indices="all",
        pbc=False,
        output_type="molsysmt.Interactions",
    )
    view.interactions.attach(analysis, name="science", assume_aligned=True)
    before = coords(view)
    with puw.context(standard_units=[policy, "ps", "radians"]):
        packet = act(
            view,
            sent,
            "review",
            draft={"source": "indices", "indices": "2,4"},
            parameters={
                "task": task,
                "fit_expression": "atom_name=='CA'",
                "fit_reference_structure": "1",
                "dx": "1",
                "unit": "angstrom",
                "structures": "indices",
                "indices": "2,0",
            },
        )
        assert packet["stage"] == "review", packet["message"]
        assert (
            act(view, sent, "apply", token=packet["review"]["token"])["stage"] == "done"
        )
    expected = before.copy()
    if task == "translate":
        expected[np.ix_([2, 0], [2, 4], range(3))] += [0.1, 0, 0]
    elif task == "rotate":
        expected = _rotated_z(before, [2, 4], [2, 0], "geometric")
    elif task == "center":
        for frame in [2, 0]:
            expected[frame, [2, 4]] -= before[frame, [2, 4]].mean(axis=0)
    else:
        alpha = np.asarray(
            msm.select(view.molsys, selection="atom_name=='CA'"), dtype=int
        )
        expected = _fitted_coordinates(before, [2, 4], alpha, alpha, [2, 0], 1)
    np.testing.assert_allclose(coords(view), expected)
    np.testing.assert_array_equal(analysis.evaluated_structure_indices, [0, 1, 2])
    np.testing.assert_array_equal(
        view.molsys.interactions["science"].evaluated_structure_indices, [1]
    )


@pytest.mark.parametrize("task", ["translate", "rotate"])
def test_projection_retry_does_not_repeat_native_translation(case, monkeypatch, task):
    view, sent = case
    packet = act(
        view,
        sent,
        "review",
        draft={"source": "all"},
        parameters={"task": task, "dx": "1", "unit": "nm"},
    )
    rebuild = view._rebuild_view_from_current_molsys

    def reject_projection(*args, **kwargs):
        raise RuntimeError("Injected scene projection failure after real translation")

    before = coords(view)
    monkeypatch.setattr(view, "_rebuild_view_from_current_molsys", reject_projection)
    result = act(view, sent, "apply", token=packet["review"]["token"])
    assert result["stage"] == "sync_required"
    expected = (
        before + [1, 0, 0]
        if task == "translate"
        else _rotated_z(before, list(range(before.shape[1])), [0, 1, 2], "geometric")
    )
    np.testing.assert_allclose(coords(view), expected)
    revision = view.addons.molsysmt.get_sync_status()["target_revision"]
    monkeypatch.setattr(view, "_rebuild_view_from_current_molsys", rebuild)
    view._handle_frontend_event(
        {"event": "interaction_context_action", "action": "sync_system_edits"}
    )
    np.testing.assert_allclose(coords(view), expected)
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


def test_geometry_edit_invalidates_system_review_in_a_peer_window(case):
    view, sent = case
    view._endpoint_transfers.register("peer", "canvas")
    peer = mount(view, "system", "peer")
    peer.handle_action(
        view,
        "review",
        {"request_id": 1, "draft": {"source": "indices", "indices": "2,4"}},
    )
    assert peer._review is not None
    packet = act(view, sent, "review", draft={"source": "all"}, parameters={"dx": "1"})
    assert act(view, sent, "apply", token=packet["review"]["token"])["stage"] == "done"
    assert peer._review is None
    assert peer._draft["indices"] == "2,4"
    assert "another window" in state(sent, "peer")["message"]


@pytest.mark.parametrize("effect", ["update", "result"])
@pytest.mark.parametrize("weighting", ["geometric", "masses"])
@pytest.mark.parametrize("destination", ["point", "selection"])
def test_centering_uses_explicit_reference_destination_and_native_frames(
    case, effect, weighting, destination
):
    view, sent = case
    before = coords(view)
    box = puw.get_value(view.molsys.structures.box, to_unit="nm").copy()
    revision = view.addons.molsysmt.get_sync_status()["target_revision"]
    moving, source, target = list(range(10)), [2, 4], [10, 12]
    weights = (
        None
        if weighting == "geometric"
        else puw.get_value(
            msm.physchem.get_mass(view.molsys, element="atom", selection=source),
            to_unit="dalton",
        )
    )
    if weights is not None:
        assert np.ptp(weights) > 0, "The mass-weighting oracle needs unequal masses."
    expected = before.copy()
    for frame in [2, 0]:
        reference = np.average(before[frame, source], weights=weights, axis=0)
        point = (
            np.array([0.1, 0.2, 0.3])
            if destination == "point"
            else before[frame, target].mean(axis=0)
        )
        expected[frame, moving] += point - reference
    parameters = {
        "task": "center",
        "cx": "1",
        "cy": "2",
        "cz": "3",
        "center_unit": "angstrom",
        "center_kind": weighting,
        "source_expression": "atom_index in [2,4]",
        "destination_kind": destination,
        "target_expression": "atom_index in [10,12]",
        "structures": "indices",
        "indices": "2,0",
        "effect": effect,
    }
    with puw.context(standard_units=["pm", "ps", "radians", "dalton"]):
        packet = act(
            view,
            sent,
            "review",
            draft={"source": "indices", "indices": ",".join(map(str, moving))},
            parameters=parameters,
        )
        assert packet["stage"] == "review", packet["message"]
        assert packet["review"]["n_center_atoms"] == 2
        assert packet["review"]["n_target_atoms"] == (
            2 if destination == "selection" else 0
        )
        np.testing.assert_array_equal(coords(view), before)
        result = act(view, sent, "apply", token=packet["review"]["token"])
    assert result["stage"] == ("done" if effect == "update" else "result"), result[
        "message"
    ]
    output = (
        view
        if effect == "update"
        else view.addons.manager.presentations.get(result["result"]["id"])
    )
    np.testing.assert_allclose(coords(output), expected, atol=1e-12)
    np.testing.assert_array_equal(
        puw.get_value(output.molsys.structures.box, to_unit="nm"), box
    )
    if effect == "result":
        np.testing.assert_array_equal(coords(view), before)
        assert result["result"]["operation"] == "molsysmt.structure.center"
        assert result["result"]["effect_label"] == "Centered"
        act(view, sent, "result.discard")
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision + int(
        effect == "update"
    )


@pytest.mark.parametrize(
    "parameters",
    [
        {"center_kind": "charges"},
        {"destination_kind": "implicit"},
        {"center_unit": "ps"},
        {"cx": "nan"},
        {"source_expression": "atom_index==15"},
        {"source_expression": "atom_name=='NOT_AN_ATOM'"},
        {"destination_kind": "selection", "target_expression": ""},
        {
            "destination_kind": "selection",
            "target_expression": "atom_name=='NOT_AN_ATOM'",
        },
    ],
)
def test_centering_rejects_invalid_or_undefined_inputs_before_editing(case, parameters):
    view, sent = case
    before, status = coords(view), view.addons.molsysmt.get_sync_status()
    packet = act(
        view,
        sent,
        "review",
        draft={"source": "indices", "indices": "2,4"},
        parameters={"task": "center", **parameters},
    )
    assert packet["stage"] == "error"
    np.testing.assert_array_equal(coords(view), before)
    assert view.addons.molsysmt.get_sync_status() == status


def test_switching_geometry_task_cannot_reuse_review_or_unpresented_result(case):
    view, sent = case
    review = act(
        view,
        sent,
        "review",
        draft={"source": "all"},
        parameters={"dx": "1", "effect": "result"},
    )
    packet = act(view, sent, "apply", token=review["review"]["token"])
    child = view.addons.manager.presentations.get(packet["result"]["id"])
    changed = act(view, sent, "task", parameters={"task": "center"})
    assert child.closed and changed["result"] is None
    assert act(view, sent, "apply", token=review["review"]["token"])["stage"] == "error"


def test_missing_mass_unit_policy_rejects_before_write_and_can_be_retried(case):
    view, sent = case
    before, status = coords(view), view.addons.molsysmt.get_sync_status()
    parameters = {"task": "center", "center_kind": "masses"}
    with puw.context(standard_units=["pm", "ps", "radians"]):
        packet = act(
            view,
            sent,
            "review",
            draft={"source": "indices", "indices": "0,1,2,3"},
            parameters=parameters,
        )
        assert packet["stage"] == "review"
        failed = act(view, sent, "apply", token=packet["review"]["token"])
        assert failed["stage"] == "error"
        diagnostic = failed["message"]
        for _ in range(2):
            refreshed = act(view, sent, "refresh")
            assert refreshed["stage"] == "error"
            assert refreshed["message"] == diagnostic
            assert "review" not in refreshed
        assert view._active_panel_widgets[None][2]._diagnostic.message == diagnostic
    np.testing.assert_array_equal(coords(view), before)
    rejected = view.addons.molsysmt.get_sync_status()
    for key in (
        "state",
        "target_revision",
        "integration_revision",
        "pending_operations",
        "reason",
    ):
        assert rejected[key] == status[key]
    assert rejected["operation_id"].startswith("molsysmt.structure.center:")
    with puw.context(standard_units=["pm", "ps", "radians", "dalton"]):
        packet = act(view, sent, "review")
        assert (
            act(view, sent, "apply", token=packet["review"]["token"])["stage"] == "done"
        )
    assert (
        view.addons.molsysmt.get_sync_status()["target_revision"]
        == status["target_revision"] + 1
    )


@pytest.mark.parametrize("panel_name", ["system", "geometry"])
@pytest.mark.parametrize(
    "change", ["review", "back", "frame", "draft", "revision", "remount"]
)
def test_task_diagnostic_expires_with_its_inputs_context_or_lifecycle(
    case, panel_name, change
):
    view, sent = case
    mount(view, panel_name)
    panel = view._active_panel_widgets[None][2]
    sequence = 0

    def request(action, **payload):
        nonlocal sequence
        sequence += 1
        panel.handle_action(view, action, {"request_id": sequence, **payload})
        return state(sent)

    failed = request("review", draft={"source": "indices", "indices": "bad"})
    assert failed["stage"] == "error"
    for _ in range(2):
        refreshed = request("refresh")
        assert refreshed["stage"] == "error"
        assert refreshed["message"] == failed["message"]
        assert "review" not in refreshed
    if change in {"review", "draft"}:
        packet = request(
            change if change == "review" else "refresh",
            draft={"source": "indices", "indices": "2,4"},
        )
        assert packet["stage"] == ("review" if change == "review" else "select")
    elif change == "back":
        assert request("back")["stage"] == "select"
    elif change == "frame":
        view.player.go_to_structure(1)
        assert request("refresh")["stage"] == "select"
    elif change == "revision":
        view.addons.molsysmt.structure.translate(
            translation=puw.quantity([0.1, 0, 0], "nm"), in_place=True
        )
        assert request("refresh")["stage"] == "select"
    else:
        panel.on_unmount(view)
        panel.on_mount(view)
        assert state(sent)["stage"] == "select"
    assert panel._diagnostic is None


def test_geometry_diagnostic_does_not_survive_a_new_task_or_parameters(case):
    view, sent = case
    failed = act(
        view, sent, "review", draft={"source": "all"}, parameters={"dx": "bad"}
    )
    assert failed["stage"] == "error"
    assert act(view, sent, "refresh")["stage"] == "error"
    assert act(view, sent, "refresh", parameters={"dx": "1"})["stage"] == "select"
    assert act(view, sent, "review", parameters={"dx": "bad"})["stage"] == "error"
    assert act(view, sent, "task", parameters={"task": "center"})["stage"] == "select"


def _fitted_coordinates(before, moving, fit, reference, frames, reference_frame):
    """Independent unweighted Kabsch oracle; no native fitting helper."""
    expected = before.copy()
    target = before[reference_frame, reference]
    target_center = target.mean(axis=0)
    for frame in frames:
        anchors = before[frame, fit]
        center = anchors.mean(axis=0)
        u, _, vt = np.linalg.svd((anchors - center).T @ (target - target_center))
        proper = np.eye(3)
        proper[-1, -1] = np.linalg.det(u @ vt)
        rotation = u @ proper @ vt
        expected[frame, moving] = (
            before[frame, moving] - center
        ) @ rotation + target_center
    return expected


@pytest.mark.parametrize("effect", ["update", "result"])
@pytest.mark.parametrize("partial", [False, True])
@pytest.mark.parametrize("correspondence", ["moving", "alpha", "explicit"])
def test_superposition_matches_independent_kabsch_with_declared_correspondence(
    case, effect, partial, correspondence
):
    view, sent = case
    before, target = coords(view), view.molsys
    box = puw.get_value(target.structures.box, to_unit="nm").copy()
    moving = list(range(10 if partial else target.get_n_atoms()))
    alpha = np.asarray(
        msm.select(target, selection="atom_name=='CA'"), dtype=int
    ).tolist()
    fit, reference = moving, moving
    parameters = {
        "task": "fit",
        "fit_reference_structure": "1",
        "structures": "indices",
        "indices": "2,0",
        "effect": effect,
    }
    if correspondence != "moving":
        fit = alpha if correspondence == "alpha" else alpha[:3]
        reference = fit if correspondence == "alpha" else alpha[1:4]
        parameters["fit_expression"] = f"atom_index in {fit}"
        if correspondence == "explicit":
            parameters["fit_reference_expression"] = f"atom_index in {reference}"
    expected = _fitted_coordinates(before, moving, fit, reference, [2, 0], 1)
    revision = view.addons.molsysmt.get_sync_status()["target_revision"]
    with puw.context(standard_units=["pm", "ps", "radians", "dalton"]):
        reviewed = act(
            view,
            sent,
            "review",
            draft={"source": "indices", "indices": ",".join(map(str, moving))},
            parameters=parameters,
        )
        assert reviewed["stage"] == "review", reviewed["message"]
        assert reviewed["review"]["n_fit_atoms"] == len(fit)
        assert reviewed["review"]["reference_structure"] == 1
        np.testing.assert_array_equal(coords(view), before)
        applied = act(view, sent, "apply", token=reviewed["review"]["token"])
    assert applied["stage"] == ("done" if effect == "update" else "result"), applied[
        "message"
    ]
    output = (
        view
        if effect == "update"
        else view.addons.manager.presentations.get(applied["result"]["id"])
    )
    np.testing.assert_allclose(coords(output), expected, atol=1e-10)
    np.testing.assert_array_equal(coords(output)[1], before[1])
    np.testing.assert_array_equal(
        puw.get_value(output.molsys.structures.box, to_unit="nm"), box
    )
    if partial:
        np.testing.assert_array_equal(coords(output)[:, 10:], before[:, 10:])
    if effect == "result":
        np.testing.assert_array_equal(coords(view), before)
        assert output.molsys is not target
        assert applied["result"]["operation"] == "molsysmt.structure.least_rmsd_fit"
        assert applied["result"]["effect_label"] == "Superposed"
        act(view, sent, "result.discard")
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision + int(
        effect == "update"
    )


@pytest.mark.parametrize(
    "parameters",
    [
        {"fit_reference_structure": "-1"},
        {"fit_reference_structure": "3"},
        {"fit_reference_structure": "nan"},
        {"fit_reference_structure": "0.5"},
        {"fit_reference_structure": ""},
        {"fit_reference_structure": 0},
        {"fit_expression": "atom_index == 0"},
        {"fit_expression": "atom_index == 999"},
        {"fit_reference_expression": "atom_index in [0,1,2]"},
        {"fit_reference_expression": "atom_index == 999"},
    ],
)
def test_superposition_rejects_invalid_reference_requests_before_editing(
    case, parameters
):
    view, sent = case
    before, revision = (
        coords(view),
        view.addons.molsysmt.get_sync_status()["target_revision"],
    )
    packet = act(
        view,
        sent,
        "review",
        draft={"source": "all"},
        parameters={"task": "fit", **parameters},
    )
    assert packet["stage"] == "error"
    np.testing.assert_array_equal(coords(view), before)
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision
    assert not view.addons.manager.presentations.records()


def test_superposition_validates_all_structure_geometry_before_any_native_write(case):
    view, sent = case
    # A later degenerate structure must not leave an earlier valid one fitted.
    anchors = np.asarray(
        msm.select(view.molsys, selection="atom_name=='CA'"), dtype=int
    )[:3]
    changed = coords(view)
    changed[2, anchors] = [[0, 0, 0], [1, 0, 0], [2, 0, 0]]
    view.addons.molsysmt.basic.set(coordinates=puw.quantity(changed, "nm"))
    before, revision = (
        coords(view),
        view.addons.molsysmt.get_sync_status()["target_revision"],
    )
    review = act(
        view,
        sent,
        "review",
        draft={"source": "all"},
        parameters={
            "task": "fit",
            "fit_expression": f"atom_index in {anchors.tolist()}",
            "fit_reference_structure": "1",
            "structures": "indices",
            "indices": "0,2",
        },
    )
    assert review["stage"] == "review"
    failed = act(view, sent, "apply", token=review["review"]["token"])
    assert failed["stage"] == "error" and "non-collinear" in failed["message"]
    np.testing.assert_array_equal(coords(view), before)
    status = view.addons.molsysmt.get_sync_status()
    assert status["state"] == "synchronized" and status["target_revision"] == revision
    assert act(view, sent, "refresh")["message"] == failed["message"]
    assert "review" not in state(sent)


def test_superposition_projection_retry_preserves_completed_native_fit(
    case, monkeypatch
):
    view, sent = case
    before = coords(view)
    atoms = list(range(view.molsys.get_n_atoms()))
    expected = _fitted_coordinates(before, atoms, atoms, atoms, [2, 0], 1)
    review = act(
        view,
        sent,
        "review",
        draft={"source": "all"},
        parameters={
            "task": "fit",
            "fit_reference_structure": "1",
            "structures": "indices",
            "indices": "2,0",
        },
    )
    rebuild = view._rebuild_view_from_current_molsys

    def reject_projection(*args, **kwargs):
        raise RuntimeError("Injected projection failure after the actual native fit")

    monkeypatch.setattr(view, "_rebuild_view_from_current_molsys", reject_projection)
    failed = act(view, sent, "apply", token=review["review"]["token"])
    assert failed["stage"] == "sync_required"
    np.testing.assert_allclose(coords(view), expected, atol=1e-10)
    revision = view.addons.molsysmt.get_sync_status()["target_revision"]
    monkeypatch.setattr(view, "_rebuild_view_from_current_molsys", rebuild)
    view._handle_frontend_event(
        {"event": "interaction_context_action", "action": "sync_system_edits"}
    )
    np.testing.assert_allclose(coords(view), expected, atol=1e-10)
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision


@pytest.mark.parametrize(
    "change",
    [
        {"fit_reference_structure": "2"},
        {"fit_expression": "atom_name=='CA'"},
        {"fit_reference_expression": "atom_name=='CA'"},
    ],
)
def test_superposition_reference_changes_expire_the_single_use_review(case, change):
    view, sent = case
    before, revision = (
        coords(view),
        view.addons.molsysmt.get_sync_status()["target_revision"],
    )
    parameters = {"task": "fit", "fit_reference_structure": "1"}
    reviewed = act(view, sent, "review", draft={"source": "all"}, parameters=parameters)
    assert reviewed["stage"] == "review"
    rejected = act(
        view,
        sent,
        "apply",
        token=reviewed["review"]["token"],
        parameters={**parameters, **change},
    )
    assert rejected["stage"] == "error" and "expired" in rejected["message"]
    np.testing.assert_array_equal(coords(view), before)
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision


def _rotated_z(before, atoms, structures, center_kind, sign=1):
    """Independent signed quarter turn, without the matrix construction under test."""
    expected = before.copy()
    for structure in structures:
        center = (
            before[structure, atoms].mean(axis=0)
            if center_kind == "geometric"
            else np.array([0.1, -0.2, 0.3])
            if center_kind == "point"
            else np.zeros(3)
        )
        relative = before[structure, atoms] - center
        expected[structure, atoms, 0] = center[0] - sign * relative[:, 1]
        expected[structure, atoms, 1] = center[1] + sign * relative[:, 0]
    return expected


@pytest.mark.parametrize(
    "source", ["saved", "current", "region", "indices", "expression", "all"]
)
@pytest.mark.parametrize("effect", ["update", "result"])
@pytest.mark.parametrize("center_kind", ["geometric", "origin", "point"])
def test_rotation_centers_selection_order_units_and_independent_ownership(
    case, source, effect, center_kind, monkeypatch
):
    view, sent = case
    target, before = view.molsys, coords(view)
    box = puw.get_value(target.structures.box, to_unit="nm").copy()
    revision = view.addons.molsysmt.get_sync_status()["target_revision"]
    calls = []
    native_center = msm.structure.get_center

    def center(*args, **kwargs):
        calls.append(kwargs)
        if effect == "update":
            assert view.addons.molsysmt.get_sync_status()["state"] == "editing"
        result = native_center(*args, **kwargs)
        assert puw.get_value(result).shape == (2, 1, 3)
        return result

    monkeypatch.setattr(msm.structure, "get_center", center)
    with puw.context(standard_units=["pm", "ps", "radians"]):
        packet = act(
            view,
            sent,
            "review",
            draft={
                "source": source,
                "value": "chosen",
                "indices": "2,4,2",
                "expression": "atom_index in [2,4]",
            },
            parameters={
                "task": "rotate",
                "rotation_center_kind": center_kind,
                "cx": "1",
                "cy": "-2",
                "cz": "3",
                "center_unit": "angstrom",
                "structures": "indices",
                "indices": "2,0",
                "effect": effect,
            },
        )
        assert packet["stage"] == "review", packet["message"]
        assert packet["review"]["structure_indices"] == [2, 0]
        assert not calls, "Review must not calculate structure-dependent centers."
        np.testing.assert_array_equal(coords(view), before)
        packet = act(view, sent, "apply", token=packet["review"]["token"])
    assert packet["stage"] == ("done" if effect == "update" else "result"), packet[
        "message"
    ]
    atoms = list(range(target.get_n_atoms())) if source == "all" else [2, 4]
    expected = _rotated_z(before, atoms, [2, 0], center_kind)
    assert len(calls) == int(center_kind == "geometric")
    if calls:
        assert calls[0]["selection"] == atoms
        assert calls[0]["structure_indices"] == [2, 0]
        assert calls[0]["weights"] is None
    output = (
        view
        if effect == "update"
        else view.addons.manager.presentations.get(packet["result"]["id"])
    )
    np.testing.assert_allclose(coords(output), expected, atol=1e-12)
    np.testing.assert_array_equal(
        puw.get_value(output.molsys.structures.box, to_unit="nm"), box
    )
    assert view.molsys is target
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision + int(
        effect == "update"
    )
    if effect == "result":
        np.testing.assert_array_equal(coords(view), before)
        assert output.player.n_structures == 3
        assert not np.shares_memory(
            puw.get_value(output.molsys.structures.coordinates),
            puw.get_value(target.structures.coordinates),
        )
        assert packet["result"]["operation"] == "molsysmt.structure.rotate"
        assert packet["result"]["effect_label"] == "Rotated"
        assert packet["result"]["affected_structures"] == [2, 0]
        act(view, sent, "result.discard")
        assert output.closed


@pytest.mark.parametrize(
    "parameters",
    [
        {"ax": "0", "ay": "0", "az": "0"},
        {"ax": "nan"},
        {"az": "inf"},
        {"angle": "nan"},
        {"angle": "inf"},
        {"angle": ""},
        {"angle": 90},
        {"angle_unit": "nm"},
        {"rotation_center_kind": "camera"},
        {"ax": "x"},
        {"rotation_center_kind": "point", "cx": "nan"},
    ],
)
def test_rotation_rejects_undefined_axis_angle_and_center_before_edit(case, parameters):
    view, sent = case
    before, status = coords(view), view.addons.molsysmt.get_sync_status()
    packet = act(
        view,
        sent,
        "review",
        draft={"source": "all"},
        parameters={"task": "rotate", **parameters},
    )
    assert packet["stage"] == "error"
    assert not packet.get("review")
    np.testing.assert_array_equal(coords(view), before)
    assert view.addons.molsysmt.get_sync_status() == status


@pytest.mark.parametrize("angle,unit", [("-90", "degree"), (str(-np.pi / 2), "radian")])
def test_negative_rotation_and_explicit_angular_units(case, angle, unit):
    view, sent = case
    before = coords(view)
    packet = act(
        view,
        sent,
        "review",
        draft={"source": "indices", "indices": "2,4"},
        parameters={
            "task": "rotate",
            "angle": angle,
            "angle_unit": unit,
            "rotation_center_kind": "origin",
            "structures": "current",
        },
    )
    assert packet["stage"] == "review", packet["message"]
    packet = act(view, sent, "apply", token=packet["review"]["token"])
    assert packet["stage"] == "done", packet["message"]
    np.testing.assert_allclose(
        coords(view), _rotated_z(before, [2, 4], [0], "origin", sign=-1), atol=1e-12
    )


@pytest.mark.parametrize("angle", ["0", "0.000001"])
def test_rotation_does_not_suppress_zero_or_small_requested_edit(case, angle):
    view, sent = case
    before = coords(view)
    revision = view.addons.molsysmt.get_sync_status()["target_revision"]
    packet = act(
        view,
        sent,
        "review",
        draft={"source": "all"},
        parameters={"task": "rotate", "angle": angle, "rotation_center_kind": "origin"},
    )
    assert packet["stage"] == "review", packet["message"]
    assert act(view, sent, "apply", token=packet["review"]["token"])["stage"] == "done"
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision + 1
    if angle == "0":
        np.testing.assert_allclose(coords(view), before, atol=1e-15)
    else:
        assert np.max(np.abs(coords(view) - before)) > 1e-9


@pytest.mark.parametrize("change", ["axis", "angle", "center", "structures", "peer"])
def test_rotation_review_expires_on_scope_parameters_and_peer_edits(case, change):
    view, sent = case
    packet = act(
        view,
        sent,
        "review",
        draft={"source": "indices", "indices": "2,4"},
        parameters={"task": "rotate"},
    )
    assert packet["stage"] == "review", packet["message"]
    patch = {
        "axis": {"az": "-1"},
        "angle": {"angle": "45"},
        "center": {"rotation_center_kind": "origin"},
        "structures": {"structures": "current"},
    }
    if change == "peer":
        view._endpoint_transfers.register("rotation-peer", "canvas")
        mount(view, endpoint="rotation-peer")
        peer = act(
            view,
            sent,
            "review",
            endpoint="rotation-peer",
            draft={"source": "all"},
            parameters={"dx": "1"},
        )
        assert (
            act(
                view,
                sent,
                "apply",
                endpoint="rotation-peer",
                token=peer["review"]["token"],
            )["stage"]
            == "done"
        )
    before, status = coords(view), view.addons.molsysmt.get_sync_status()
    extra = (
        {}
        if change == "peer"
        else {"parameters": {**packet["parameters"], **patch[change]}}
    )
    # Peer invalidations are unsolicited state packets (request_id=0).
    # A real frontend retains its own increasing request sequence.
    result = act(
        view,
        sent,
        "apply",
        token=packet["review"]["token"],
        request_id=packet["request_id"] + 1,
        **extra,
    )
    assert result["stage"] == "error"
    np.testing.assert_array_equal(coords(view), before)
    assert view.addons.molsysmt.get_sync_status() == status


def test_rotation_review_never_copies_a_molecular_trajectory(case, monkeypatch):
    view, sent = case

    def reject_copy(*args, **kwargs):
        raise AssertionError("Review must not copy the molecular trajectory.")

    monkeypatch.setattr(view.molsys, "copy", reject_copy)
    packet = act(
        view,
        sent,
        "review",
        draft={"source": "all"},
        parameters={"task": "rotate", "effect": "result"},
    )
    assert packet["stage"] == "review", packet["message"]
    assert packet["review"]["n_atoms"] == view.molsys.get_n_atoms()
    assert act(view, sent, "back")["stage"] == "select"


@pytest.mark.parametrize("kind", ["inertia", "geometric"])
@pytest.mark.parametrize("weighting", ["uniform", "masses"])
@pytest.mark.parametrize("centered", [False, True])
@pytest.mark.parametrize("custom_basis", [False, True])
@pytest.mark.parametrize("effect", ["update", "result"])
@pytest.mark.parametrize("reference", ["moving", "disjoint"])
def test_principal_axis_panel_matches_independent_tensor_invariants(
    case, kind, weighting, centered, custom_basis, effect, reference
):
    from tests.molsysviewer_molsysmt.test_structure_axes_tools import covariance

    view, sent = case
    target, before = view.molsys, coords(view)
    box = puw.get_value(target.structures.box, to_unit="nm").copy()
    revision = view.addons.molsysmt.get_sync_status()["target_revision"]
    moving = list(range(8))
    fit = moving if reference == "moving" else list(range(10, 16))
    numerical_weights = (
        np.ones(len(fit))
        if weighting == "uniform"
        else puw.get_value(
            msm.physchem.get_mass(target, element="atom", selection=fit),
            to_unit="dalton",
        )
    )
    basis = (
        np.array([[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0]])
        if custom_basis
        else np.eye(3)
    )
    with puw.context(standard_units=["pm", "ps", "radians", "dalton"]):
        packet = act(
            view,
            sent,
            "review",
            draft={"source": "indices", "indices": "0,1,2,3,4,5,6,7,2"},
            parameters={
                "task": "axes",
                "axes_type": kind,
                "axes_weights": weighting,
                "axes_center": "origin" if centered else "preserve",
                "axes_target": "custom" if custom_basis else "cartesian",
                "axes_basis": "0 1 0; 0 0 1; 1 0 0",
                "axes_expression": ""
                if reference == "moving"
                else "atom_index in [10,11,12,13,14,15]",
                "structures": "indices",
                "indices": "2,0",
                "effect": effect,
            },
        )
        assert packet["stage"] == "review", packet["message"]
        assert packet["review"]["n_fit_atoms"] == len(fit)
        assert packet["review"]["structure_indices"] == [2, 0]
        np.testing.assert_array_equal(coords(view), before)
        packet = act(view, sent, "apply", token=packet["review"]["token"])
    assert packet["stage"] == ("done" if effect == "update" else "result"), packet[
        "message"
    ]
    output = (
        view
        if effect == "update"
        else view.addons.manager.presentations.get(packet["result"]["id"])
    )
    after = coords(output)
    unchanged = sorted(set(range(target.get_n_atoms())) - set(moving))
    for structure in [2, 0]:
        center, cov = covariance(before[structure, fit], numerical_weights)
        _, eigenvectors = np.linalg.eigh(cov)
        if kind == "inertia":
            eigenvectors = eigenvectors[:, ::-1]
        projected = (after[structure, moving] - (0 if centered else center)) @ basis.T
        expected = (before[structure, moving] - center) @ eigenvectors
        # Individual eigenvector signs are arbitrary; squared projections and
        # proper rigid geometry independently constrain the published result.
        np.testing.assert_allclose(projected**2, expected**2, atol=1e-11)
        initial = before[structure, moving]
        final = after[structure, moving]
        np.testing.assert_allclose(
            np.linalg.norm(initial[:, None] - initial[None, :], axis=-1),
            np.linalg.norm(final[:, None] - final[None, :], axis=-1),
            atol=1e-12,
        )
        np.testing.assert_allclose(
            np.linalg.det(final[[1, 2, 3]] - final[0]),
            np.linalg.det(initial[[1, 2, 3]] - initial[0]),
            atol=1e-12,
        )
        np.testing.assert_array_equal(
            after[structure, unchanged], before[structure, unchanged]
        )
    np.testing.assert_array_equal(after[1], before[1])
    np.testing.assert_array_equal(
        puw.get_value(output.molsys.structures.box, to_unit="nm"), box
    )
    assert view.molsys is target
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision + int(
        effect == "update"
    )
    if effect == "result":
        np.testing.assert_array_equal(coords(view), before)
        assert output.player.n_structures == 3
        assert (
            packet["result"]["operation"] == "molsysmt.structure.align_principal_axes"
        )
        assert not np.shares_memory(
            puw.get_value(output.molsys.structures.coordinates),
            puw.get_value(target.structures.coordinates),
        )
        act(view, sent, "result.discard")


@pytest.mark.parametrize(
    "parameters",
    [
        {"axes_type": "unknown"},
        {"axes_weights": "charges"},
        {"axes_center": "average"},
        {"axes_target": "camera"},
        {"axes_target": "custom", "axes_basis": "1 0 0"},
        {"axes_target": "custom", "axes_basis": "1 0 0; 0 nan 0; 0 0 1"},
        {"axes_target": "custom", "axes_basis": "identity"},
        {"axes_expression": "atom_name=='DOES_NOT_EXIST'"},
    ],
)
def test_principal_axis_panel_rejects_invalid_requests_during_review(case, parameters):
    view, sent = case
    before, status = coords(view), view.addons.molsysmt.get_sync_status()
    packet = act(
        view,
        sent,
        "review",
        draft={"source": "all"},
        parameters={"task": "axes", **parameters},
    )
    assert packet["stage"] == "error"
    np.testing.assert_array_equal(coords(view), before)
    assert view.addons.molsysmt.get_sync_status() == status


@pytest.mark.parametrize("basis", ["1 0 0; 0 1 0; 0 0 -1", "2 0 0; 0 1 0; 0 0 1"])
def test_native_principal_axis_admission_rejects_bad_bases_before_writes(case, basis):
    view, sent = case
    before, status = coords(view), view.addons.molsysmt.get_sync_status()
    packet = act(
        view,
        sent,
        "review",
        draft={"source": "all"},
        parameters={"task": "axes", "axes_target": "custom", "axes_basis": basis},
    )
    assert packet["stage"] == "review", packet["message"]
    result = act(view, sent, "apply", token=packet["review"]["token"])
    assert result["stage"] == "error", result["message"]
    np.testing.assert_array_equal(coords(view), before)
    current = view.addons.molsysmt.get_sync_status()
    # The coordinator records a new attempted operation, without publishing
    # coordinates, advancing the revision or leaving pending scene work.
    assert current["operation_id"].startswith(
        "molsysmt.structure.align_principal_axes:"
    )
    assert {**current, "operation_id": status["operation_id"]} == status


def test_principal_axis_panel_reviews_without_geometry_or_copy(case, monkeypatch):
    view, sent = case

    def reject(*args, **kwargs):
        raise AssertionError(
            "Review cannot compute principal axes or copy a trajectory."
        )

    monkeypatch.setattr(msm.structure, "get_principal_axes", reject)
    monkeypatch.setattr(view.molsys, "copy", reject)
    packet = act(
        view,
        sent,
        "review",
        draft={"source": "all"},
        parameters={"task": "axes", "effect": "result"},
    )
    assert packet["stage"] == "review", packet["message"]
    assert act(view, sent, "back")["stage"] == "select"


def test_principal_axes_validate_every_structure_before_coordinate_publication(case):
    view, sent = case
    xyz = coords(view)
    xyz[0, :8] = np.column_stack([np.arange(8), np.zeros((8, 2))])
    view.addons.molsysmt.basic.set(coordinates=puw.quantity(xyz, "nm"))
    before, status = coords(view), view.addons.molsysmt.get_sync_status()
    packet = act(
        view,
        sent,
        "review",
        draft={"source": "indices", "indices": "0,1,2,3,4,5,6,7"},
        parameters={"task": "axes", "structures": "indices", "indices": "2,0"},
    )
    assert packet["stage"] == "review", packet["message"]
    result = act(view, sent, "apply", token=packet["review"]["token"])
    assert result["stage"] == "error", result["message"]
    assert "degenerate" in result["message"].lower()
    assert "structure_index 0 (selection position 1)" in result["message"]
    np.testing.assert_array_equal(coords(view), before)
    current = view.addons.molsysmt.get_sync_status()
    # The coordinator records a new attempted operation, without publishing
    # coordinates, advancing the revision or leaving pending scene work.
    assert current["operation_id"].startswith(
        "molsysmt.structure.align_principal_axes:"
    )
    assert {**current, "operation_id": status["operation_id"]} == status


def test_principal_axis_projection_retry_does_not_recalculate(case, monkeypatch):
    view, sent = case
    operation = msm.structure.align_principal_axes
    calls = []

    def align(*args, **kwargs):
        calls.append(kwargs)
        assert view.addons.molsysmt.get_sync_status()["state"] == "editing"
        return operation(*args, **kwargs)

    monkeypatch.setattr(msm.structure, "align_principal_axes", align)
    packet = act(
        view, sent, "review", draft={"source": "all"}, parameters={"task": "axes"}
    )
    assert packet["stage"] == "review", packet["message"]
    rebuild = view._rebuild_view_from_current_molsys

    def reject(*args, **kwargs):
        raise RuntimeError(
            "Injected projection failure after native principal-axis alignment"
        )

    monkeypatch.setattr(view, "_rebuild_view_from_current_molsys", reject)
    assert (
        act(view, sent, "apply", token=packet["review"]["token"])["stage"]
        == "sync_required"
    )
    assert len(calls) == 1 and "skip_digestion" not in calls[0]
    after, status = coords(view), view.addons.molsysmt.get_sync_status()
    monkeypatch.setattr(view, "_rebuild_view_from_current_molsys", rebuild)
    view._handle_frontend_event(
        {"event": "interaction_context_action", "action": "sync_system_edits"}
    )
    assert len(calls) == 1
    np.testing.assert_array_equal(coords(view), after)
    assert (
        view.addons.molsysmt.get_sync_status()["target_revision"]
        == status["target_revision"]
    )
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


@pytest.mark.parametrize("effect", ["update", "result"])
@pytest.mark.parametrize("policy", ["angstrom", "pm"])
def test_principal_axis_publication_preserves_chemistry_boxes_and_scope(
    case, effect, policy
):
    view, sent = case
    original = msm.interactions.hbonds.get_buch_hbonds(
        view.molsys,
        structure_indices="all",
        pbc=False,
        output_type="molsysmt.Interactions",
    )
    view.interactions.attach(original, name="science", assume_aligned=True)
    chemistry = msm.convert(
        view.molsys.chemical_states, to_form="molsysmt.ChemicalStatesDict"
    ).to_dict()
    box = puw.get_value(view.molsys.structures.box, to_unit="nm").copy()
    before = coords(view)
    with puw.context(standard_units=[policy, "ps", "radians", "dalton"]):
        packet = act(
            view,
            sent,
            "review",
            draft={"source": "all"},
            parameters={
                "task": "axes",
                "axes_weights": "masses",
                "structures": "indices",
                "indices": "2,0",
                "effect": effect,
            },
        )
        assert packet["stage"] == "review", packet["message"]
        packet = act(view, sent, "apply", token=packet["review"]["token"])
    assert packet["stage"] == ("done" if effect == "update" else "result"), packet[
        "message"
    ]
    output = (
        view
        if effect == "update"
        else view.addons.manager.presentations.get(packet["result"]["id"])
    )
    np.testing.assert_equal(
        msm.convert(
            output.molsys.chemical_states, to_form="molsysmt.ChemicalStatesDict"
        ).to_dict(),
        chemistry,
    )
    np.testing.assert_array_equal(
        puw.get_value(output.molsys.structures.box, to_unit="nm"), box
    )
    np.testing.assert_array_equal(original.evaluated_structure_indices, [0, 1, 2])
    np.testing.assert_array_equal(
        output.molsys.interactions["science"].evaluated_structure_indices, [1]
    )
    np.testing.assert_array_equal(coords(output)[1], before[1])
    if effect == "result":
        np.testing.assert_array_equal(coords(view), before)
        np.testing.assert_array_equal(
            view.molsys.interactions["science"].evaluated_structure_indices, [0, 1, 2]
        )
        act(view, sent, "result.discard")
