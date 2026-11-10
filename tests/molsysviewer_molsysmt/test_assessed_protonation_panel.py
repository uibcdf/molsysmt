"""Consume one inspected native decision through explicit graphical actions."""

import json

import molsysviewer as msv
import numpy as np
import pytest

import molsysmt as msm
from tests.molsysviewer_molsysmt.test_build_assignment_tools import (
    same,
    snapshot,
    unchanged,
)
from tests.molsysviewer_molsysmt.test_chemistry_panel import act, mount
from tests.molsysviewer_molsysmt.test_chemistry_preparation_panel import result_view
from tests.molsysviewer_molsysmt.test_protonation_tools import (
    retained_indices,
)
from tests.molsysviewer_molsysmt.test_protonation_tools import (
    source as source,
)
from tests.molsysviewer_molsysmt.test_system_panel import transport

puw = msm.pyunitwizard


@pytest.fixture
def case(source):
    with msv.new_view(source.copy()) as view:
        view.regions.add(selection=[0, 2], tag="retained")
        view.active_selection.set([0, 2])
        view.shapes.add_sphere(atom_indices=[1], tag="marker")
        keep = retained_indices(view.molsys, 12.0)
        removed = next(i for i in range(596) if i not in keep)
        view.interactions.attach(
            msm.Interactions.from_records(
                [
                    {
                        "structure_index": frame,
                        "interaction_type": "contact",
                        "participants": [
                            {"role": "first", "atom_indices": [atom]},
                            {"role": "second", "atom_indices": [keep[-1]]},
                        ],
                    }
                    for frame in range(3)
                    for atom in (keep[0], removed)
                ],
                n_atoms=596,
                n_structures=3,
                evaluated_structure_indices=[0, 1, 2],
                method="synthetic.assessed-panel",
            ),
            name="source-observations",
            assume_aligned=True,
        )
        sent = transport(view)
        panel = mount(view)
        yield view, sent, panel
        for record in view.addons.manager.presentations.records():
            view.addons.manager.presentations.close(record["id"])


def inspect(case, pH="12"):
    view, sent, _ = case
    packet = act(view, sent, parameters={"task": "protonation", "pH": pH})
    assert packet["stage"] == "report", packet["message"]
    return packet


def review(case, packet):
    view, sent, _ = case
    result = act(view, sent, "protonation.review", report_id=packet["report"]["id"])
    assert result["stage"] == "assessment_review", result["message"]
    return result


def managed_unchanged(view, before):
    # The host records the attempted operation ID even after atomic rejection
    # or a true no-op. Molecular data, axes, scene, history and revisions stay.
    status = view.addons.molsysmt.get_sync_status()
    assert status["operation_id"].startswith(
        "molsysmt.build.ProtonationAssessment.apply:"
    )
    status_before = dict(before[3], operation_id=status["operation_id"])
    unchanged(view, (*before[:3], status_before, *before[4:]))


