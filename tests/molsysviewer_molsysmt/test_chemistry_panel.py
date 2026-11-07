"""Inspect native chemistry with honest coverage, bounded pages and no edits."""

import json

import molsysviewer as msv
import numpy as np
import pytest

import molsysmt as msm
from tests.molsysviewer_molsysmt.test_system_panel import state, transport

puw = msm.pyunitwizard


def mount(view, endpoint=None):
    view._handle_frontend_event(
        {
            "event": "panel_navigate",
            "addon": "molsysmt",
            "panel": "chemistry",
            "_panel_endpoint_id": endpoint,
        }
    )
    return view._active_panel_widgets[endpoint][2]


def act(
    view, sent, action="inspect", *, draft=None, parameters=None, endpoint=None, **extra
):
    before = state(sent, endpoint)
    payload = {
        "request_id": before["request_id"] + 1,
        "draft": before["draft"] if draft is None else draft,
        "parameters": before["parameters"] if parameters is None else parameters,
        **extra,
    }
    view._handle_frontend_event(
        {
            "event": "addon_panel_action",
            "addon": "molsysmt",
            "panel": "chemistry",
            "_panel_endpoint_id": endpoint,
            "content": {"type": "action", "id": action, "payload": payload},
        }
    )
    return state(sent, endpoint)


@pytest.fixture
def case():
    with msv.new_view(msm.systems["caffeine"]["caffeine.sdf"]) as view:
        view.regions.add(selection=[0, 2, 14], tag="chosen")
        view.selections.add("chosen", atom_indices=[0, 2, 14])
        view.active_selection.set([0, 2, 14])
        view.interactions.attach(
            msm.Interactions.from_records(
                [],
                n_atoms=24,
                n_structures=1,
                evaluated_structure_indices=[0],
                method="chemistry.panel.readonly",
            ),
            name="preserve",
            assume_aligned=True,
        )
        sent = transport(view)
        panel = mount(view)
        yield view, sent, panel


def page(view, sent, packet, dataset, offset=0):
    result = act(
        view,
        sent,
        "page",
        report_id=packet["report"]["id"],
        dataset=dataset,
        offset=offset,
    )
    assert result["stage"] != "error", result["message"]
    return result


@pytest.mark.parametrize("task", ["chemistry", "hydrogens"])
@pytest.mark.parametrize(
    "draft,indices",
    [
        ({"source": "all"}, list(range(24))),
        ({"source": "indices", "indices": "14,2,0,14"}, [0, 2, 14]),
        ({"source": "current"}, [0, 2, 14]),
        ({"source": "saved", "value": "chosen"}, [0, 2, 14]),
        ({"source": "region", "value": "chosen"}, [0, 2, 14]),
        ({"source": "expression", "expression": "atom_type=='H'"}, list(range(14, 24))),
        ({"source": "indices", "indices": ""}, []),
    ],
)
def test_native_population_and_report_without_any_molecular_or_scene_effect(
    case, task, draft, indices
):
    view, sent, panel = case
    scene, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    coords = puw.get_value(view.molsys.structures.coordinates, to_unit="nm").copy()
    chemistry = msm.convert(
        view.molsys.chemical_states, to_form="molsysmt.ChemicalStatesDict"
    ).to_dict()
    with puw.context(standard_units=["pm", "ps", "radians"]):
        result = act(view, sent, draft=draft, parameters={"task": task})
    assert result["stage"] == "report", result["message"]
    assert result["report"]["n_atoms"] == len(indices)
    np.testing.assert_array_equal(panel._report.data["atom_indices"], indices)
    assert result["report"]["structure_index"] == 0
    assert result["report"]["chemical_state_index"] == 0
    assert (
        "ready" not in result["report"]
        and "protonation" in result["report"]["unassessed_checks"]
    )
    assert (
        view.export_state() == scene
        and view.addons.molsysmt.get_sync_status() == status
    )
    np.testing.assert_array_equal(
        puw.get_value(view.molsys.structures.coordinates, to_unit="nm"), coords
    )
    np.testing.assert_equal(
        msm.convert(
            view.molsys.chemical_states, to_form="molsysmt.ChemicalStatesDict"
        ).to_dict(),
        chemistry,
    )
    np.testing.assert_array_equal(
        view.molsys.interactions["preserve"].evaluated_structure_indices, [0]
    )


