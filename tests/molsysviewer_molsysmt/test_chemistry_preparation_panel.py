"""Native preparation, explicit result ownership and stale replacement guards."""

import json

import molsysviewer as msv
import numpy as np
import pytest

import molsysmt as msm
from tests.build.add_missing_heavy_atoms.test_domain_preservation import (
    incomplete_serine,
)
from tests.build.add_missing_hydrogens.test_fixed_state import prepared
from tests.molsysviewer_molsysmt.test_build_assignment_tools import snapshot, unchanged
from tests.molsysviewer_molsysmt.test_chemistry_panel import act, mount
from tests.molsysviewer_molsysmt.test_system_panel import transport

puw = msm.pyunitwizard
FIXED = {"task": "add_hydrogens", "hydrogen_mode": "fixed_chemical_state"}


@pytest.fixture
def case():
    with msv.new_view(prepared("CO", [[0, 0, 0], [1.4, 0, 0]])) as view:
        view.regions.add(selection=[0], tag="source-region")
        view.shapes.add_sphere(atom_indices=[0], tag="source-marker")
        sent = transport(view)
        panel = mount(view)
        yield view, sent, panel
        for item in view.addons.manager.presentations.records():
            view.addons.manager.presentations.close(item["id"])


def result_view(view, packet):
    return view.addons.manager.presentations.get(packet["result"]["id"])


@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_fixed_generation_preserves_source_and_native_report_with_bounded_metadata(
    case, unit
):
    view, sent, _ = case
    before = snapshot(view)
    with puw.context(standard_units=[unit, "ps"]):
        packet = act(view, sent, "prepare", parameters=FIXED)
    assert packet["stage"] == "prepared", packet["message"]
    child = result_view(view, packet)
    assert child.molsys is not view.molsys and child.molsys.get_n_atoms() == 6
    assert packet["result"]["source_atoms"] == 2
    assert packet["result"]["parameters"]["engine"] == "RDKit"
    assert packet["result"]["parameters"]["pH"] is None
    assert packet["result"]["parameters"]["added_hydrogens"] == 4
    history = child.molsys.chemical_states.get_preparation_history()
    assert history[-1]["report"]["coordinate_unit"] == "nm"
    assert history[-1]["report"]["n_added_hydrogens"] == 4
    np.testing.assert_array_equal(
        puw.get_value(child.molsys.structures.coordinates, to_unit="nm")[:, :2],
        puw.get_value(view.molsys.structures.coordinates, to_unit="nm"),
    )
    assert len(json.dumps(packet).encode()) < 65536
    assert "coordinates" not in packet["result"] and packet["can_replace"]
    unchanged(view, before)


def test_heavy_completion_uses_selected_groups_and_every_structure_without_auto_adoption():
    source = incomplete_serine()
    with msv.new_view(source) as view:
        sent = transport(view)
        mount(view)
        before = snapshot(view)
        packet = act(
            view,
            sent,
            "prepare",
            draft={"source": "all"},
            parameters={"task": "heavy", "attribute_policy": "intersection"},
        )
        assert packet["stage"] == "prepared", packet["message"]
        child = result_view(view, packet)
        assert child.molsys.get_n_atoms() == view.molsys.get_n_atoms() + 1
        assert (
            child.molsys.structures.n_structures == view.molsys.structures.n_structures
        )
        assert packet["result"]["operation"] == "molsysmt.build.add_missing_heavy_atoms"
        assert not child.molsys.interactions[
            "declared-analysis"
        ].evaluated_structure_indices.size
        unchanged(view, before)


def test_strict_heavy_attribute_rejection_leaves_source_and_no_partial_result():
    with msv.new_view(incomplete_serine()) as view:
        sent = transport(view)
        mount(view)
        before = snapshot(view)
        packet = act(
            view,
            sent,
            "prepare",
            draft={"source": "all"},
            parameters={"task": "heavy", "attribute_policy": "strict"},
        )
        assert packet["stage"] == "error" and not packet["result"], packet["message"]
        assert not view.addons.manager.presentations.records()
        unchanged(view, before)


