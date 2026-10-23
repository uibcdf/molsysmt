"""Real native removal through the view-bound addon and generic edit receiver."""

import inspect
from copy import deepcopy
from threading import Event, Thread

import molsysviewer as msv
import numpy as np
import pytest
from molsysviewer.widget import MolSysViewerWidget

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError as NativeArgumentError

system_edits = pytest.importorskip(
    "molsysviewer.system_edits",
    reason="Managed edit receiving requires the coordinated source host.",
)
SystemEditPendingError = system_edits.SystemEditPendingError
SystemEditSyncError = system_edits.SystemEditSyncError


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0, 8, 3]) as result:
            yield result


def test_native_independent_default_does_not_adopt_or_rebuild(view):
    original = view.molsys
    state = view.export_state()
    result = view.addons.molsysmt.basic.remove(selection=[0, 2], structure_indices=[1])
    assert result is not original
    assert result.get_n_atoms() == original.get_n_atoms() - 2
    assert result.structures.n_structures == 2
    assert view.molsys is original
    assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


def test_immediate_remove_keeps_bound_identity_handles_maps_and_active_picks(view):
    target = view.molsys
    region = view.regions.add(selection=[0, 2, 4], tag="kept")
    selection = view.selections.add("saved", atom_indices=[2, 4])
    view.active_selection.set([0, 2, 4])
    view.player.go_to_structure(2)
    original = msm.pyunitwizard.get_value(
        target.structures.coordinates, to_unit="nm"
    ).copy()
    source = view.load_blocks[0]

    assert (
        view.addons.molsysmt.remove(
            selection=[0, 1], structure_indices=[1], in_place=True
        )
        is None
    )

    assert view.molsys is target
    assert view.regions["kept"] is region
    assert region.atom_indices == (0, 2)
    assert view.selections["saved"] is selection
    assert view.active_selection.atom_indices == [0, 2]
    expected = msm.get(target, element="atom", selection=[0, 2], group_index=True)
    assert view.active_selection.group_indices == sorted(set(expected))
    assert view.player.index == 1
    assert view.load_blocks[0]["source_id"] == source["source_id"]
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(target.structures.coordinates, to_unit="nm"),
        original[[0, 2], 2:, :],
    )
    assert not view.history.can_undo()
    status = view.addons.molsysmt.get_sync_status()
    assert status["state"] == "synchronized"
    assert status["integration_revision"] == status["target_revision"] == 1


def test_deferred_maps_compose_and_old_index_commands_are_rejected_even_when_skipped(
    view,
):
    tools = view.addons.molsysmt
    region = view.regions.add(selection=[0, 2, 4], tag="kept")
    view.active_selection.set([2, 4])
    original = view.molsys
    tools.remove(selection=[0], in_place=True, update_view=False)
    tools.remove(selection=[0], structure_indices=[1], in_place=True, update_view=False)
    status = tools.get_sync_status()
    assert status["state"] == "pending" and status["pending_operations"] == 2
    status["state"] = "forged"
    assert tools.get_sync_status()["state"] == "pending"
    assert tools.get(n_atoms=True) == original.get_n_atoms()
    assert view._current_molecular_projection is None
    for operation in (
        lambda: region.hide(skip_digestion=True),
        lambda: view.active_selection.set([0], skip_digestion=True),
        lambda: view.shapes.add_sphere(center="[0, 0, 0] nm", skip_digestion=True),
        lambda: view.load(original, mode="replace", skip_digestion=True),
        lambda: view.export_state(skip_digestion=True),
        lambda: view.build_popup_scene_snapshot("canvas", skip_digestion=True),
    ):
        with pytest.raises(SystemEditPendingError):
            operation()
    view._handle_frontend_event(
        {"event": "interaction_active_selection_changed", "atom_indices": [0]}
    )
    assert view._last_active_selection_event["atom_indices"] == [2, 4]
    view._handle_frontend_event({"event": "ready", "capabilities": {}})
    assert view._current_molecular_projection is None

    assert tools.sync_view() is None
    assert view.regions["kept"] is region and region.atom_indices == (0, 2)
    assert view.active_selection.atom_indices == [0, 2]
    assert tools.get_sync_status()["target_revision"] == 2
    assert tools.get_sync_status()["pending_operations"] == 0
    snapshot = view.build_popup_scene_snapshot("canvas")
    assert snapshot[-1]["state"] == "synchronized"