@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize("destination", ["protonation.apply", "protonation.prepare"])
def test_same_assessed_decision_all_structures_maps_units_and_no_reassessment(
    case, unit, destination, monkeypatch
):
    view, sent, panel = case
    before = snapshot(view)
    keep = retained_indices(view.molsys, 12.0)
    expected = msm.build.reconcile_protonation(view.molsys, pH=12.0)
    with puw.context(standard_units=[unit, "ps"]):
        policy = puw.configure.report()
        packet = inspect(case)
        decision = panel._protonation_decision
        assert decision.to_dict()["execution"]["status"] == "prepared"
        assert packet["can_apply_protonation"] and packet["can_prepare_protonation"]
        monkeypatch.setattr(
            msm.build,
            "assess_protonation",
            lambda *a, **k: pytest.fail("Repeated assessment"),
        )
        if destination.endswith("apply"):
            packet = review(case, packet)
        result = act(
            view,
            sent,
            destination,
            report_id=packet["report"]["id"],
            token=packet["protonation_review"],
        )
        assert result["stage"] == (
            "applied" if destination.endswith("apply") else "prepared"
        ), result["message"]
        assert puw.configure.report() == policy
    actual = (
        view.molsys
        if destination.endswith("apply")
        else result_view(view, result).molsys
    )
    same(actual, expected)
    assert actual.get_n_atoms() == 590 and actual.structures.n_structures == 3
    assert actual.structures.structure_id.tolist() == ["C", "A", "C"]
    np.testing.assert_array_equal(
        puw.get_value(actual.structures.coordinates, to_unit="nm"),
        puw.get_value(before[1].structures.coordinates, to_unit="nm")[:, keep],
    )
    assert panel._protonation_decision is panel._report is None
    assert decision.to_dict()["execution"]["status"] != "prepared"
    assert not result["can_apply_protonation"] and not result["can_prepare_protonation"]
    assert len(json.dumps(result)) < 40000
    if destination.endswith("prepare"):
        unchanged(view, before)
        assert actual is not view.molsys and result["can_replace"]
        assert result["result"]["parameters"]["assessed_decision"]
    else:
        assert view.addons.molsysmt.get_sync_status()["target_revision"] == 1
        assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"
        assert view.whole.get(n_atoms=True) == 590


def test_back_foreign_review_and_replayed_decision_never_remove_atoms(case):
    view, sent, panel = case
    before = snapshot(view)
    packet = inspect(case)
    token = packet["report"]["id"]
    rejected = act(view, sent, "protonation.apply", report_id=token, token="foreign")
    assert rejected["stage"] == "error"
    unchanged(view, before)
    packet = review(case, rejected)
    old = packet["protonation_review"]
    cancelled = act(view, sent, "protonation.back", report_id=token)
    assert not cancelled["protonation_review"]
    unchanged(view, before)
    rejected = act(view, sent, "protonation.apply", report_id=token, token=old)
    assert rejected["stage"] == "error"
    unchanged(view, before)
    packet = review(case, rejected)
    applied = act(
        view,
        sent,
        "protonation.apply",
        report_id=token,
        token=packet["protonation_review"],
    )
    assert applied["stage"] == "applied", applied["message"]
    current = snapshot(view)
    rejected = act(
        view,
        sent,
        "protonation.apply",
        report_id=token,
        token=packet["protonation_review"],
    )
    assert rejected["stage"] == "error" and panel._protonation_decision is None
    unchanged(view, current)


@pytest.mark.parametrize("destination", ["protonation.apply", "protonation.prepare"])
def test_raw_inventory_change_refuses_stale_native_decision_atomically(
    case, destination
):
    view, sent, panel = case
    packet = review(case, inspect(case))
    view.molsys.topology.atoms.loc[0, "atom_name"] = "changed"
    before = snapshot(view)
    rejected = act(
        view,
        sent,
        destination,
        report_id=packet["report"]["id"],
        token=packet["protonation_review"],
    )
    assert rejected["stage"] == "error", rejected["message"]
    assert panel._protonation_decision is panel._report is None
    (managed_unchanged if destination.endswith("apply") else unchanged)(view, before)


def test_noop_consumes_once_without_revisions_history_or_domain_publication(case):
    view, sent, panel = case
    before = snapshot(view)
    domains = (
        view.molsys.topology,
        view.molsys.chemical_states,
        view.molsys.structures,
        view.molsys.molecular_mechanics,
    )
    packet = review(case, inspect(case, "7.4"))
    assert packet["report"]["removed_atoms"] == 0
    decision = panel._protonation_decision
    applied = act(
        view,
        sent,
        "protonation.apply",
        report_id=packet["report"]["id"],
        token=packet["protonation_review"],
    )
    assert applied["stage"] == "applied", applied["message"]
    assert decision.to_dict()["execution"]["status"] != "prepared"
    assert domains == (
        view.molsys.topology,
        view.molsys.chemical_states,
        view.molsys.structures,
        view.molsys.molecular_mechanics,
    )
    managed_unchanged(view, before)


