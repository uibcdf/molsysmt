"""Real native selection/removal through the host's routed task panel."""

from copy import deepcopy

import molsysviewer as msv
import numpy as np
import pytest

import molsysmt as msm
from molsysviewer_molsysmt.tools import get_addon

puw = msm.pyunitwizard


def mount(view, *, endpoint=None):
    view._handle_frontend_event(
        {
            "event": "panel_navigate",
            "addon": "molsysmt",
            "panel": "system",
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


def act(
    view, sent, kind, *, draft=None, token=None, endpoint=None, request_id=None, **extra
):
    old = state(sent, endpoint)
    payload = {
        "request_id": old["request_id"] + 1 if request_id is None else request_id,
        "draft": old["draft"] if draft is None else draft,
        **extra,
    }
    if token is not None:
        payload["token"] = token
    view._handle_frontend_event(
        {
            "event": "addon_panel_action",
            "addon": "molsysmt",
            "panel": "system",
            "_panel_endpoint_id": endpoint,
            "content": {"type": "action", "id": kind, "payload": payload},
        }
    )
    return state(sent, endpoint)


def transport(view):
    sent = []
    view.widget.send = lambda content, buffers=None: sent.append(content)
    view._ready = True
    return sent


@pytest.fixture
def case():
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0, 8, 3]) as view:
            view.regions.add(selection=[2, 4], tag="chosen")
            view.selections.add("chosen", atom_indices=[2, 4])
            view.active_selection.set([2, 4])
            sent = transport(view)
            mount(view)
            yield view, sent


def test_workspace_registration_keeps_lazy_expert_api_and_only_real_task(case):
    view, sent = case
    spec = get_addon()
    assert [(w.id, w.title, w.entry_panel) for w in spec.workspaces] == [
        ("molsysmt", "Molecular tools", "system")
    ]
    assert [(p.id, p.title) for p in spec.panels] == [("system", "System")]
    assert "system" not in dir(view.addons.molsysmt)
    assert state(sent)["context"]["has_system"]
    assert state(sent)["context"]["saved"] == ["chosen"]
    assert state(sent)["context"]["regions"] == ["chosen"]
    assert not state(sent).get("review")
    assert list(view.addons.molsysmt.basic.select([2, 4])) == [2, 4]


@pytest.mark.parametrize(
    "draft",
    [
        {"source": "current"},
        {"source": "saved", "value": "chosen"},
        {"source": "region", "value": "chosen"},
        {"source": "expression", "expression": "atom_index in [2,4]"},
        {"source": "indices", "indices": "2, 4 2"},
    ],
)
def test_review_is_read_only_bounded_and_uses_native_indices(case, draft):
    view, sent = case
    before = deepcopy(view.export_state())
    status = view.addons.molsysmt.get_sync_status()
    coordinates = view.molsys.structures.coordinates
    packet = act(view, sent, "review", draft=draft)
    assert packet["stage"] == "review"
    assert packet["review"]["remove_atoms"] == 2
    assert packet["review"]["keep_atoms"] == view.molsys.get_n_atoms() - 2
    assert packet["review"]["n_structures"] == 3
    assert "indices" not in packet["review"]
    assert "coordinates" not in str(packet)
    assert np.shares_memory(
        puw.get_value(view.molsys.structures.coordinates), puw.get_value(coordinates)
    )
    assert view.export_state() == before
    assert view.addons.molsysmt.get_sync_status() == status
    indices = view._active_panel_widget[2]._review.indices
    assert indices.dtype == np.int64 and not indices.flags.writeable


def test_real_tctim_water_removal_applies_to_every_structure():
    with msv.demo["1TCD"] as source:
        with msv.new_view(source.molsys, structure_indices=[0, 0, 0]) as view:
            original = view.molsys
            before = puw.get_value(original.structures.coordinates, to_unit="nm").copy()
            selected = msm.select(original, "group_type=='water'")
            retained = np.setdiff1d(np.arange(original.get_n_atoms()), selected)
            view.regions.add(selection=retained[:3].tolist(), tag="keep")
            view.selections.add("keep", atom_indices=retained[:3].tolist())
            sent = transport(view)
            mount(view)
            review = act(
                view, sent, "review", draft={"source": "category", "value": "water"}
            )
            assert review["review"]["remove_atoms"] == 165
            assert review["review"]["n_groups"] == 165
            result = act(view, sent, "remove", token=review["review"]["token"])
            assert result["stage"] == "done"
            assert view.molsys is original and original.get_n_atoms() == 3818
            assert original.structures.n_structures == 3
            np.testing.assert_array_equal(
                puw.get_value(original.structures.coordinates, to_unit="nm"),
                before[:, retained],
            )
            assert view.regions["keep"].atom_indices == (0, 1, 2)
            assert view.selections["keep"].atom_indices == [0, 1, 2]
            assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


