"""Inspect native coverage and protonation decisions without preparing a system."""

import json

import molsysviewer as msv
import numpy as np
import pytest

import molsysmt as msm
from tests.molsysviewer_molsysmt.test_build_assignment_tools import snapshot, unchanged
from tests.molsysviewer_molsysmt.test_chemistry_panel import act, mount, page
from tests.molsysviewer_molsysmt.test_system_panel import transport

puw = msm.pyunitwizard
TASKS = ["coverage", "terminals", "protonation"]


@pytest.fixture
def case():
    with msv.new_view(msm.systems["chicken villin HP35"]["1vii.pdb"]) as view:
        view.active_selection.set([0])
        sent = transport(view)
        panel = mount(view)
        yield view, sent, panel


def inspect(case, task, *, draft=None, **parameters):
    view, sent, _ = case
    return act(view, sent, draft=draft, parameters={"task": task, **parameters})


@pytest.mark.parametrize("task", TASKS)
@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
def test_native_reports_keep_scope_units_source_and_scene(case, task, unit):
    view, sent, panel = case
    before = snapshot(view)
    with puw.context(standard_units=[unit, "ps"]):
        policy = puw.configure.report()
        result = inspect(case, task, draft={"source": "all"}, pH="12")
        assert result["stage"] == "report", result.get("message")
        if task == "coverage":
            native = msm.build.get_residue_chemical_coverage(
                view.molsys, structure_indices=[0]
            )
            assert result["report"]["counts"] == native["summary"]
            assert result["report"]["group_count"] == len(native["groups"])
        elif task == "terminals":
            native = msm.build.get_missing_terminal_cappings(view.molsys)
            assert result["page"]["rows"] == [
                [str(i), ", ".join(names)] for i, names in native.items()
            ]
        else:
            native = msm.build.assess_protonation(view.molsys, pH=12).to_dict()
            assert result["report"]["removed_atoms"] == 6
            assert result["report"]["status"] == native["status"]
            removed = page(view, sent, result, "protonation_removals")
            assert removed["page"]["rows"] == [
                [str(value) for value in row] for row in native["removed_atoms"]
            ]
            assert panel._report.data["assessment"]["execution"]["status"] == "prepared"
            assert not hasattr(panel._report.data["assessment"], "apply")
            assert len(result["report"]["attribution"]) > 0
        assert puw.configure.report() == policy
    assert result["report"]["family"] == "assessment"
    assert len(result["page"]["rows"]) <= 50
    assert len(json.dumps(result)) < 40000
    assert not view.addons.manager.presentations.records()
    unchanged(view, before)


def test_partial_atom_selection_becomes_one_whole_source_group(case):
    view, _, panel = case
    result = inspect(case, "coverage", draft={"source": "indices", "indices": "2,0,2"})
    assert result["stage"] == "report"
    assert result["report"]["group_count"] == 1
    assert result["page"]["rows"][0][0] == "0"
    np.testing.assert_array_equal(panel._report.data["atom_indices"], [0, 2])
    np.testing.assert_array_equal(
        panel._report.data["assessment"]["group_indices"], [0]
    )
    assert len(panel._report.data["assessment"]["groups"][0]["atom_indices"]) > 2


def test_unknown_group_is_not_certified_as_complete():
    builder = msm.MolSysBuilder()
    atom = builder.add_atom(atom_name="C1", atom_type="C")
    builder.add_group([atom], group_name="LIG")
    builder.set_coordinates(puw.quantity(np.zeros((1, 1, 3)), "nm"))
    with msv.new_view(builder.build()) as view:
        sent = transport(view)
        panel = mount(view)
        result = inspect((view, sent, panel), "coverage", draft={"source": "all"})
        assert result["report"]["counts"] == {
            "assessed": 0,
            "incomplete": 0,
            "unassessed": 1,
        }
        assert result["page"]["rows"][0][2:6] == [
            "unassessed",
            "unassessed",
            "Unknown",
            "Unknown",
        ]
        assert "no_exact_residue_template" in result["page"]["rows"][0][-1]
        result = inspect((view, sent, panel), "protonation")
        assert result["report"]["removed_atoms"] == 0
        assert result["report"]["status"] == "unassessed"
        assert not result["report"]["coverage_complete"]
        assert result["report"]["unassessed_groups"] == 1
        result = inspect((view, sent, panel), "terminals")
        assert result["page"]["total"] == 0 and result["page"]["rows"] == []
        assert "non_amino_acid_groups" in result["report"]["unassessed_checks"]


@pytest.mark.parametrize("task", ["terminals", "protonation"])
def test_whole_system_checks_ignore_hidden_selection_state_and_structure_drafts(
    case, task
):
    view, _, panel = case
    result = inspect(
        case,
        task,
        draft={
            "source": "indices",
            "indices": "not indices",
            "context": "index",
            "structure_index": 900,
        },
        state_mode="index",
        state_index="9999",
    )
    assert result["stage"] == "report", result.get("message")
    assert result["report"]["structure_index"] is None
    assert panel._report.data["atom_indices"] is None
    assert result["report"]["group_count"] > 0 or task == "terminals"


