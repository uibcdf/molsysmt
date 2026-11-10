"""Native sparse detector reports keep explicit science, coverage and adoption."""

import json

import molsysviewer as msv
import numpy as np
import pytest

import molsysmt as msm
from molsysviewer_molsysmt._analysis_interactions import INTERACTION_METHODS
from tests.molsysviewer_molsysmt.test_analysis_panel import act, mount
from tests.molsysviewer_molsysmt.test_build_assignment_tools import snapshot, unchanged
from tests.molsysviewer_molsysmt.test_contact_detector_tools import (
    system as contact_system,
)
from tests.molsysviewer_molsysmt.test_interaction_detector_tools import (
    hbond_system,
    sulfur_system,
)
from tests.molsysviewer_molsysmt.test_remaining_interaction_tools import (
    system as aromatic_system,
)
from tests.molsysviewer_molsysmt.test_system_panel import transport

puw = msm.pyunitwizard


def source(family):
    if family == "hbonds":
        return hbond_system()
    if family == "disulfides":
        return sulfur_system()
    if family in {"ionic", "hydrophobic", "halogen_bonds"}:
        return contact_system(family)
    return aromatic_system(family)


def calculate(view, sent, task, *, draft=None, **parameters):
    response = act(
        view,
        sent,
        draft=draft or {"source": "all", "context": "index", "structure_index": 0},
        parameters={
            "task": task,
            "structures": "indices",
            "indices": "2,0,2",
            "interaction_distance": "0.4 nm" if task == "interaction_ionic" else "",
            **(
                dict(
                    interaction_distance="0.6 nm",
                    interaction_angle="30 degrees",
                    interaction_offset="0.2 nm",
                    interaction_planarity="0.02 nm",
                )
                if task == "interaction_pi_pi"
                else {}
            ),
            **parameters,
        },
    )
    assert response["stage"] == "report", response["message"]
    return response


@pytest.mark.parametrize("length", ["nm", "pm"])
@pytest.mark.parametrize("task", list(INTERACTION_METHODS))
def test_nine_native_detectors_keep_sparse_axes_units_and_independent_result(
    task, length
):
    family, name = INTERACTION_METHODS[task]
    with msv.new_view(source(family)) as view:
        sent = transport(view)
        panel = mount(view)
        before = snapshot(view)
        with puw.context(
            standard_units=[
                length,
                "ps",
                "radians",
                "dalton",
                "K",
                "mole",
                "e",
                "dimensionless",
                "kJ/mol",
            ]
        ):
            policy = puw.configure.report()
            response = calculate(view, sent, task)
            native = panel._report.native_values
            args = dict(
                selection=list(range(view.molsys.get_n_atoms())),
                structure_indices=[2, 0, 2],
                pbc=False,
                output_type="molsysmt.Interactions",
            )
            if family == "ionic":
                args["distance_threshold"] = "0.4 nm"
            if family == "pi_pi":
                args.update(
                    distance_threshold="0.6 nm",
                    angle_threshold="30 degrees",
                    offset_threshold="0.2 nm",
                    planarity_threshold="0.02 nm",
                )
            direct = getattr(getattr(msm.interactions, family), name)(
                view.molsys, **args
            )
            from tests.molsysviewer_molsysmt.test_contact_detector_tools import (
                same as same_result,
            )

            same_result(native, direct)
            assert response["report"]["family"] == "interactions"
            assert response["report"]["native_experimental"]
            assert response["report"]["structure_indices"] == [2, 0, 2]
            assert set(response["report"]["evaluated_structure_indices"]) == {0, 2}
            assert response["report"]["rows"] == native.n_interactions > 0
            page = native.to_page(limit=50)
            assert [row[1] for row in response["page"]["rows"]] == page[
                "occurrence_indices"
            ].tolist()
            assert [row[0] for row in response["page"]["rows"]] == page[
                "structure_indices"
            ].tolist()
            assert set(view.molsys.interactions) == set()
            assert not view.interactions.tags()
            assert len(json.dumps(response)) < 100000
            assert puw.configure.report() == policy
            unchanged(view, before)