@pytest.mark.parametrize(
    "draft,message",
    [
        ({"source": "none"}, "Choose which atoms"),
        ({"source": "indices", "indices": "0.5"}, "integer"),
        ({"source": "indices", "indices": "99999"}, ""),
        ({"source": "expression", "expression": "all"}, "every atom"),
        ({"source": "saved", "value": "missing"}, "no longer exists"),
        ({"source": "region", "value": "missing"}, "no longer exists"),
        ({"source": "category", "value": "protein"}, "Water or Ions"),
        (
            {
                "source": "indices",
                "indices": "2",
                "context": "index",
                "structure_index": 5,
            },
            "outside",
        ),
        ({"source": "indices", "indices": "2", "unexpected": 1}, "unsupported fields"),
    ],
)
def test_rejections_never_change_data_or_managed_revision(case, draft, message):
    view, sent = case
    before = deepcopy(view.export_state())
    status = view.addons.molsysmt.get_sync_status()
    packet = act(view, sent, "review", draft=draft)
    assert packet["stage"] == "error" and message in packet["message"]
    assert not packet.get("review")
    assert view.export_state() == before
    assert view.addons.molsysmt.get_sync_status() == status


def test_no_matches_do_not_execute_an_edit(case):
    view, sent = case
    before = view.addons.molsysmt.get_sync_status()
    packet = act(view, sent, "review", draft={"source": "category", "value": "water"})
    assert packet["stage"] == "no_matches"
    assert not packet.get("review")
    assert view.addons.molsysmt.get_sync_status() == before


@pytest.mark.parametrize(
    "change", ["replace", "revision", "frame", "draft", "active", "saved", "region"]
)
def test_stale_review_rejects_before_science(case, change):
    view, sent = case
    source = (
        "current"
        if change == "active"
        else "saved"
        if change == "saved"
        else "region"
        if change == "region"
        else "indices"
    )
    draft = {"source": source, "value": "chosen", "indices": "2,4"}
    review = act(view, sent, "review", draft=draft)
    assert review["stage"] == "review"
    if change == "replace":
        view.load(view.molsys.copy(), mode="replace")
    elif change == "revision":
        view.addons.molsysmt.basic.set(
            box=puw.quantity(np.tile(np.eye(3), (3, 1, 1)), "nm"), update_view=False
        )
    elif change == "frame":
        view.player.go_to_structure(1)
    elif change == "active":
        view.active_selection.set([1, 3])
    elif change == "saved":
        view.selections["chosen"].delete()
    elif change == "region":
        view.regions["chosen"].delete()
    else:
        draft = {"source": "indices", "indices": "1,3"}
    count = view.molsys.get_n_atoms()
    revision = view.addons.molsysmt.get_sync_status()["target_revision"]
    result = act(view, sent, "remove", draft=draft, token=review["review"]["token"])
    if change == "revision":
        # The host deliberately rejects all addon commands while projection is pending.
        assert view.addons.molsysmt.get_sync_status()["state"] == "pending"
    else:
        assert result["stage"] == "error"
    assert view.molsys.get_n_atoms() == count
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision


def test_review_is_single_use_and_unknown_actions_cannot_execute_science(case):
    view, sent = case
    packet = act(view, sent, "review", draft={"source": "indices", "indices": "2,4"})
    token = packet["review"]["token"]
    assert act(view, sent, "remove", token=token)["stage"] == "done"
    count = view.molsys.get_n_atoms()
    assert act(view, sent, "remove", token=token)["stage"] == "error"
    assert act(view, sent, "__import__")["stage"] == "error"
    assert view.molsys.get_n_atoms() == count


def test_completed_removal_survives_context_refresh_without_replaying_science(case):
    view, sent = case
    review = act(view, sent, "review", draft={"source": "indices", "indices": "2,4"})
    completed = act(view, sent, "remove", token=review["review"]["token"])
    count = view.molsys.get_n_atoms()
    status = view.addons.molsysmt.get_sync_status()
    for _ in range(3):
        refreshed = act(view, sent, "refresh")
        assert refreshed["stage"] == "done"
        assert refreshed["message"] == completed["message"]
        assert "review" not in refreshed
        assert view.molsys.get_n_atoms() == count
        assert view.addons.molsysmt.get_sync_status() == status


