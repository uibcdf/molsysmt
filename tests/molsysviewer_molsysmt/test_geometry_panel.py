"""Analytic translation checks through actual provider/host panel routing."""

import molsysviewer as msv
import numpy as np
import pytest

import molsysmt as msm

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


def state(sent, endpoint=None):
    return [
        m["content"]["state"]
        for m in sent
        if m.get("op") == "addon_panel_message"
        and m.get("target_endpoint_id") == endpoint
        and m.get("content", {}).get("type") == "state"
    ][-1]


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
            sent = []
            view.widget.send = lambda content, buffers=None: sent.append(content)
            view._ready = True
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
@pytest.mark.parametrize("task", ["translate", "center", "fit"])
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


def test_projection_retry_does_not_repeat_native_translation(case, monkeypatch):
    view, sent = case
    packet = act(
        view,
        sent,
        "review",
        draft={"source": "all"},
        parameters={"dx": "1", "unit": "nm"},
    )
    rebuild = view._rebuild_view_from_current_molsys

    def reject_projection(*args, **kwargs):
        raise RuntimeError("Injected scene projection failure after real translation")

    before = coords(view)
    monkeypatch.setattr(view, "_rebuild_view_from_current_molsys", reject_projection)
    result = act(view, sent, "apply", token=packet["review"]["token"])
    assert result["stage"] == "sync_required"
    np.testing.assert_allclose(coords(view), before + [1, 0, 0])
    revision = view.addons.molsysmt.get_sync_status()["target_revision"]
    monkeypatch.setattr(view, "_rebuild_view_from_current_molsys", rebuild)
    view._handle_frontend_event(
        {"event": "interaction_context_action", "action": "sync_system_edits"}
    )
    np.testing.assert_allclose(coords(view), before + [1, 0, 0])
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