@pytest.mark.parametrize(
    "task", ["interaction_hbonds", "interaction_pi_pi", "interaction_water"]
)
def test_roles_full_participants_empty_coverage_and_explicit_scientific_then_visual_adoption(
    task, tmp_path
):
    family, _ = INTERACTION_METHODS[task]
    with msv.new_view(source(family)) as view:
        sent = transport(view)
        panel = mount(view)
        response = calculate(view, sent, task, indices="0,1,2")
        raw = panel._report.native_values
        assert (
            len(
                raw.query(structure_indices=[1]).to_page(limit=1)[
                    "evaluated_structure_indices"
                ]
            )
            == 1
        )
        assert raw.query(structure_indices=[1]).n_interactions == 0
        assert raw.query(structure_indices=[2]).n_interactions > 0
        assert raw.n_interactions == response["report"]["rows"]
        page = raw.to_page(limit=1)
        relation = raw.relation(int(page["relation_indices"][0]))
        expected = list(
            dict.fromkeys(
                a for p in relation["participants"] for a in p["atom_indices"].tolist()
            )
        )
        raw_id = response["report"]["id"]
        packet = act(view, sent, "select_participants", report_id=raw_id, row_index=0)
        assert packet["stage"] == "scene", packet["message"]
        assert set(view.active_selection.atom_indices) == set(expected)
        packet = act(view, sent, "focus_participants", report_id=raw_id, row_index=0)
        assert packet["stage"] == "scene"
        packet = act(
            view,
            sent,
            "add_interaction_set",
            report_id=raw_id,
            analysis_name="calculated",
        )
        assert packet["stage"] == "error" and "First store" in packet["message"]
        assert not view.molsys.interactions and not view.interactions.tags()
        packet = act(
            view,
            sent,
            "store_interactions",
            report_id=raw_id,
            analysis_name="calculated",
        )
        assert packet["stage"] == "scene", packet["message"]
        assert "calculated" in view.molsys.interactions and not view.interactions.tags()
        packet = act(
            view,
            sent,
            "add_interaction_set",
            report_id=raw_id,
            analysis_name="calculated",
        )
        assert packet["stage"] == "scene", packet["message"]
        assert len(view.interactions.tags()) == 1
        visual = view.interactions.get(view.interactions.tags()[0])
        visual.hide()
        visual.show()
        view.interactions.delete(visual.tag)
        assert "calculated" in view.molsys.interactions
        act(view, sent, "clear")
        assert panel._report is None and "calculated" in view.molsys.interactions
        assert raw.n_interactions > 0
        filename = tmp_path / "scientific.h5msm"
        msm.convert(view.molsys, to_form=str(filename))
        loaded = msm.convert(str(filename))
        from tests.molsysviewer_molsysmt.test_contact_detector_tools import (
            same as same_result,
        )

        same_result(loaded.interactions["calculated"], raw)


@pytest.mark.parametrize("mode", ["internal", "incident", "between"])
def test_explicit_search_scopes_retain_participant_source_membership(mode):
    with msv.new_view(contact_system("ionic")) as view:
        sent = transport(view)
        panel = mount(view)
        packet = act(
            view,
            sent,
            draft={
                "source": "indices",
                "indices": "0",
                "context": "index",
                "structure_index": 0,
            },
            second={
                "source": "indices",
                "indices": "1",
                "context": "index",
                "structure_index": 0,
            },
            parameters={
                "task": "interaction_ionic",
                "structures": "all",
                "interaction_mode": mode,
                "interaction_distance": "0.4 nm",
            },
        )
        assert packet["stage"] == "report", packet["message"]
        assert panel._report.native_values.evaluation_mode == mode
        assert packet["report"]["rows"] == (0 if mode == "internal" else 2)
        assert panel._report.native_values.evaluated_structure_indices.tolist() == [
            0,
            1,
            2,
        ]