@pytest.mark.parametrize("change", ["draft", "revision", "unmount", "new_action"])
def test_completed_removal_notice_expires_with_its_operation_context(case, change):
    view, sent = case
    review = act(view, sent, "review", draft={"source": "indices", "indices": "2,4"})
    completed = act(view, sent, "remove", token=review["review"]["token"])
    if change == "draft":
        refreshed = act(
            view, sent, "refresh", draft={"source": "indices", "indices": "0"}
        )
    elif change == "revision":
        view.addons.molsysmt.basic.remove(selection=[0], in_place=True)
        refreshed = act(view, sent, "refresh")
    elif change == "unmount":
        view._handle_frontend_event(
            {"event": "panel_unmount", "addon": "molsysmt", "panel": "system"}
        )
        mount(view)
        refreshed = act(view, sent, "refresh")
    else:
        act(view, sent, "review", draft={"source": "indices", "indices": "0"})
        refreshed = act(view, sent, "back")
    assert refreshed["stage"] != "done"
    assert refreshed["message"] != completed["message"]


def test_pending_reconciliation_is_not_repeated_science(case):
    view, sent = case
    view.addons.molsysmt.basic.set(
        box=puw.quantity(np.tile(np.eye(3), (3, 1, 1)), "nm"), update_view=False
    )
    # Recovery uses the existing host control; pending addon actions stay gated.
    before = view.addons.molsysmt.get_sync_status()["target_revision"]
    view._handle_frontend_event(
        {"event": "interaction_context_action", "action": "sync_system_edits"}
    )
    result = act(view, sent, "refresh")
    assert result["context"]["state"] == "synchronized"
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == before


def test_peer_windows_invalidate_each_others_reviews_without_losing_drafts(case):
    view, sent = case
    view._endpoint_transfers.register("peer", "canvas")
    mount(view, endpoint="peer")
    peer = act(
        view,
        sent,
        "review",
        draft={"source": "indices", "indices": "1,3"},
        endpoint="peer",
    )
    main = act(view, sent, "review", draft={"source": "indices", "indices": "2,4"})
    assert peer["review"] and main["review"]
    act(view, sent, "remove", token=main["review"]["token"])
    peer = state(sent, "peer")
    assert not peer.get("review") and peer["draft"]["indices"] == "1,3"
    assert "another window" in peer["message"]


def test_navigation_close_and_persisted_draft_cannot_replay_review(case):
    view, sent = case
    old = view._active_panel_widget[2]
    packet = act(view, sent, "review", draft={"source": "indices", "indices": "2,4"})
    view._handle_frontend_event(
        {"event": "panel_unmount", "addon": "molsysmt", "panel": "system"}
    )
    assert old._review is None and not old._alive
    mount(view)
    assert state(sent)["draft"]["indices"] == "2,4" and not state(sent).get("review")
    count = view.molsys.get_n_atoms()
    old.handle_action(
        view, "remove", {"request_id": 99, "token": packet["review"]["token"]}
    )
    assert view.molsys.get_n_atoms() == count
    current = view._active_panel_widget[2]
    view.close()
    current.handle_action(view, "review", {"request_id": 99})
    assert current._review is None and current._owner is None


def test_empty_view_is_a_context_not_a_failed_panel():
    with msv.new_view() as view:
        sent = transport(view)
        mount(view)
        assert not state(sent)["context"]["has_system"]
        result = act(view, sent, "review", draft={"source": "indices", "indices": "0"})
        assert result["stage"] == "error" and view.molsys is None


def test_explicit_structure_context_is_independent_of_visible_structure(case):
    view, sent = case
    packet = act(
        view,
        sent,
        "review",
        draft={
            "source": "indices",
            "indices": "2,4",
            "context": "index",
            "structure_index": 2,
        },
    )
    assert packet["review"]["selection_structure"] == 2
    view.player.go_to_structure(1)
    count = view.molsys.get_n_atoms()
    assert act(view, sent, "remove", token=packet["review"]["token"])["stage"] == "done"
    assert view.molsys.get_n_atoms() == count - 2
    assert view.molsys.structures.n_structures == 3


def test_foreign_read_lock_rejects_confirmation_without_any_native_write(case):
    from threading import Event, Thread

    view, sent = case
    packet = act(view, sent, "review", draft={"source": "indices", "indices": "2,4"})
    panel = view._active_panel_widget[2]
    entered, release = Event(), Event()
    errors = []

    def hold():
        try:

            def read(target):
                entered.set()
                assert release.wait(10)

            view.addons.manager.system_edits.read(read)
        except BaseException as exc:
            errors.append(exc)

    worker = Thread(target=hold)
    worker.start()
    assert entered.wait(10)
    count = view.molsys.get_n_atoms()
    try:
        panel.handle_action(
            view,
            "remove",
            {
                "request_id": 2,
                "draft": packet["draft"],
                "token": packet["review"]["token"],
            },
        )
        assert state(sent)["stage"] == "error"
        assert state(sent)["context"]["state"] == "busy"
        assert view.molsys.get_n_atoms() == count
    finally:
        release.set()
        worker.join(10)
    assert not worker.is_alive() and not errors
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == 0