@pytest.mark.parametrize("group_index,added", [(0, 1), (1, 0)])
def test_heavy_task_resolves_atom_editor_to_groups_explicitly(group_index, added):
    with msv.new_view(incomplete_serine()) as view:
        sent = transport(view)
        mount(view)
        atom = int(msm.select(view.molsys, selection=f"group_index=={group_index}")[0])
        packet = act(
            view,
            sent,
            "prepare",
            draft={"source": "indices", "indices": str(atom)},
            parameters={"task": "heavy", "attribute_policy": "intersection"},
        )
        assert packet["stage"] == "prepared", packet["message"]
        assert (
            result_view(view, packet).molsys.get_n_atoms()
            == view.molsys.get_n_atoms() + added
        )
        assert packet["result"]["parameters"]["selection_atoms"] == 1
        assert packet["result"]["parameters"]["selected_groups"] == 1


def test_heavy_completion_retains_all_structures_and_their_observed_coordinates():
    source = incomplete_serine()
    source.interactions = {}
    first = puw.get_value(source.structures.coordinates, to_unit="nm")
    coordinates = np.concatenate([first, first + [0.5, 0.1, -0.2]], axis=0)
    msm.set(source, time=puw.quantity([0], "ps"))
    incoming = msm.copy(source)
    msm.set(
        incoming,
        coordinates=puw.quantity(coordinates[1:], "nm"),
        time=puw.quantity([2], "ps"),
    )
    msm.append_structures(source, incoming)
    with msv.new_view(source) as view:
        sent = transport(view)
        mount(view)
        packet = act(
            view,
            sent,
            "prepare",
            draft={"source": "all"},
            parameters={"task": "heavy", "attribute_policy": "intersection"},
        )
        assert packet["stage"] == "prepared", packet["message"]
        child = result_view(view, packet)
        assert child.molsys.structures.n_structures == 2
        assert packet["result"]["structure_indices"] == [0, 1]
        ids = list(child.molsys.topology.atoms.atom_id)
        mapping = [ids.index(i) for i in source.topology.atoms.atom_id]
        np.testing.assert_array_equal(
            puw.get_value(child.molsys.structures.coordinates, to_unit="nm")[
                :, mapping
            ],
            coordinates,
        )
        np.testing.assert_array_equal(
            puw.get_value(child.molsys.structures.time, to_unit="ps"), [0, 2]
        )


@pytest.mark.parametrize("task", ["heavy", "add_hydrogens"])
def test_generation_is_not_admitted_as_a_pending_state_reader(case, task):
    view, sent, panel = case
    assert "prepare" not in panel.read_only_actions
    assert not any(
        action.startswith("replacement.") for action in panel.read_only_actions
    )
    view.addons.molsysmt.basic.set(
        box=puw.quantity(np.eye(3)[None], "nm"), update_view=False
    )
    count = len(sent)
    act(view, sent, "prepare", parameters={"task": task})
    assert not any(x.get("op") == "addon_panel_message" for x in sent[count:])
    assert not view.addons.manager.presentations.records()
    assert view.addons.molsysmt.get_sync_status()["state"] == "pending"


def test_review_back_and_replacement_keep_result_independent_and_reset_scene(case):
    view, sent, _ = case
    before = snapshot(view)
    packet = act(view, sent, "prepare", parameters=FIXED)
    child = result_view(view, packet)
    review = act(view, sent, "replacement.review")
    assert review["replacement"]["token"]
    cancelled = act(view, sent, "replacement.back")
    assert not cancelled["replacement"]
    unchanged(view, before)
    stale = act(view, sent, "replacement.apply", token=review["replacement"]["token"])
    assert stale["stage"] == "error" and view.molsys.get_n_atoms() == 2
    review = act(view, sent, "replacement.review")
    applied = act(view, sent, "replacement.apply", token=review["replacement"]["token"])
    assert applied["stage"] == "prepared", applied["message"]
    assert view.molsys.get_n_atoms() == 6 and view.molsys is not child.molsys
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"
    assert not np.shares_memory(
        puw.get_value(view.molsys.structures.coordinates, to_unit="nm"),
        puw.get_value(child.molsys.structures.coordinates, to_unit="nm"),
    )
    assert (
        "source-region" not in view.regions and view.shapes.get("source-marker") is None
    )
    assert not applied["can_replace"]
    child_coords = puw.get_value(
        child.molsys.structures.coordinates, to_unit="nm"
    ).copy()
    view.addons.molsysmt.structure.translate(
        translation="[0.1, 0, 0] nm", in_place=True
    )
    np.testing.assert_array_equal(
        puw.get_value(child.molsys.structures.coordinates, to_unit="nm"), child_coords
    )


