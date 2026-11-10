"""Source-mapped native reports, explicit units, independent controls and effects."""

import numpy as np
import pytest

import molsysmt as msm
from tests.molsysviewer_molsysmt.test_analysis_panel import act
from tests.molsysviewer_molsysmt.test_analysis_panel import case as case
from tests.molsysviewer_molsysmt.test_build_assignment_tools import snapshot, unchanged

puw = msm.pyunitwizard
ATOMS = {
    "source": "indices",
    "indices": "20, 10, 6, 20",
    "context": "index",
    "structure_index": 0,
}


def calculate(case, task, **parameters):
    view, sent, panel = case
    result = act(
        view,
        sent,
        draft=ATOMS,
        parameters={
            "task": task,
            "structures": "indices",
            "indices": "2, 0, 2",
            **parameters,
        },
    )
    assert result["stage"] == "report", result["message"]
    return result, panel._report


@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize(
    "task",
    [
        "mass",
        "reference_charge",
        "hydrophobicity",
        "polarity",
        "sequence",
        "bonds",
        "blocks",
    ],
)
def test_native_reports_keep_source_axes_and_original_system(case, task, unit):
    view, sent, panel = case
    original = snapshot(view)
    with puw.context(
        standard_units=[unit, "ps", "radians", "dalton", "elementary_charge", "kelvin"]
    ):
        result, report = calculate(case, task)
    metadata = report.auxiliary
    assert result["report"]["family"] == "property"
    assert result["report"]["method"].startswith("molsysmt.")
    assert len(result["page"]["rows"]) <= 50
    atoms = [20, 10, 6, 20]
    groups = list(
        dict.fromkeys(
            map(
                int,
                msm.get(view.molsys, element="atom", selection=atoms, group_index=True),
            )
        )
    )
    if task == "mass":
        expected = msm.physchem.get_mass(view.molsys, element="atom", selection=atoms)
        np.testing.assert_allclose(
            [float(row[-1]) for row in result["page"]["rows"]],
            puw.get_value(expected, to_unit="dalton"),
            rtol=2e-9,
        )
        # Atomic symbols provide an independent table control for standard mass.
        symbols = msm.get(view.molsys, element="atom", selection=atoms, atom_type=True)
        oracle = {"C": 12.011, "H": 1.008, "O": 15.999, "N": 14.007}
        np.testing.assert_allclose(
            report.values, [oracle[s] for s in symbols], atol=0.001
        )
        assert [row[0] for row in result["page"]["rows"]] == atoms
    elif task in {"reference_charge", "hydrophobicity", "polarity"}:
        method, definition = {
            "reference_charge": ("get_charge", "physical_pH7"),
            "hydrophobicity": ("get_hydrophobicity", "eisenberg"),
            "polarity": ("get_polarity", "grantham"),
        }[task]
        expected = getattr(msm.physchem, method)(
            view.molsys, element="group", selection=groups, definition=definition
        )
        if task == "reference_charge":
            expected = puw.get_value(expected, to_unit="elementary_charge")
            assert "not stored formal" in result["report"]["notice"]
        np.testing.assert_allclose(report.values, expected)
        assert [row[0] for row in result["page"]["rows"]] == groups
        for group, members in zip(groups, metadata["members"], strict=True):
            expected_members = msm.get(
                view.molsys, element="group", selection=[group], atom_index=True
            )[0]
            assert members == list(map(int, expected_members))
    elif task == "sequence":
        assert [row[0] for row in result["page"]["rows"]] == groups
        for name, code in zip(metadata["names"], report.values, strict=True):
            assert code == ("A" if name == "ALA" else "")
    else:
        native = msm.chemical_states.get_bondgraph(view.molsys, selection=atoms)
        if task == "bonds":
            assert metadata["members"] == [list(pair) for pair in native.edges]
        else:
            import networkx as nx

            assert metadata["members"] == [
                sorted(block) for block in nx.connected_components(native)
            ]
    assert result["report"]["structure_indices"] == (
        [2, 0, 2] if task in {"bonds", "blocks"} else []
    )
    unchanged(view, original)


@pytest.mark.parametrize("element", ["atom", "group"])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_sasa_exact_axes_and_explicit_area_units_include_all_occluders(
    case, element, unit
):
    view, _, _ = case
    original = snapshot(view)
    with puw.context(
        standard_units=[unit, "ps", "radians", "dalton", "elementary_charge", "kelvin"]
    ):
        result, report = calculate(case, "sasa", property_element=element)
    indices = report.auxiliary["indices"].tolist()
    expected = msm.physchem.get_sasa(
        view.molsys,
        element=element,
        selection=indices,
        structure_indices=[2, 0, 2],
        pbc=False,
        parallel=False,
        num_threads=1,
        use_gpu=False,
    )
    np.testing.assert_allclose(
        report.values, puw.get_value(expected, to_unit="nm**2"), rtol=2e-10
    )
    assert result["report"]["unit"] == "nm**2"
    assert [r[0] for r in result["page"]["rows"]] == [
        f for f in [2, 0, 2] for _ in indices
    ]
    assert [r[1] for r in result["page"]["rows"]] == indices * 3
    np.testing.assert_allclose(
        [float(r[2]) for r in result["page"]["rows"]], report.values.ravel(), rtol=5e-9
    )
    assert "including solvent" in result["report"]["notice"]
    unchanged(view, original)


