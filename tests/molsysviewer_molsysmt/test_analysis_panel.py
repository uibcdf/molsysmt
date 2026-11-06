"""Native geometric analysis, global result axes, bounded pages and lifetimes."""

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
from tests.molsysviewer_molsysmt.test_system_panel import transport

puw = msm.pyunitwizard
A = {"source": "indices", "indices": "4 0 4", "context": "index", "structure_index": 1}
B = {"source": "indices", "indices": "5 2", "context": "index", "structure_index": 2}
FRAMES = [2, 0, 2]


def mount(view, endpoint=None):
    view._handle_frontend_event(
        {
            "event": "panel_navigate",
            "addon": "molsysmt",
            "panel": "analysis",
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
    view,
    sent,
    action="calculate",
    *,
    draft=None,
    second=None,
    parameters=None,
    endpoint=None,
    **extra,
):
    old = state(sent, endpoint)
    payload = {
        "request_id": old["request_id"] + 1,
        "draft": old["draft"] if draft is None else draft,
        "second": old["second"] if second is None else second,
        "parameters": old["parameters"] if parameters is None else parameters,
        **extra,
    }
    view._handle_frontend_event(
        {
            "event": "addon_panel_action",
            "addon": "molsysmt",
            "panel": "analysis",
            "_panel_endpoint_id": endpoint,
            "content": {"type": "action", "id": action, "payload": payload},
        }
    )
    return state(sent, endpoint)


@pytest.fixture
def case():
    with msv.demo["pentalanine"] as seed:
        with msv.new_view(seed.molsys, structure_indices=[0, 8, 3]) as view:
            view.regions.add(selection=[4, 0], tag="chosen")
            view.selections.add("chosen", atom_indices=[4, 0])
            view.active_selection.set([4, 0])
            sent = transport(view)
            panel = mount(view)
            yield view, sent, panel


def calculate(case, task="distances", *, a=A, b=B, **parameters):
    view, sent, _ = case
    result = act(
        view,
        sent,
        draft=a,
        second=b,
        parameters={
            "task": task,
            "structures": "indices",
            "indices": "2,0,2",
            **parameters,
        },
    )
    assert result["stage"] == "report", result["message"]
    return result


def _conformation_oracle(
    xyz, task, atoms, structures, reference_atoms, reference, weights=None
):
    selected = xyz[structures][:, atoms]
    if task == "rmsf":
        return np.sqrt(
            np.mean(np.sum((selected - selected.mean(axis=0)) ** 2, axis=2), axis=0)
        )
    if task == "gyration":
        center = np.average(selected, axis=1, weights=weights)
        squared = np.sum((selected - center[:, None]) ** 2, axis=2)
        return np.sqrt(np.average(squared, axis=1, weights=weights))
    target = xyz[reference, reference_atoms]
    if task == "rmsd":
        return np.sqrt(np.mean(np.sum((selected - target) ** 2, axis=2), axis=1))
    target = target - target.mean(axis=0)
    results = []
    for coords in selected:
        centered = coords - coords.mean(axis=0)
        u, _, vt = np.linalg.svd(centered.T @ target)
        correction = np.diag([1.0, 1.0, np.linalg.det(u @ vt)])
        fitted = centered @ (u @ correction @ vt)
        results.append(np.sqrt(np.mean(np.sum((fitted - target) ** 2, axis=1))))
    return np.array(results)


@pytest.mark.parametrize("task", ["rmsd", "least_rmsd", "gyration", "rmsf"])
@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize("structures", ["2, 0, 2", "1"])
def test_conformations_preserve_native_axes_and_match_independent_geometry(
    case, task, unit, structures
):
    view, sent, panel = case
    before = snapshot(view)
    atoms = [4, 0, 2, 4]
    draft = {**A, "indices": "4,0,2,4"}
    frames = [int(i) for i in structures.replace(",", " ").split()]
    coords = puw.get_value(view.molsys.structures.coordinates, to_unit="nm")
    expected = _conformation_oracle(coords, task, atoms, frames, atoms, 1)
    with puw.context(standard_units=[unit, "ps", "radians"]):
        result = calculate(
            case, task, a=draft, indices=structures, reference_structure="1"
        )
        assert puw.get_unit(panel._report.values) == puw.unit(unit)
    assert result["report"]["family"] == "conformation"
    assert result["report"]["structure_indices"] == frames
    assert result["report"]["result_axis"] == (
        "atom" if task == "rmsf" else "structure"
    )
    rows = result["page"]["rows"]
    assert [row[0] for row in rows] == (atoms if task == "rmsf" else frames)
    np.testing.assert_allclose([float(row[1]) for row in rows], expected, atol=2e-9)
    np.testing.assert_allclose(
        puw.get_value(panel._report.values, to_unit="nm"), expected, atol=2e-9
    )
    assert result["report"]["reference_structure_index"] == (
        1 if "rmsd" in task else None
    )
    assert result["report"]["requested_pbc"] is False
    unchanged(view, before)


@pytest.mark.parametrize("task", ["rmsd", "least_rmsd"])
def test_rmsd_reference_atoms_are_explicit_positional_correspondence(case, task):
    view, _, panel = case
    before = snapshot(view)
    atoms, reference_atoms = [4, 0, 2, 4], [5, 2, 3, 5]
    result = calculate(
        case,
        task,
        a={**A, "indices": "4 0 2 4"},
        b={**B, "indices": "5 2 3 5"},
        reference_population="second",
        reference_structure="1",
    )
    xyz = puw.get_value(view.molsys.structures.coordinates, to_unit="nm")
    expected = _conformation_oracle(xyz, task, atoms, FRAMES, reference_atoms, 1)
    np.testing.assert_allclose(
        puw.get_value(panel._report.values, to_unit="nm"), expected, atol=2e-9
    )
    assert result["report"]["second_atoms"] == 4
    unchanged(view, before)


@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_gyration_mass_weighting_uses_native_standard_mass_table_without_edits(
    case, unit
):
    view, _, panel = case
    before = snapshot(view)
    atoms = [4, 0, 2, 4]
    masses = puw.get_value(
        msm.physchem.get_mass(view.molsys, element="atom", selection=atoms),
        to_unit="dalton",
    )
    xyz = puw.get_value(view.molsys.structures.coordinates, to_unit="nm")
    expected = _conformation_oracle(xyz, "gyration", atoms, FRAMES, atoms, 0, masses)
    with puw.context(standard_units=[unit, "ps", "dalton"]):
        calculate(case, "gyration", a={**A, "indices": "4 0 2 4"}, weighting="masses")
    np.testing.assert_allclose(
        puw.get_value(panel._report.values, to_unit="nm"), expected, atol=2e-12
    )
    unchanged(view, before)


def test_mass_weighting_retains_native_missing_mass_unit_diagnostic(case):
    view, sent, _ = case
    before = snapshot(view)
    with puw.context(standard_units=["nm", "ps"]):
        result = act(
            view, sent, draft=A, parameters={"task": "gyration", "weighting": "masses"}
        )
    assert result["stage"] == "error" and "standard units" in result["message"]
    unchanged(view, before)


@pytest.mark.parametrize("task", ["rmsd", "least_rmsd", "gyration"])
def test_deliberate_structure_plot_uses_core_axis_ownership_and_survives_clear(
    case, task
):
    view, sent, panel = case
    result = calculate(
        case,
        task,
        a={**A, "indices": "4 0 2 4"},
        structures="all",
        reference_structure="1",
    )
    native_values = puw.get_value(panel._report.values, to_unit="nm").copy()
    assert not result["report"]["plot_unavailable"]
    source = snapshot(view)
    plotted = act(view, sent, "add_structure_plot", report_id=result["report"]["id"])
    assert plotted["stage"] == "scene", plotted["message"]
    tag = plotted["scene_action"]["plot_tag"]
    record = view.trajectory_plot.records()[0]
    assert record["tag"] == tag and record["n_frames"] == 3
    assert record["x_label"] == "Structure index" and record["y_label"] == "Length (nm)"
    np.testing.assert_allclose(record["series"][0]["values"], native_values)
    assert panel._report.token == result["report"]["id"]
    # Repeating adoption updates the same core object, never recalculates science.
    act(view, sent, "add_structure_plot", report_id=result["report"]["id"])
    assert len(view.trajectory_plot.records()) == 1
    act(view, sent, "clear")
    assert panel._report is None and view.trajectory_plot.records()[0]["tag"] == tag
    assert view.molsys is source[0]
    same(view.molsys, source[1])
    assert view.addons.molsysmt.get_sync_status() == source[3]


@pytest.mark.parametrize(
    "task,structures",
    [
        ("rmsf", "0,1,2"),
        ("rmsd", "2,0"),
        ("gyration", "2,1,0"),
        ("least_rmsd", "0,0,2"),
    ],
)
def test_nonstructure_or_partial_reordered_repeated_axes_cannot_be_padded_into_plot(
    case, task, structures
):
    view, sent, _ = case
    result = calculate(case, task, a={**A, "indices": "4 0 2 4"}, indices=structures)
    before = snapshot(view)
    assert result["report"]["plot_unavailable"]
    rejected = act(view, sent, "add_structure_plot", report_id=result["report"]["id"])
    assert rejected["stage"] == "error"
    assert not view.trajectory_plot.records()
    unchanged(view, before)


def test_rmsf_rows_page_atom_indices_and_select_one_source_atom(case):
    view, sent, panel = case
    atoms = list(range(view.molsys.get_n_atoms())) + [4, 0]
    result = calculate(case, "rmsf", a={**A, "indices": " ".join(map(str, atoms))})
    assert result["page"]["columns"] == ["Atom index", "Value (nm)"]
    assert len(result["page"]["rows"]) == 50 and result["page"]["total"] == len(atoms)
    report_id = result["report"]["id"]
    page = act(view, sent, "page", report_id=report_id, offset=50)
    assert [row[0] for row in page["page"]["rows"]] == atoms[50:100]
    selected = act(view, sent, "select_participants", report_id=report_id, row_index=51)
    assert selected["stage"] == "scene"
    assert selected["scene_action"]["observation_structure_index"] is None
    assert view.active_selection.atom_indices == [atoms[51]]
    rejected = act(view, sent, "add_live_distance", report_id=report_id, row_index=51)
    assert rejected["stage"] == "error" and "not a pair distance" in rejected["message"]
    assert panel._report is not None


@pytest.mark.parametrize(
    "parameters",
    [
        {"reference_structure": "-1"},
        {"reference_structure": "3"},
        {"reference_structure": "0.5"},
        {"reference_population": "unknown"},
        {"reference_structure": 0},
    ],
)
def test_conformation_reference_validation_preserves_data_and_scene(case, parameters):
    view, sent, _ = case
    before = snapshot(view)
    result = act(view, sent, draft=A, parameters={"task": "rmsd", **parameters})
    assert result["stage"] == "error"
    unchanged(view, before)


def test_conformation_pending_reader_uses_current_coordinates_without_projecting_plot(
    case,
):
    view, sent, panel = case
    coordinates = puw.get_value(view.molsys.structures.coordinates, to_unit="nm").copy()
    coordinates[2, 4] += [0.3, 0.1, -0.2]
    view.addons.molsysmt.basic.set(
        coordinates=puw.quantity(coordinates, "nm"), update_view=False
    )
    before = snapshot(view)
    result = calculate(case, "rmsd", structures="all")
    expected = _conformation_oracle(
        coordinates, "rmsd", [4, 0, 4], [0, 1, 2], [4, 0, 4], 0
    )
    np.testing.assert_allclose(
        puw.get_value(panel._report.values, to_unit="nm"), expected
    )
    assert result["context"]["state"] == "pending"
    assert "add_structure_plot" not in panel.read_only_actions
    start = len(sent)
    act(view, sent, "add_structure_plot", report_id=result["report"]["id"])
    assert panel._report.token == result["report"]["id"]
    assert not any(
        message.get("op") == "set_trajectory_plot" for message in sent[start:]
    )
    unchanged(view, before)


@pytest.mark.parametrize(
    "change", ["revision", "reference_selection", "unmount", "foreign"]
)
def test_stale_conformation_results_cannot_publish_plots(case, change):
    view, sent, panel = case
    draft = {**A, "source": "saved", "value": "chosen"}
    result = calculate(case, "gyration", a=draft, structures="all")
    token = result["report"]["id"]
    if change == "revision":
        view.addons.molsysmt.structure.translate(
            translation=puw.quantity([1, 0, 0], "nm"), in_place=True
        )
    elif change == "reference_selection":
        view.selections.delete("chosen")
    elif change == "unmount":
        view._handle_frontend_event(
            {"event": "panel_unmount", "addon": "molsysmt", "panel": "analysis"}
        )
        mount(view)
    else:
        token = "foreign"
    before = snapshot(view)
    rejected = act(view, sent, "add_structure_plot", report_id=token)
    assert rejected["stage"] == "error" and "expired" in rejected["message"]
    unchanged(view, before)


def test_plot_failure_and_retry_do_not_repeat_the_native_calculation(case, monkeypatch):
    view, sent, panel = case
    calls = []
    method = view.addons.molsysmt.structure.get_radius_of_gyration

    def counted(**parameters):
        calls.append(parameters)
        return method(**parameters)

    monkeypatch.setattr(
        view.addons.molsysmt.structure, "get_radius_of_gyration", counted
    )
    result = calculate(case, "gyration", structures="all")
    values = panel._report.values
    show = view.trajectory_plot.show

    def rejected(*args, **kwargs):
        raise RuntimeError("Injected plot failure before publication")

    monkeypatch.setattr(view.trajectory_plot, "show", rejected)
    failed = act(view, sent, "add_structure_plot", report_id=result["report"]["id"])
    assert failed["stage"] == "error" and len(calls) == 1
    assert panel._report.values is values and not view.trajectory_plot.records()
    refreshed = act(view, sent, "refresh")
    assert "Injected plot failure" in refreshed["message"]
    monkeypatch.setattr(view.trajectory_plot, "show", show)
    retried = act(view, sent, "add_structure_plot", report_id=result["report"]["id"])
    assert retried["stage"] == "scene" and len(calls) == 1
    assert panel._report.values is values


@pytest.mark.parametrize("task", ["distances", "minimum", "maximum"])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_native_distances_extrema_order_and_units_against_coordinate_oracle(
    case, task, unit
):
    view, sent, _ = case
    before = snapshot(view)
    xyz = puw.get_value(view.molsys.structures.coordinates, to_unit="nm")
    matrix = np.linalg.norm(
        xyz[FRAMES][:, [4, 0, 4], None] - xyz[FRAMES][:, None, [5, 2]], axis=-1
    )
    with puw.context(standard_units=[unit, "ps"]):
        result = calculate(case, task)
    rows = result["page"]["rows"]
    if task == "distances":
        assert len(rows) == 18
        expected = [[f, a, b] for f in FRAMES for a in [4, 0, 4] for b in [5, 2]]
        np.testing.assert_array_equal([r[:3] for r in rows], expected)
        np.testing.assert_allclose(
            [float(r[3]) for r in rows], matrix.ravel(), atol=1e-8
        )
    else:
        chooser = np.argmin if task == "minimum" else np.argmax
        expected = []
        for frame, slab in zip(FRAMES, matrix, strict=True):
            a, b = np.unravel_index(chooser(slab), slab.shape)
            expected.append([frame, [4, 0, 4][a], [5, 2][b], slab[a, b]])
        np.testing.assert_allclose(np.array(rows, dtype=float), expected, atol=1e-8)
    assert result["report"]["structure_indices"] == FRAMES
    assert result["report"]["unit"] == "nm"
    assert not result["report"]["periodic"]
    unchanged(view, before)


@pytest.mark.parametrize("task", ["distances", "minimum", "maximum"])
def test_corresponding_pairs_keep_supplied_order_and_repeated_atoms(case, task):
    b = {**B, "indices": "5 2 5"}
    result = calculate(case, task, b=b, pairing="paired")
    view, _, _ = case
    xyz = puw.get_value(view.molsys.structures.coordinates, to_unit="nm")[FRAMES]
    values = np.linalg.norm(xyz[:, [4, 0, 4]] - xyz[:, [5, 2, 5]], axis=-1)
    expected = (
        values.ravel()
        if task == "distances"
        else (np.min(values, axis=1) if task == "minimum" else np.max(values, axis=1))
    )
    np.testing.assert_allclose(
        [float(r[3]) for r in result["page"]["rows"]], expected, atol=1e-8
    )


@pytest.mark.parametrize(
    "first_mode,second_mode",
    [("geometric", "atoms"), ("atoms", "geometric"), ("mass", "mass")],
)
def test_population_centers_are_not_reported_as_fictitious_atom_indices(
    case, first_mode, second_mode
):
    view, _, _ = case
    result = calculate(case, first_endpoint=first_mode, second_endpoint=second_mode)
    xyz = puw.get_value(view.molsys.structures.coordinates, to_unit="nm")[FRAMES]
    endpoints = []
    for indices, mode in [([4, 0, 4], first_mode), ([5, 2], second_mode)]:
        values = xyz[:, indices]
        if mode != "atoms":
            weights = (
                puw.get_value(
                    msm.physchem.get_mass(
                        view.molsys, element="atom", selection=indices
                    )
                )
                if mode == "mass"
                else None
            )
            values = np.average(values, axis=1, weights=weights)[:, None]
        endpoints.append(values)
    expected = np.linalg.norm(endpoints[0][:, :, None] - endpoints[1][:, None], axis=-1)
    np.testing.assert_allclose(
        [float(r[3]) for r in result["page"]["rows"]], expected.ravel(), atol=1e-8
    )
    for row in result["page"]["rows"]:
        assert (row[1] == "Center A") == (first_mode != "atoms")
        assert (row[2] == "Center B") == (second_mode != "atoms")


@pytest.mark.parametrize("relation", ["within", "between"])
@pytest.mark.parametrize("criterion", ["cutoff", "count"])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_neighbors_global_atoms_inclusive_cutoff_and_native_self_policy(
    case, relation, criterion, unit
):
    view, _, _ = case
    first = {**A, "indices": "4 0 2"}
    second = {**B, "indices": "5 2 4"}
    args = dict(relation=relation, neighbor_mode=criterion, cutoff="0.5", count="2")
    with puw.context(standard_units=[unit, "ps"]):
        result = calculate(case, "neighbors", a=first, b=second, **args)
    xyz = puw.get_value(view.molsys.structures.coordinates, to_unit="nm")
    expected = []
    for frame in FRAMES:
        for a in [4, 0, 2]:
            population = [5, 2, 4] if relation == "between" else [4, 0, 2]
            candidates = [
                (np.linalg.norm(xyz[frame, a] - xyz[frame, b]), i, b)
                for i, b in enumerate(population)
                if relation == "between" or b != a
            ]
            candidates.sort(key=lambda x: (x[0], x[1]))
            chosen = (
                [c for c in candidates if c[0] <= 0.5]
                if criterion == "cutoff"
                else candidates[:2]
            )
            expected.extend([[frame, a, b, d] for d, _, b in chosen])
    np.testing.assert_allclose(
        np.array(result["page"]["rows"], dtype=float), expected[:50], atol=1e-8
    )
    assert result["report"]["rows"] == len(expected)


@pytest.mark.parametrize(
    "parameters", [{"neighbor_mode": "count", "count": "0"}, {"cutoff": "0"}]
)
def test_zero_neighbors_is_evaluated_result_not_missing_or_failed(case, parameters):
    result = calculate(
        case,
        "neighbors",
        a={**A, "indices": "4"},
        b={**B, "indices": "5"},
        **parameters,
    )
    assert result["report"]["rows"] == 0 and result["page"]["rows"] == []


@pytest.mark.parametrize(
    "first_mode,second_mode",
    [("geometric", "atoms"), ("atoms", "geometric"), ("mass", "mass")],
)
def test_neighbor_centers_retain_population_labels_and_native_geometry(
    case, first_mode, second_mode
):
    result = calculate(
        case,
        "neighbors",
        a={**A, "indices": "4 0 2"},
        first_endpoint=first_mode,
        second_endpoint=second_mode,
        cutoff="100",
    )
    for row in result["page"]["rows"]:
        assert (row[1] == "Center A") == (first_mode != "atoms")
        assert (row[2] == "Center B") == (second_mode != "atoms")
    assert result["report"]["rows"] == 3 * (1 if first_mode != "atoms" else 3) * (
        1 if second_mode != "atoms" else 2
    )


@pytest.mark.parametrize("task", ["distances", "minimum", "maximum", "neighbors"])
def test_within_one_population_preserves_native_directed_self_and_center_semantics(
    case, task
):
    result = calculate(case, task, relation="within", cutoff="100")
    if task == "distances":
        assert len(result["page"]["rows"]) == 27
        assert any(
            row[1] == row[2] and float(row[3]) == 0 for row in result["page"]["rows"]
        )
    elif task == "minimum":
        assert all(float(row[3]) == 0 for row in result["page"]["rows"])
    elif task == "neighbors":
        assert all(row[1] != row[2] for row in result["page"]["rows"])


@pytest.mark.parametrize("change", ["inputs", "source", "unmount"])
def test_disk_backing_retires_when_its_scientific_context_is_abandoned(case, change):
    view, sent, panel = case
    with msm.configure.context(
        max_ram_usage=4096, chunk_memory_fraction=None, chunk_size=2
    ):
        result = calculate(case, indices=",".join("0" for _ in range(120)))
    path = panel._report.native_values.path
    assert path.exists() and result["report"]["disk_backed"]
    if change == "inputs":
        act(view, sent, "refresh", draft={**A, "indices": "1"})
    elif change == "source":
        view.addons.molsysmt.structure.translate(
            translation="[0.1,0,0] nm", in_place=True
        )
        act(view, sent, "refresh")
    else:
        panel.on_unmount(view)
    assert panel._report is None and not path.exists()


@pytest.mark.parametrize("task", ["distances", "minimum", "maximum", "neighbors"])
def test_periodic_result_metadata_and_values_follow_stored_row_vector_box(case, task):
    view, _, _ = case
    view.addons.molsysmt.basic.set(
        box=puw.quantity(np.repeat(np.diag([3.0, 4.0, 5.0])[None], 3, axis=0), "nm")
    )
    result = calculate(
        case,
        task,
        a={**A, "indices": "4"},
        b={**B, "indices": "5"},
        pbc=True,
        cutoff="10",
    )
    xyz = puw.get_value(view.molsys.structures.coordinates, to_unit="nm")[FRAMES]
    displacement = xyz[:, 4] - xyz[:, 5]
    displacement -= np.rint(displacement / [3, 4, 5]) * [3, 4, 5]
    np.testing.assert_allclose(
        [float(row[3]) for row in result["page"]["rows"]],
        np.linalg.norm(displacement, axis=1),
        atol=1e-8,
    )
    assert result["report"]["periodic"] and result["report"]["requested_pbc"]


def test_source_without_a_box_reports_native_nonperiodic_fallback(case):
    view, _, _ = case
    msm.set(view.molsys, box=None)
    result = calculate(case, pbc=True)
    assert result["report"]["requested_pbc"] and not result["report"]["periodic"]


def test_disk_backed_result_pages_convert_only_requested_values_and_clear_retires_file(
    case,
):
    view, sent, panel = case
    with (
        puw.context(standard_units=["pm", "ps"]),
        msm.configure.context(
            max_ram_usage=4096, chunk_memory_fraction=None, chunk_size=2
        ),
    ):
        result = calculate(case, indices=",".join("0" for _ in range(120)))
    assert result["report"]["disk_backed"]
    path = panel._report.native_values.path
    assert path.exists()
    page = act(view, sent, "page", report_id=result["report"]["id"], offset=50)
    assert len(page["page"]["rows"]) == 50 and page["page"]["offset"] == 50
    assert len(json.dumps(page).encode()) < 65536
    act(view, sent, "clear")
    assert not path.exists() and panel._report is None


@pytest.mark.parametrize(
    "source,value", [("current", ""), ("saved", "chosen"), ("region", "chosen")]
)
def test_scene_populations_expire_when_their_membership_changes(case, source, value):
    view, sent, panel = case
    result = calculate(case, a={**A, "source": source, "value": value})
    if source == "current":
        view.active_selection.set([1])
    elif source == "saved":
        view.selections.delete("chosen")
    else:
        view.regions.delete("chosen")
    refreshed = act(view, sent, "refresh")
    assert result["report"] and not refreshed["report"] and panel._report is None


def test_pending_primary_calculation_allows_only_current_molecular_populations(case):
    view, sent, _ = case
    view.addons.molsysmt.basic.set(
        box=puw.quantity(np.repeat(np.eye(3)[None], 3, axis=0), "nm"), update_view=False
    )
    result = calculate(case)
    assert result["context"]["state"] == "pending"
    rejected = act(view, sent, draft={"source": "current"})
    assert rejected["stage"] == "error" and "Update the scene" in rejected["message"]
    assert view.addons.molsysmt.get_sync_status()["state"] == "pending"


@pytest.mark.parametrize(
    "change",
    [
        {"task": "other"},
        {"pbc": "yes"},
        {"neighbor_mode": "count", "count": "-1"},
        {"cutoff": "nan"},
        {"cutoff": "-1"},
        {"structures": "indices", "indices": "3"},
    ],
)
def test_invalid_requests_preserve_system_and_scene(case, change):
    view, sent, _ = case
    before = snapshot(view)
    result = act(
        view, sent, draft=A, second=B, parameters={"task": "neighbors", **change}
    )
    assert result["stage"] == "error" and not result["report"]
    unchanged(view, before)


def test_foreign_page_token_and_unmount_cannot_reuse_a_report(case):
    view, sent, panel = case
    result = calculate(case)
    rejected = act(view, sent, "page", report_id="foreign", offset=0)
    assert rejected["stage"] == "error"
    panel.on_unmount(view)
    assert panel._report is None
    panel.on_mount(view)
    rejected = act(
        view,
        sent,
        "page",
        report_id=result["report"]["id"],
        offset=0,
        request_id=panel._last_request + 1,
    )
    assert rejected["stage"] == "error" and not rejected["report"]


@pytest.mark.parametrize(
    "task,pairing",
    [
        (task, pairing)
        for task in ["distances", "minimum", "maximum", "neighbors"]
        for pairing in ["cartesian", "paired"]
        if task != "neighbors" or pairing != "paired"
    ],
)
def test_row_scene_actions_keep_native_global_atom_axes_without_navigation(
    case, task, pairing
):
    view, sent, _ = case
    result = calculate(
        case, task, b={**B, "indices": "5 2 5"}, pairing=pairing, cutoff="100"
    )
    scientific = view.molsys.copy()
    for position, row in enumerate(result["page"]["rows"][:4]):
        selected = act(
            view,
            sent,
            "select_participants",
            report_id=result["report"]["id"],
            row_index=position,
        )
        assert selected["stage"] == "scene", selected["message"]
        assert set(view.active_selection.atom_indices) == set(row[1:3])
        assert selected["scene_action"]["observation_structure_index"] == row[0]
        assert view.player.index == 0
        start = len(sent)
        focused = act(
            view,
            sent,
            "focus_participants",
            report_id=result["report"]["id"],
            row_index=position,
        )
        assert focused["stage"] == "scene"
        zooms = [m for m in sent[start:] if m.get("op") == "zoom"]
        assert len(zooms) == 1 and set(zooms[0]["atom_indices"]) == set(row[1:3])
        assert view.player.index == 0
    same(view.molsys, scientific)


@pytest.mark.parametrize(
    "first_mode,second_mode",
    [
        ("atoms", "atoms"),
        ("geometric", "atoms"),
        ("atoms", "geometric"),
        ("geometric", "geometric"),
    ],
)
def test_live_distance_preserves_populations_multiplicity_current_structure_and_core_ownership(
    case, first_mode, second_mode
):
    view, sent, _ = case
    result = calculate(case, first_endpoint=first_mode, second_endpoint=second_mode)
    scientific = view.molsys.copy()
    with puw.context(standard_units=["pm", "ps"]):
        added = act(
            view,
            sent,
            "add_live_distance",
            report_id=result["report"]["id"],
            row_index=0,
        )
        assert added["stage"] == "scene", added["message"]
        tag = added["scene_action"]["measurement_tag"]
        measurement = view.measurements[tag]
        first = [4, 0, 4] if first_mode == "geometric" else [4]
        second = [5, 2] if second_mode == "geometric" else [5]
        assert measurement.info()["picks_atom_indices"] == [first, second]
        xyz = puw.get_value(view.get_coordinates(), to_unit="nm")
        expected = np.linalg.norm(
            xyz[:, first].mean(axis=1) - xyz[:, second].mean(axis=1), axis=1
        )
        np.testing.assert_allclose(
            puw.get_value(view.measurements.series(tag), to_unit="nm"), expected
        )
        assert (
            view.player.index == 0
            and added["scene_action"]["observation_structure_index"] == 2
        )
        assert float(result["page"]["rows"][0][3]) == pytest.approx(
            expected[2], abs=1e-8
        )
        assert expected[0] != pytest.approx(expected[2], abs=1e-8)
        for index in [2, 1, 0]:
            view.player.go_to_structure(index)
            coordinates = puw.get_value(measurement.get_coordinates(), to_unit="nm")
            np.testing.assert_allclose(
                coordinates,
                [xyz[index, first].mean(axis=0), xyz[index, second].mean(axis=0)],
            )
        act(view, sent, "clear")
        assert view.measurements.contains(tag)
    same(view.molsys, scientific)


@pytest.mark.parametrize("reason", ["periodic", "mass"])
def test_nonequivalent_live_distance_is_refused_but_participants_remain_usable(
    case, reason
):
    view, sent, _ = case
    if reason == "periodic":
        view.addons.molsysmt.basic.set(
            box=puw.quantity(np.repeat((np.eye(3) * 3)[None], 3, axis=0), "nm")
        )
    result = calculate(
        case,
        pbc=reason == "periodic",
        first_endpoint="mass" if reason == "mass" else "atoms",
    )
    assert reason in result["report"]["live_distance_unavailable"]
    before = snapshot(view)
    rejected = act(
        view, sent, "add_live_distance", report_id=result["report"]["id"], row_index=0
    )
    assert rejected["stage"] == "error" and reason in rejected["message"]
    unchanged(view, before)
    selected = act(
        view, sent, "select_participants", report_id=result["report"]["id"], row_index=0
    )
    assert selected["stage"] == "scene" and view.active_selection.atom_indices
    focused = act(
        view, sent, "focus_participants", report_id=result["report"]["id"], row_index=0
    )
    assert focused["stage"] == "scene"


def test_requested_periodicity_without_a_box_can_create_a_nonperiodic_live_distance(
    case,
):
    view, sent, _ = case
    msm.set(view.molsys, box=None)
    result = calculate(case, pbc=True)
    assert (
        not result["report"]["periodic"]
        and not result["report"]["live_distance_unavailable"]
    )
    added = act(
        view, sent, "add_live_distance", report_id=result["report"]["id"], row_index=0
    )
    assert added["stage"] == "scene" and view.measurements.contains(
        added["scene_action"]["measurement_tag"]
    )


@pytest.mark.parametrize("position", [None, True, -1, 0.5, "0", 18, 1000000])
def test_invalid_scene_row_never_changes_selection_history_or_molecular_data(
    case, position
):
    view, sent, _ = case
    result = calculate(case)
    before = snapshot(view)
    rejected = act(
        view,
        sent,
        "add_live_distance",
        report_id=result["report"]["id"],
        row_index=position,
    )
    assert rejected["stage"] == "error" and "row" in rejected["message"]
    unchanged(view, before)


def test_scene_row_must_belong_to_the_current_page_and_ignores_no_browser_atom_list(
    case,
):
    view, sent, _ = case
    result = calculate(
        case, a={**A, "indices": "0 1 2 3 4 5 6"}, b={**B, "indices": "7 8 9 10 11 12"}
    )
    page = act(view, sent, "page", report_id=result["report"]["id"], offset=50)
    before = snapshot(view)
    stale = act(
        view, sent, "select_participants", report_id=result["report"]["id"], row_index=0
    )
    assert stale["stage"] == "error"
    forged = act(
        view,
        sent,
        "select_participants",
        report_id=result["report"]["id"],
        row_index=50,
        atom_indices=[61],
    )
    assert forged["stage"] == "error" and "unsupported" in forged["message"]
    unchanged(view, before)
    selected = act(
        view,
        sent,
        "select_participants",
        report_id=result["report"]["id"],
        row_index=50,
    )
    assert selected["stage"] == "scene"
    assert set(view.active_selection.atom_indices) == set(page["page"]["rows"][0][1:3])


@pytest.mark.parametrize(
    "change", ["nonce", "inputs", "revision", "unmount", "endpoint"]
)
def test_expired_or_foreign_reports_cannot_create_scene_objects(case, change):
    view, sent, panel = case
    result = calculate(case)
    token = result["report"]["id"]
    endpoint = None
    if change == "nonce":
        token = "foreign"
    elif change == "inputs":
        act(view, sent, "refresh", draft={**A, "indices": "1"})
    elif change == "revision":
        view.addons.molsysmt.structure.translate(
            translation="[0.1,0,0] nm", in_place=True
        )
    elif change == "unmount":
        view._handle_frontend_event(
            {"event": "panel_unmount", "addon": "molsysmt", "panel": "analysis"}
        )
        mount(view)
    else:
        endpoint = "analysis-peer"
        view._endpoint_transfers.register(endpoint, "canvas")
        mount(view, endpoint)
    before = snapshot(view)
    rejected = act(
        view, sent, "add_live_distance", endpoint=endpoint, report_id=token, row_index=0
    )
    assert rejected["stage"] == "error" and "expired" in rejected["message"]
    unchanged(view, before)


@pytest.mark.parametrize(
    "action", ["select_participants", "focus_participants", "add_live_distance"]
)
def test_pending_scene_rejects_row_actions_while_retaining_declared_calculation_readers(
    case, action
):
    view, sent, panel = case
    view.addons.molsysmt.basic.set(
        box=puw.quantity(np.repeat(np.eye(3)[None], 3, axis=0), "nm"), update_view=False
    )
    result = calculate(case)
    assert (
        result["context"]["state"] == "pending"
        and action not in panel.read_only_actions
    )
    before = snapshot(view)
    act(view, sent, action, report_id=result["report"]["id"], row_index=0)
    unchanged(view, before)


def test_selecting_from_current_selection_expires_its_report_but_keeps_the_action_outcome(
    case,
):
    view, sent, panel = case
    result = calculate(case, a={**A, "source": "current"})
    selected = act(
        view, sent, "select_participants", report_id=result["report"]["id"], row_index=0
    )
    assert selected["stage"] == "scene" and "Selected" in selected["message"]
    assert "context changed" in selected["message"]
    assert set(view.active_selection.atom_indices) == set(
        result["page"]["rows"][0][1:3]
    )
    assert selected["report"] is None and panel._report is None


def test_replayed_request_cannot_duplicate_a_measurement_but_new_requests_have_distinct_core_tags(
    case,
):
    view, sent, _ = case
    result = calculate(case)
    added = act(
        view, sent, "add_live_distance", report_id=result["report"]["id"], row_index=0
    )
    tag = added["scene_action"]["measurement_tag"]
    view._handle_frontend_event(
        {
            "event": "addon_panel_action",
            "addon": "molsysmt",
            "panel": "analysis",
            "content": {
                "type": "action",
                "id": "add_live_distance",
                "payload": {
                    "request_id": added["request_id"],
                    "report_id": result["report"]["id"],
                    "row_index": 0,
                },
            },
        }
    )
    assert len(view.measurements.info()) == 1
    second = act(
        view, sent, "add_live_distance", report_id=result["report"]["id"], row_index=0
    )
    assert second["scene_action"]["measurement_tag"] != tag
    assert len(view.measurements.info()) == 2


@pytest.mark.parametrize(
    "action", ["select_participants", "focus_participants", "add_live_distance"]
)
def test_evaluated_empty_report_has_no_scene_row(case, action):
    view, sent, _ = case
    result = calculate(
        case, "neighbors", a={**A, "indices": "4"}, b={**B, "indices": "5"}, cutoff="0"
    )
    assert result["report"]["rows"] == 0
    before = snapshot(view)
    rejected = act(view, sent, action, report_id=result["report"]["id"], row_index=0)
    assert rejected["stage"] == "error" and "row" in rejected["message"]
    unchanged(view, before)


def test_unused_second_population_weighting_does_not_restrict_a_within_population_result(
    case,
):
    view, sent, _ = case
    result = calculate(
        case, relation="within", first_endpoint="geometric", second_endpoint="mass"
    )
    assert not result["report"]["live_distance_unavailable"]
    added = act(
        view, sent, "add_live_distance", report_id=result["report"]["id"], row_index=0
    )
    assert added["stage"] == "scene"
    measurement = view.measurements[added["scene_action"]["measurement_tag"]]
    assert measurement.info()["picks_atom_indices"] == [[4, 0, 4], [4, 0, 4]]
    np.testing.assert_allclose(
        puw.get_value(view.measurements.series(measurement.tag), to_unit="nm"),
        np.zeros(3),
    )