def test_periodic_images_and_geometry_remain_native_in_sparse_report():
    with msv.new_view(hbond_system(periodic=True)) as view:
        sent = transport(view)
        panel = mount(view)
        packet = calculate(view, sent, "interaction_hbonds", indices="0", pbc=True)
        page = panel._report.native_values.to_page(limit=50)
        assert page["image_vectors"] is not None and np.any(page["image_vectors"])
        assert any(row[-1] != "null" for row in packet["page"]["rows"])
        raw = panel._report.native_values
        xyz = puw.get_value(view.molsys.structures.coordinates, to_unit="nm")[0]
        box = puw.get_value(view.molsys.structures.box, to_unit="nm")[0]
        for i, relation_index in enumerate(page["relation_indices"]):
            participants = raw.relation(int(relation_index))["participants"]
            a, b = page["image_offsets"][i : i + 2]
            images = page["image_vectors"][a:b]
            positions = {
                p["role"]: xyz[p["atom_indices"][0]] + image @ box
                for p, image in zip(participants, images, strict=True)
            }
            actual = np.linalg.norm(positions["hydrogen"] - positions["acceptor"])
            assert actual == pytest.approx(
                page["measurements"]["hydrogen_acceptor_distance"][i]
            )


def test_name_conflicts_stale_results_and_missing_prerequisites_preserve_science():
    with msv.new_view(hbond_system()) as view:
        sent = transport(view)
        panel = mount(view)
        packet = calculate(view, sent, "interaction_hbonds")
        token = packet["report"]["id"]
        packet = act(
            view, sent, "store_interactions", report_id=token, analysis_name="saved"
        )
        assert packet["stage"] == "scene", packet["message"]
        stored = view.molsys.interactions["saved"]
        packet = act(
            view, sent, "store_interactions", report_id=token, analysis_name="saved"
        )
        assert (
            packet["stage"] == "error" and view.molsys.interactions["saved"] is stored
        )
        act(view, sent, "clear")
        packet = act(
            view, sent, "add_interaction_set", report_id=token, analysis_name="saved"
        )
        assert packet["stage"] == "error" and not view.interactions.tags()
    with msv.demo["pentalanine"] as view:
        sent = transport(view)
        panel = mount(view)
        before = snapshot(view)
        packet = act(
            view,
            sent,
            draft={"source": "all"},
            parameters={"task": "interaction_pi_pi"},
        )
        assert packet["stage"] == "error" and panel._report is None
        unchanged(view, before)


@pytest.mark.parametrize(
    "parameters",
    [
        {"interaction_mode": "cross"},
        {"interaction_mode": []},
        {"hbond_method": "buch"},
        {"interaction_distance": "0.4"},
        {"interaction_profile": "unknown-profile"},
        {"interaction_angle": "nan degrees"},
        {"interaction_distance": None},
    ],
)
def test_invalid_scientific_settings_do_not_change_source_or_scene(parameters):
    with msv.new_view(hbond_system()) as view:
        sent = transport(view)
        panel = mount(view)
        before = snapshot(view)
        packet = act(
            view,
            sent,
            draft={"source": "all"},
            parameters={"task": "interaction_hbonds", **parameters},
        )
        assert packet["stage"] == "error" and panel._report is None
        unchanged(view, before)


def test_ionic_threshold_has_no_hidden_universal_default():
    with msv.new_view(contact_system("ionic")) as view:
        sent = transport(view)
        mount(view)
        before = snapshot(view)
        packet = act(
            view,
            sent,
            draft={"source": "all"},
            parameters={"task": "interaction_ionic"},
        )
        assert (
            packet["stage"] == "error"
            and "explicit distance threshold" in packet["message"]
        )
        unchanged(view, before)


@pytest.mark.parametrize("task", list(INTERACTION_METHODS))
def test_periodic_request_without_box_reports_native_nonperiodic_effect(task):
    family, _ = INTERACTION_METHODS[task]
    with msv.new_view(source(family)) as view:
        sent = transport(view)
        panel = mount(view)
        calculate(view, sent, task, pbc=False)
        previous = panel._report.native_values.to_page(limit=50)
        response = calculate(view, sent, task, pbc=True)
        actual = panel._report.native_values.to_page(limit=50)
        assert response["report"]["requested_pbc"] is True
        assert response["report"]["periodic"] is False
        assert "No box is stored" in response["report"]["notice"]
        np.testing.assert_array_equal(
            actual["structure_indices"], previous["structure_indices"]
        )
        for name, value in previous["measurements"].items():
            np.testing.assert_array_equal(actual["measurements"][name], value)