def test_group_mass_participants_and_focus_preserve_source_and_visible_structure(case):
    view, sent, panel = case
    result, report = calculate(case, "mass", property_element="group")
    expected = report.auxiliary["members"][0]
    old_frame = view.player.index
    action = act(
        view,
        sent,
        action="select_participants",
        report_id=result["report"]["id"],
        row_index=0,
    )
    assert action["stage"] == "scene", action["message"]
    assert sorted(view.active_selection.atom_indices) == sorted(expected)
    focused = act(
        view,
        sent,
        action="focus_participants",
        report_id=result["report"]["id"],
        row_index=0,
    )
    assert focused["stage"] == "scene", focused["message"]
    assert view.player.index == old_frame
    refused = act(
        view,
        sent,
        action="add_live_distance",
        report_id=result["report"]["id"],
        row_index=0,
    )
    assert refused["stage"] == "error" and "not a pair distance" in refused["message"]
    assert len(view.measurements.info()) == 0


@pytest.mark.parametrize(
    "parameters",
    [
        {"probe_radius": "nan"},
        {"sphere_points": "0"},
        {"probe_unit": "seconds"},
        {"sasa_engine": "automatic"},
        {"assume_complete": 1},
        {"property_element": "system"},
    ],
)
def test_invalid_property_inputs_refuse_without_editing(case, parameters):
    view, sent, panel = case
    original = snapshot(view)
    result = act(view, sent, draft=ATOMS, parameters={"task": "sasa", **parameters})
    assert result["stage"] == "error"
    assert panel._report is None
    unchanged(view, original)


def test_report_expiry_and_clear_release_native_data(case):
    view, sent, panel = case
    result, report = calculate(case, "mass")
    view.player.go_to_structure(1)
    response = act(view, sent, action="refresh")
    # Explicit selection context and static data can remain valid when only the
    # visible structure changes; no fictional per-structure mass evaluation.
    assert response["report"]["id"] == result["report"]["id"]
    cleared = act(view, sent, action="clear")
    assert cleared["report"] is None and panel._report is None
    stale = act(
        view, sent, action="select_participants", report_id=report.token, row_index=0
    )
    assert stale["stage"] == "error"


@pytest.mark.parametrize("task", ["hydrophobicity", "polarity"])
def test_unsupported_reference_group_is_not_filtered_or_prepared(case, task):
    view, sent, panel = case
    before = snapshot(view)
    response = act(
        view, sent, draft={**ATOMS, "indices": "0,6"}, parameters={"task": task}
    )
    assert response["stage"] == "error" and "ACE" in response["message"]
    assert panel._report is None
    unchanged(view, before)


def test_sequence_keeps_omitted_caps_and_explicit_source_group_mapping(case):
    view, sent, panel = case
    response = act(
        view,
        sent,
        draft={**ATOMS, "indices": "0,20,6"},
        parameters={"task": "sequence"},
    )
    assert response["stage"] == "report", response["message"]
    rows = response["page"]["rows"]
    assert rows[0] == [0, "ACE", "omitted by native projection"]
    assert [row[2] for row in rows[1:]] == ["A", "A"]
    assert response["report"]["structure_indices"] == []


def test_static_reports_ignore_hidden_structure_and_second_population_inputs(case):
    view, sent, panel = case
    response = act(
        view,
        sent,
        draft=ATOMS,
        second={"source": "none"},
        parameters={
            "task": "mass",
            "structures": "indices",
            "indices": "invalid hidden value",
        },
    )
    assert response["stage"] == "report", response["message"]
    view.player.go_to_structure(1)
    assert act(view, sent, "refresh")["report"]["id"] == response["report"]["id"]


def test_fifty_row_pages_preserve_source_axis_and_reject_invisible_row_actions(case):
    view, sent, panel = case
    response = act(
        view,
        sent,
        draft={"source": "all", "context": "index", "structure_index": 0},
        parameters={"task": "mass"},
    )
    assert response["stage"] == "report", response["message"]
    assert len(response["page"]["rows"]) == 50
    report_id = response["report"]["id"]
    page = act(view, sent, "page", report_id=report_id, offset=50)
    assert [r[0] for r in page["page"]["rows"]] == list(range(50, 62))
    refused = act(view, sent, "select_participants", report_id=report_id, row_index=0)
    assert refused["stage"] == "error" and "current page" in refused["message"]


def test_ring_report_uses_native_memberships_and_rejects_cut_rings():
    import molsysviewer as msv

    from tests.molsysviewer_molsysmt.test_analysis_panel import mount
    from tests.molsysviewer_molsysmt.test_aromatic_tools import (
        CAFFEINE_RINGS,
        caffeine_system,
    )
    from tests.molsysviewer_molsysmt.test_system_panel import transport

    with msv.new_view(caffeine_system()) as view:
        before = snapshot(view)
        sent = transport(view)
        panel = mount(view)
        result = act(view, sent, draft={"source": "all"}, parameters={"task": "rings"})
        assert result["stage"] == "report", result["message"]
        assert {
            tuple(row) for row in panel._report.auxiliary["members"]
        } == CAFFEINE_RINGS
        assert result["report"]["structure_indices"] == [0]
        assert "not all cycles" in result["report"]["notice"]
        cut = act(view, sent, draft={"source": "indices", "indices": "1,2,3"})
        assert cut["stage"] == "error" and panel._report is None
        unchanged(view, before)


def test_frontend_is_valid_javascript_module():
    import subprocess

    from molsysviewer_molsysmt._analysis_panel_frontend import ESM

    subprocess.run(
        ["node", "--input-type=module", "--check"], input=ESM, text=True, check=True
    )