@pytest.mark.parametrize("changed", ["source", "candidate", "source_reload"])
def test_managed_changes_after_review_never_overwrite_current_system(case, changed):
    view, sent, _ = case
    packet = act(view, sent, "prepare", parameters=FIXED)
    child = result_view(view, packet)
    review = act(view, sent, "replacement.review")
    if changed == "source_reload":
        view.addons.manager.system_edits.replace(view.molsys)
    else:
        owner = view if changed == "source" else child
        owner.addons.molsysmt.structure.translate(
            translation="[0.1, 0, 0] nm", in_place=True
        )
    before = snapshot(view)
    rejected = act(
        view, sent, "replacement.apply", token=review["replacement"]["token"]
    )
    assert rejected["stage"] == "error", rejected["message"]
    assert not rejected["replacement"] and rejected["result"]
    unchanged(view, before)


@pytest.mark.parametrize("when", ["before", "after"])
def test_source_change_disables_replacement_but_preserves_independent_result(
    case, when
):
    view, sent, _ = case
    packet = act(view, sent, "prepare", parameters=FIXED)
    if when == "after":
        act(view, sent, "replacement.review")
    view.addons.molsysmt.structure.translate(
        translation="[0.1, 0, 0] nm", in_place=True
    )
    refreshed = act(view, sent, "refresh")
    assert refreshed["result"]["id"] == packet["result"]["id"]
    assert not refreshed["can_replace"] and not refreshed["replacement"]
    rejected = act(view, sent, "replacement.review")
    assert rejected["stage"] == "error"


@pytest.mark.parametrize(
    "change",
    [
        {"pH": "nan"},
        {"pH": "a"},
        {"task": "unknown"},
        {"title": "a" * 201},
        {"engine": "other"},
    ],
)
def test_invalid_preparation_requests_do_not_create_or_modify_data(case, change):
    view, sent, _ = case
    before = snapshot(view)
    packet = act(view, sent, "prepare", parameters={"task": "add_hydrogens", **change})
    assert packet["stage"] == "error" and not packet["result"]
    assert not view.addons.manager.presentations.records()
    unchanged(view, before)


@pytest.mark.parametrize("mode", ["pH", "fixed_chemical_state"])
def test_hydrogens_require_explicit_single_structure_extraction(mode):
    with msv.demo["pentalanine"] as seed:
        with msv.new_view(seed.molsys, structure_indices=[0, 8, 3]) as view:
            sent = transport(view)
            mount(view)
            before = snapshot(view)
            packet = act(
                view,
                sent,
                "prepare",
                parameters={"task": "add_hydrogens", "hydrogen_mode": mode},
            )
            assert (
                packet["stage"] == "error"
                and "Extract one structure" in packet["message"]
            )
            assert not view.addons.manager.presentations.records()
            unchanged(view, before)


@pytest.mark.parametrize(
    "mode", ["leave_unpresented", "leave_presented", "close", "unmount"]
)
def test_result_lifetime_and_repeated_preparation_are_explicit(case, mode):
    view, sent, panel = case
    packet = act(view, sent, "prepare", parameters=FIXED)
    child = result_view(view, packet)
    repeated = act(view, sent, "prepare")
    assert repeated["stage"] == "error"
    assert len(view.addons.manager.presentations.records()) == 1
    if mode == "leave_presented":
        # The real host publication path roots the result, without manufacturing
        # a scientific substitute or a fake destination record.
        view.addons.manager.presentations._show(packet["result"]["id"], "notebook")
    if mode == "unmount":
        reviewed = act(view, sent, "replacement.review")
        assert reviewed["replacement"]
        panel.on_unmount(view)
        assert child.closed and panel._adoption is None
    else:
        act(view, sent, "result.discard" if mode == "close" else "result.new")
        assert child.closed == (mode != "leave_presented")


def test_clear_report_does_not_delete_prepared_molecular_data(case):
    view, sent, _ = case
    packet = act(view, sent, "prepare", parameters=FIXED)
    cleared = act(view, sent, "clear")
    assert cleared["result"]["id"] == packet["result"]["id"]
    assert not result_view(view, cleared).closed