@pytest.mark.parametrize(
    "kwargs",
    [
        {"selection": [999999]},
        {"structure_indices": [3]},
        {"selection": "all"},
        {"structure_indices": "all"},
        {"to_form": "molsysmt.Topology"},
        {"update_view": "yes"},
    ],
)
def test_rejected_removal_does_not_publish_or_block(view, kwargs):
    before = view.export_state()
    domains = view.molsys.topology, view.molsys.structures
    with pytest.raises((TypeError, ValueError, NativeArgumentError)):
        view.addons.molsysmt.remove(in_place=True, **kwargs)
    assert view.molsys.topology is domains[0] and view.molsys.structures is domains[1]
    assert view.export_state() == before
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


def test_noop_keeps_revision_and_existing_pending_edits(view):
    tools = view.addons.molsysmt
    tools.remove(in_place=True)
    assert tools.get_sync_status()["target_revision"] == 0
    tools.remove(selection=[0], in_place=True, update_view=False)
    tools.remove(in_place=True, update_view=False)
    assert tools.get_sync_status()["pending_operations"] == 1
    tools.remove(in_place=True)
    assert tools.get_sync_status()["state"] == "synchronized"


def test_closed_lifetime_two_views_and_explicit_replacement(view):
    tools = view.addons.molsysmt
    with msv.demo["dialanine"] as other:
        other_state = deepcopy(other.export_state())
        tools.remove(selection=[0], in_place=True, update_view=False)
        old = view.molsys
        view.addons.manager.system_edits.replace(other.molsys)
        assert tools.get(n_atoms=True) == other.molsys.get_n_atoms()
        assert view.molsys is not old and view.molsys is not other.molsys
        assert other.export_state() == other_state
    tools.remove(selection=[0], in_place=True, update_view=False)
    view.close()
    assert tools.get_sync_status()["state"] == "closed"
    with pytest.raises(RuntimeError, match="closed"):
        tools.remove(selection=[0], in_place=True)


class _InterruptedWidget(MolSysViewerWidget):
    """A real widget whose connector interrupts one actual scene send.

    This injects a transport failure after native science and some remapping;
    no scientific result or MolSysMT operation is mocked.
    """

    interrupt = False

    def send(self, message, buffers=None):
        if self.interrupt and message.get("op") == "add_sphere":
            self.interrupt = False
            raise OSError("receiving fixture: connector disconnected")
        return super().send(message, buffers=buffers)


def test_reconciliation_failure_retries_scene_once_without_double_remapping_or_science():
    with msv.demo["pentalanine"] as source:
        with msv.MolSysView(transport=_InterruptedWidget()) as view:
            view.load(source.molsys, structure_indices=[0, 8, 3])
            tools = view.addons.molsysmt
            target = view.molsys
            count = target.get_n_atoms()
            region = view.regions.add(selection=[1, 2, 4], tag="kept")
            sphere = view.shapes.add_sphere(atom_indices=[2], tag="anchor")
            view._ready = True
            view.widget.interrupt = True
            with pytest.raises(SystemEditSyncError) as failure:
                tools.remove(selection=[0], in_place=True)
            assert failure.value.science_completed is True
            assert failure.value.scientific_result is None
            assert isinstance(failure.value.__cause__, OSError)
            assert failure.value.operation_id == tools.get_sync_status()["operation_id"]
            assert target.get_n_atoms() == count - 1
            assert tools.get_sync_status()["state"] == "sync_failed"
            assert region.atom_indices == (1, 2, 4)
            tools.sync_view()
            assert target.get_n_atoms() == count - 1
            assert view.regions["kept"] is region and region.atom_indices == (0, 1, 3)
            assert view.shapes["anchor"] is sphere
            assert view.shapes.records()[0]["options"]["atom_indices"] == [1]