def test_caffeine_stored_zero_unknown_finiteness_and_hydrogen_counts_remain_distinct(
    case,
):
    view, sent, _ = case
    result = act(view, sent, draft={"source": "all"})
    charges = page(view, sent, result, "formal_charge")
    assert all(row[1:3] == ["0", "present"] for row in charges["page"]["rows"])
    assert charges["page"]["unit"] == "elementary_charge"
    unknown = page(view, sent, result, "n_implicit_hydrogens")
    assert all(row[1:3] == ["Unknown", "missing"] for row in unknown["page"]["rows"])
    coords = page(view, sent, result, "coordinates")
    assert (
        coords["page"]["unit"] == "nm"
        and coords["page"]["columns"][1] == "Finite position"
    )
    assert all(row[1:3] == ["True", "present"] for row in coords["page"]["rows"])
    inventory = act(view, sent, parameters={"task": "hydrogens"})
    assert (
        inventory["report"]["status"] == "unassessed"
        and inventory["report"]["explicit_hydrogens"] == 10
    )
    assert all(row[2:] == ["Unknown", "Unknown"] for row in inventory["page"]["rows"])
    # Native public annotations explicitly declare additional non-indexed H.
    msm.set(view.molsys, element="atom", n_implicit_hydrogens=0, n_explicit_hydrogens=0)
    available = act(view, sent)
    assert available["report"]["status"] == "available"
    assert all(row[2] == "0" for row in available["page"]["rows"])
    assert sum(int(row[1]) for row in available["page"]["rows"]) == 10
    pairs = page(view, sent, available, "parent_pairs")
    assert len(pairs["page"]["rows"]) == 10


def test_selected_incident_bonds_and_whole_state_checks_keep_native_scope(case):
    view, sent, _ = case
    native = msm.physchem.get_chemical_readiness(view.molsys, selection=[0, 2])
    result = act(view, sent, draft={"source": "indices", "indices": "2,0,2"})
    observed = result["report"]["connectivity"]
    assert observed["incident_bonds"] == len(native["bond_indices"])
    assert (
        observed["crossing_bonds"]
        == len(native["connectivity"]["crossing_bond_indices"])
        > 0
    )
    assert observed["examined_bonds"] == len(
        native["connectivity"]["examined_bond_indices"]
    )
    bonds = page(view, sent, result, "incident_bonds")
    np.testing.assert_array_equal(
        np.asarray([row[:3] for row in bonds["page"]["rows"]], dtype=int),
        np.column_stack([native["bond_indices"], native["bonded_atom_pairs"]]),
    )


@pytest.mark.parametrize("task", ["chemistry", "hydrogens"])
def test_tctim_has_bounded_complete_pages_and_an_ephemeral_report(task):
    with msv.demo["1TCD"] as view:
        sent = transport(view)
        panel = mount(view)
        result = act(view, sent, draft={"source": "all"}, parameters={"task": task})
        assert result["report"]["n_atoms"] == 3983
        assert len(json.dumps(result).encode()) < 65536
        report = panel._report
        collected = []
        for offset in range(0, result["page"]["total"], 50):
            result = page(view, sent, result, result["page"]["dataset"], offset)
            assert len(result["page"]["rows"]) <= 50
            assert len(json.dumps(result).encode()) < 65536
            assert panel._report is report
            collected.extend(int(row[0]) for row in result["page"]["rows"])
        assert collected == list(range(3983))
        cleared = act(view, sent, "clear")
        assert cleared["report"] is None and panel._report is None


@pytest.mark.parametrize(
    "bad",
    [
        {"dataset": "not-a-table", "offset": 0},
        {"dataset": "atom_type", "offset": True},
        {"dataset": "atom_type", "offset": -50},
        {"dataset": "atom_type", "offset": 1},
        {"dataset": "atom_type", "offset": 50},
        {"dataset": "atom_type", "offset": "0"},
    ],
)
def test_invalid_pages_do_not_poison_the_cached_report_or_following_refresh(case, bad):
    view, sent, panel = case
    result = act(view, sent, draft={"source": "all"})
    report = panel._report
    failed = act(view, sent, "page", report_id=result["report"]["id"], **bad)
    assert failed["stage"] == "error" and panel._report is report
    refreshed = act(view, sent, "refresh")
    assert (
        refreshed["page"]["offset"] == 0
        and refreshed["report"]["id"] == result["report"]["id"]
    )


@pytest.mark.parametrize(
    "parameters",
    [
        {"task": "prepare"},
        {"state_mode": "last"},
        {"state_mode": "index", "state_index": "-1"},
        {"state_mode": "index", "state_index": "1.5"},
        {"state_index": 0},
        {"hidden": True},
    ],
)
def test_invalid_report_parameters_are_rejected_without_editing(case, parameters):
    view, sent, _ = case
    scene = view.export_state()
    failed = act(view, sent, draft={"source": "all"}, parameters=parameters)
    assert failed["stage"] == "error" and failed["report"] is None
    assert view.export_state() == scene