def test_projection_failure_exposes_completed_science_and_core_retry_only(
    case, monkeypatch
):
    view, sent = case
    packet = act(view, sent, "review", draft={"source": "indices", "indices": "2,4"})
    rebuild = view._rebuild_view_from_current_molsys

    def fail_projection(*args, **kwargs):
        raise RuntimeError("Injected host projection failure after real native removal")

    # Only the host projection is fault-injected; native scientific publication is real.
    monkeypatch.setattr(view, "_rebuild_view_from_current_molsys", fail_projection)
    count = view.molsys.get_n_atoms()
    result = act(view, sent, "remove", token=packet["review"]["token"])
    assert result["stage"] == "sync_required"
    assert view.molsys.get_n_atoms() == count - 2
    revision = view.addons.molsysmt.get_sync_status()["target_revision"]
    monkeypatch.setattr(view, "_rebuild_view_from_current_molsys", rebuild)
    view._handle_frontend_event(
        {"event": "interaction_context_action", "action": "sync_system_edits"}
    )
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision
    assert view.molsys.get_n_atoms() == count - 2


@pytest.mark.parametrize(
    "task,scope,indices,atoms,structures",
    [
        ("extract", "all", "", 2, 3),
        ("extract", "current", "", 2, 1),
        ("extract", "indices", "2, 0", 2, 2),
        ("copy", "all", "", 62, 3),
    ],
)
def test_independent_result_tasks_preserve_source_and_order(
    case, task, scope, indices, atoms, structures
):
    view, sent = case
    before = puw.get_value(view.molsys.structures.coordinates, to_unit="nm").copy()
    initial = view.addons.molsysmt.get_sync_status()
    act(view, sent, "result.task", task=task)
    draft = {**state(sent)["draft"], "source": "indices", "indices": "2, 4"}
    result_state = act(
        view,
        sent,
        "result.create",
        draft=draft,
        result_draft={
            "structures": scope,
            "indices": indices,
            "title": "Independent result",
        },
    )
    assert result_state["stage"] == "result", result_state
    result = result_state["result"]
    child = view.addons.manager.presentations.get(result["id"])
    assert child.molsys.get_n_atoms() == atoms
    assert child.molsys.structures.n_structures == structures
    assert child.molsys is not view.molsys
    assert view.addons.molsysmt.get_sync_status() == initial
    np.testing.assert_equal(
        puw.get_value(view.molsys.structures.coordinates, to_unit="nm"), before
    )
    if scope == "indices":
        np.testing.assert_equal(
            puw.get_value(child.molsys.structures.coordinates, to_unit="nm"),
            before[[2, 0]][:, [2, 4]],
        )
    repeated = act(
        view,
        sent,
        "result.create",
        draft=draft,
        result_draft={
            "structures": scope,
            "indices": indices,
            "title": "Independent result",
        },
    )
    assert repeated["stage"] == "error"
    assert repeated["result"]["id"] == result["id"]
    closed = act(view, sent, "result.discard")
    assert child.closed
    assert closed["result"] is None


@pytest.mark.parametrize("indices", ["", "0,0", "-1", "3", "0, text"])
def test_result_rejects_invalid_structures_before_preparing_a_view(case, indices):
    view, sent = case
    act(view, sent, "result.task", task="extract")
    draft = {**state(sent)["draft"], "source": "indices", "indices": "2,4"}
    result = act(
        view,
        sent,
        "result.create",
        draft=draft,
        result_draft={"structures": "indices", "indices": indices, "title": ""},
    )
    assert result["stage"] == "error"
    assert result["result"] is None
    assert view.addons.manager.presentations.records() == []


def test_panel_navigation_discards_only_unpresented_results(case):
    view, sent = case
    act(view, sent, "result.task", task="copy")
    result = act(
        view,
        sent,
        "result.create",
        result_draft={"structures": "all", "indices": "", "title": ""},
    )["result"]
    child = view.addons.manager.presentations.get(result["id"])
    view._unmount_addon_panel()
    assert child.closed
    assert view.addons.manager.presentations.records() == []
    mount(view)
    act(view, sent, "result.task", task="copy")
    result = act(
        view,
        sent,
        "result.create",
        result_draft={"structures": "all", "indices": "", "title": ""},
    )["result"]
    child = view.addons.manager.presentations.get(result["id"])
    view.addons.manager.presentations._show(result["id"], "notebook", request=1)
    view._unmount_addon_panel()
    assert not child.closed
    child.close()