@pytest.mark.parametrize("ph", ["nan", "inf", "-inf", "not pH"])
def test_bad_ph_refuses_without_result_or_scientific_write(case, ph):
    view, _, panel = case
    before = snapshot(view)
    result = inspect(case, "protonation", pH=ph)
    assert result["stage"] == "error"
    assert "finite" in result["message"]
    assert panel._report is None
    unchanged(view, before)


def test_group_pages_are_bounded_and_do_not_recompute_science(case, monkeypatch):
    view, sent, panel = case
    # TcTIM supplies more than fifty groups without a trajectory stress run.
    view.load(msm.systems["TcTIM"]["1tcd.h5msm"])
    result = inspect(case, "coverage", draft={"source": "all"})
    assert result["stage"] == "report", result.get("message")
    assert len(result["page"]["rows"]) == 50
    monkeypatch.setattr(
        msm.build,
        "get_residue_chemical_coverage",
        lambda *a, **k: pytest.fail("Paging repeated science"),
    )
    next_page = page(view, sent, result, "coverage_groups", offset=50)
    assert next_page["page"]["offset"] == 50
    assert len(next_page["page"]["rows"]) == 50
    assert next_page["report"]["id"] == result["report"]["id"]
    assert next_page["page"]["rows"][0][0] == "50"
    assert panel._report is not None


@pytest.mark.parametrize("task", TASKS)
def test_pending_readers_and_managed_source_expiry(case, task):
    view, sent, panel = case
    view.addons.molsysmt.structure.translate(
        translation="[0.1,0,0] nm", in_place=True, update_view=False
    )
    assert view.addons.molsysmt.get_sync_status()["state"] == "pending"
    before = snapshot(view)
    result = inspect(case, task, draft={"source": "all"})
    assert result["stage"] == "report", result.get("message")
    unchanged(view, before)
    token = result["report"]["id"]
    view.addons.molsysmt.structure.translate(
        translation="[0.1,0,0] nm", in_place=True, update_view=False
    )
    stale = act(
        view, sent, "page", report_id=token, dataset=result["page"]["dataset"], offset=0
    )
    assert stale["stage"] == "error"
    assert panel._report is None


def test_pending_scene_selection_does_not_become_a_primary_selection(case):
    view, _, panel = case
    view.addons.molsysmt.structure.translate(
        translation="[0.1,0,0] nm", in_place=True, update_view=False
    )
    result = inspect(case, "coverage", draft={"source": "current"})
    assert result["stage"] == "error"
    assert "Update the scene" in result["message"]
    assert panel._report is None


@pytest.mark.parametrize("task", TASKS)
def test_clear_foreign_pages_and_parameter_changes_retire_reports(case, task):
    view, sent, panel = case
    result = inspect(case, task, draft={"source": "all"})
    assert result["stage"] == "report"
    rejected = act(
        view,
        sent,
        "page",
        report_id="foreign",
        dataset=result["page"]["dataset"],
        offset=0,
    )
    assert rejected["stage"] == "error"
    refreshed = act(view, sent, "refresh", parameters={"task": task, "pH": "8.2"})
    assert refreshed["report"] is None and panel._report is None
    result = inspect(case, task, draft={"source": "all"})
    cleared = act(view, sent, "clear")
    assert cleared["report"] is None and panel._report is None


def test_ungrouped_source_has_an_explicit_prerequisite_failure():
    with msv.new_view(msm.systems["caffeine"]["caffeine.sdf"]) as view:
        sent = transport(view)
        panel = mount(view)
        result = inspect((view, sent, panel), "coverage", draft={"source": "all"})
        assert result["stage"] == "error"
        assert "known source group membership" in result["message"]
        assert panel._report is None


def test_empty_group_scope_is_evaluated_empty_not_whole_system(case):
    _, _, panel = case
    result = inspect(
        case, "coverage", draft={"source": "expression", "expression": "atom_index < 0"}
    )
    assert result["stage"] == "report", result.get("message")
    assert result["report"]["group_count"] == 0
    assert result["page"]["total"] == 0 and result["page"]["rows"] == []
    assert len(panel._report.data["assessment"]["group_indices"]) == 0


def test_explicit_state_is_passed_to_template_comparison(case):
    view, _, panel = case
    result = inspect(
        case,
        "coverage",
        draft={"source": "indices", "indices": "0"},
        state_mode="index",
        state_index="0",
    )
    assert result["stage"] == "report"
    assert result["report"]["chemical_state_index"] == 0
    native = msm.build.get_residue_chemical_coverage(
        view.molsys, selection=[0], structure_indices=[0], chemical_state=0
    )
    assert result["report"]["counts"] == native["summary"]
    result = inspect(
        case,
        "coverage",
        draft={"source": "all"},
        state_mode="index",
        state_index="9999",
    )
    assert result["stage"] == "error"
    assert panel._report is None