def test_report_expires_on_revision_context_input_and_lifetime_changes(case):
    view, sent, panel = case
    first = act(view, sent, draft={"source": "all"})
    token = first["report"]["id"]
    changed = act(
        view, sent, "refresh", parameters={"state_mode": "index", "state_index": "0"}
    )
    assert changed["report"] is None
    second = act(view, sent)
    assert second["report"]["id"] != token
    view.addons.molsysmt.structure.translate(
        translation=puw.quantity([1, 0, 0], "nm"), in_place=True
    )
    assert act(view, sent, "refresh")["report"] is None
    third = act(view, sent)
    assert third["report"]
    view._handle_frontend_event(
        {"event": "panel_navigate", "addon": "molsysmt", "panel": "system"}
    )
    assert panel._report is None and not panel._alive
    replacement = mount(view)
    assert (
        state(sent)["report"] is None
        and replacement._parameters["state_mode"] == "index"
    )


@pytest.mark.parametrize("task", ["chemistry", "hydrogens"])
def test_pending_primary_reports_do_not_project_and_scene_selections_are_refused(
    case, task
):
    view, sent, _ = case
    view.addons.molsysmt.structure.translate(
        translation=puw.quantity([1, 0, 0], "nm"), in_place=True, update_view=False
    )
    before = view.addons.molsysmt.get_sync_status()
    result = act(view, sent, draft={"source": "all"}, parameters={"task": task})
    assert result["report"] and result["context"]["state"] == "pending"
    assert view.addons.molsysmt.get_sync_status() == before
    failed = act(view, sent, draft={"source": "saved", "value": "chosen"})
    assert (
        failed["stage"] == "error"
        and failed["report"] is None
        and "Update the scene" in failed["message"]
    )
    assert view.addons.molsysmt.get_sync_status() == before


def test_long_native_labels_are_bounded_without_rewriting_source_values(case):
    view, sent, _ = case
    value = "<script>" + "a" * 10000
    msm.set(
        view.molsys, element="atom", atom_id=[value] + [str(i) for i in range(1, 24)]
    )
    result = act(view, sent, draft={"source": "all"})
    detailed = page(view, sent, result, "atom_id")
    assert detailed["page"]["rows"][0][1] == value[:200] + "…"
    assert msm.get(view.molsys, element="atom", atom_id=True)[0] == value
    assert len(json.dumps(detailed).encode()) < 65536


@pytest.mark.parametrize("source", ["current", "saved", "region"])
def test_report_revalidates_scene_membership_even_without_a_molecular_revision(
    case, source
):
    view, sent, _ = case
    draft = {"source": source, "value": "chosen"}
    assert act(view, sent, draft=draft)["report"]
    revision = view.addons.molsysmt.get_sync_status()["target_revision"]
    if source == "current":
        view.active_selection.set([1])
    elif source == "saved":
        view.selections.delete("chosen")
    else:
        view.regions.delete("chosen")
    assert view.addons.molsysmt.get_sync_status()["target_revision"] == revision
    assert act(view, sent, "refresh")["report"] is None


@pytest.mark.parametrize(
    "mode,index,state_status",
    [
        ("reference", 0, "resolved"),
        ("structure", 1, "resolved"),
        ("structure", 2, "unassociated"),
        ("index", 2, "resolved"),
    ],
)
def test_explicit_structure_context_and_state_are_preserved(mode, index, state_status):
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0, 8, 3]) as view:
            view.molsys.chemical_states.append_state()
            view.molsys.chemical_states._states[1].set_atom_attribute(
                "formal_charge", [0] * 62
            )
            msm.set(
                view.molsys,
                element="system",
                structure_chemical_state_index=[0, 1, None],
            )
            sent = transport(view)
            mount(view)
            result = act(
                view,
                sent,
                draft={"source": "all", "context": "index", "structure_index": index},
                parameters={"state_mode": mode, "state_index": "1"},
            )
            assert result["report"], result["message"]
            assert result["report"]["structure_index"] == index
            assert result["report"]["chemical_state_status"] == state_status
            assert result["report"]["chemical_state_index"] == (
                1
                if mode == "index" or index == 1
                else 0
                if mode == "reference"
                else None
            )
            view.player.go_to_structure(1)
            assert act(view, sent, "refresh")["report"] is None


def test_ambiguous_reference_is_reported_without_choosing_a_state(case):
    view, sent, _ = case
    view.molsys.chemical_states.append_state()
    view.molsys.chemical_states._set_reference_index(None)
    result = act(view, sent, draft={"source": "all"})
    assert result["report"], result["message"]
    assert result["report"]["chemical_state_status"] == "ambiguous"
    assert result["report"]["chemical_state_index"] is None
