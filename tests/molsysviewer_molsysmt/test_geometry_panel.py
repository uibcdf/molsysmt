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
def test_gui_units_and_native_coverage_survive_nondefault_application_policy(
    case, policy
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
    expected[np.ix_([2, 0], [2, 4], range(3))] += [0.1, 0, 0]
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