@pytest.mark.parametrize("change", ["clear", "inputs", "revision", "replace"])
def test_lifetime_retires_the_executable_decision(case, change):
    view, sent, panel = case
    packet = review(case, inspect(case))
    if change == "clear":
        act(view, sent, "clear")
    elif change == "inputs":
        act(view, sent, "refresh", parameters={"task": "protonation", "pH": "8"})
    elif change == "replace":
        view.load(view.molsys.copy(), mode="replace")
    else:
        view.addons.molsysmt.structure.translate(
            translation="[0.1,0,0] nm", in_place=True
        )
    before = snapshot(view)
    rejected = act(view, sent, "protonation.prepare", report_id=packet["report"]["id"])
    assert rejected["stage"] == "error"
    assert panel._protonation_decision is None
    unchanged(view, before)


def test_existing_result_refuses_second_consumption_and_keeps_inspected_decision(case):
    view, sent, panel = case
    packet = inspect(case)
    first = act(view, sent, "protonation.prepare", report_id=packet["report"]["id"])
    assert first["stage"] == "prepared", first["message"]
    packet = inspect(case)
    decision = panel._protonation_decision
    assert not packet["can_prepare_protonation"]
    rejected = act(view, sent, "protonation.prepare", report_id=packet["report"]["id"])
    assert rejected["stage"] == "error"
    assert panel._protonation_decision is decision
    assert decision.to_dict()["execution"]["status"] == "prepared"
    assert rejected["result"]["id"] == first["result"]["id"]


def test_projection_retry_cannot_repeat_the_consumed_assessed_science(
    source, monkeypatch
):
    from tests.molsysviewer_molsysmt.test_minimization_tools import (
        InterruptedMinimizationWidget,
    )

    with msv.MolSysView(transport=InterruptedMinimizationWidget()) as view:
        view.load(source.copy())
        view.shapes.add_sphere(atom_indices=[1], tag="projection-control")
        sent = transport(view)

        def receive(content, buffers=None):
            InterruptedMinimizationWidget.send(view.widget, content, buffers=buffers)
            sent.append(content)

        view.widget.send = receive
        panel = mount(view)
        view._ready = True
        packet = review((view, sent, panel), inspect((view, sent, panel)))
        decision = panel._protonation_decision
        monkeypatch.setattr(
            msm.build,
            "assess_protonation",
            lambda *a, **k: pytest.fail("Repeated assessment"),
        )
        view.widget.interrupted = True
        result = act(
            view,
            sent,
            "protonation.apply",
            report_id=packet["report"]["id"],
            token=packet["protonation_review"],
        )
        assert result["stage"] == "sync_required", result["message"]
        assert panel._protonation_decision is panel._report is None
        assert view.molsys.get_n_atoms() == 590
        assert decision.to_dict()["execution"]["status"] != "prepared"
        coordinates = puw.get_value(
            view.molsys.structures.coordinates, to_unit="nm"
        ).copy()
        view.addons.molsysmt.sync_view()
        assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"
        np.testing.assert_array_equal(
            puw.get_value(view.molsys.structures.coordinates, to_unit="nm"), coordinates
        )


def test_unmount_releases_the_executable_decision(case):
    view, _, panel = case
    inspect(case)
    assert panel._protonation_decision is not None
    panel.on_unmount(view)
    assert (
        panel._protonation_decision
        is panel._protonation_review
        is panel._report
        is None
    )


def test_presentation_publication_failure_keeps_source_and_no_partial_result(
    case, monkeypatch
):
    view, sent, panel = case
    packet = inspect(case)
    before = snapshot(view)

    def unavailable(*a, **k):
        raise RuntimeError("deliberate presentation publication refusal")

    monkeypatch.setattr(panel, "_store_result", unavailable)
    result = act(view, sent, "protonation.prepare", report_id=packet["report"]["id"])
    assert result["stage"] == "error"
    assert panel._protonation_decision is panel._report is panel._result is None
    assert not view.addons.manager.presentations.records()
    unchanged(view, before)