def test_uncertain_scientific_write_is_not_recognized_from_unchanged_counts(view):
    manager = view.addons.manager.system_edits

    def prepare(target):
        def run():
            coordinates = msm.get(
                target,
                element="atom",
                selection=[0],
                structure_indices=[0],
                coordinates=True,
            ).copy()
            coordinates += msm.pyunitwizard.quantity(0.1, "nm")
            msm.set(
                target, selection=[0], structure_indices=[0], coordinates=coordinates
            )
            raise RuntimeError("partial scientific write")

        return {"run": run, "changed": True}

    with pytest.raises(RuntimeError, match="partial scientific"):
        manager.execute(prepare, name="receiving.partial")
    assert manager.get_status()["state"] == "uncertain"
    with pytest.raises(SystemEditPendingError):
        manager.synchronize()
    with msv.demo["dialanine"] as source:
        manager.replace(source.molsys)
    assert manager.get_status()["state"] == "synchronized"


def test_conflicting_scene_calls_reject_while_science_runs(view):
    entered, release = Event(), Event()
    errors = []

    def prepare(target):
        def run():
            entered.set()
            if not release.wait(timeout=10):
                raise RuntimeError("receiving fixture did not release")

        return {"run": run, "changed": False}

    def execute():
        try:
            view.addons.manager.system_edits.execute(prepare, name="receiving.lock")
        except Exception as exc:
            errors.append(exc)

    worker = Thread(target=execute)
    worker.start()
    try:
        assert entered.wait(timeout=5)
        with pytest.raises(SystemEditPendingError, match="Another operation"):
            view.active_selection.set([0])
    finally:
        release.set()
        worker.join(timeout=10)
    assert not worker.is_alive() and errors == []


def test_remove_exposes_native_options_plus_keyword_only_integration_control(view):
    native = list(inspect.signature(msm.basic.remove).parameters.values())[1:]
    bound = inspect.signature(view.addons.molsysmt.basic.remove)
    assert list(bound.parameters.values())[:-1] == native
    assert bound.parameters["update_view"].kind is inspect.Parameter.KEYWORD_ONLY
    assert bound.parameters["update_view"].default is True
    assert (
        getattr(view.addons.molsysmt.basic.remove, "digestion_plan", None) is not None
    )
    assert "get_sync_status" in dir(view.addons.molsysmt)
    assert "sync_view" in dir(view.addons.molsysmt)


def test_deactivation_retains_pending_science_and_headless_facade(view):
    tools = view.addons.molsysmt
    tools.remove(selection=[0], in_place=True, update_view=False)
    view.addons.manager.disable("molsysmt")
    assert view.addons.molsysmt is tools
    assert tools.get(n_atoms=True) == view.molsys.get_n_atoms()
    assert tools.get_sync_status()["state"] == "pending"
    tools.sync_view()
    assert tools.get_sync_status()["state"] == "synchronized"


def test_native_projected_analyses_remain_evaluated_without_recalculation(view):
    analysis = msm.Interactions.from_records(
        [
            {
                "structure_index": frame,
                "interaction_type": "hbond",
                "participants": [
                    {"role": role, "atom_indices": [atom]}
                    for role, atom in zip(("donor", "hydrogen", "acceptor"), (2, 3, 4))
                ],
            }
            for frame in range(3)
        ],
        n_atoms=view.molsys.get_n_atoms(),
        n_structures=3,
        evaluated_structure_indices=[0, 1, 2],
        method="receiving.native_subset",
    )
    view.interactions.attach(analysis, name="receiving", assume_aligned=True)
    interaction = view.interactions.add("receiving", structure_indices=[2], tag="hb")
    view.addons.molsysmt.remove(selection=[0], structure_indices=[1], in_place=True)
    projected = view.molsys.interactions["receiving"]
    assert projected is not analysis
    assert projected.n_atoms == view.molsys.get_n_atoms()
    np.testing.assert_array_equal(projected.evaluated_structure_indices, [0, 1])
    assert view.interactions["hb"] is interaction
    assert interaction.filter["structure_indices"] == [1]
    assert view.interactions._frame(interaction, 1)["status"] == "evaluated"
