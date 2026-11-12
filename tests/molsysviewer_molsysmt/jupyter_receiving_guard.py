"""Explicit local GUI guard, separate from the default scientific test lane.

Select this node with pytest in the qualified GUI environment. Set
MOLSYSVIEWER_ROOT and, for the recorded overlay, MOLSYSVIEWER_PROVIDER_ROOT.
Missing browser/Jupyter prerequisites fail; they are not silently skipped.
"""

import json
import math
import os
import subprocess
import sys
from pathlib import Path

import pytest


def test_chromium_memory_sampling_retained_and_released_controls(tmp_path):
    """Distinguish retained witnesses from retired objects and backing buffers."""
    output = tmp_path / "memory-sampling.json"
    subprocess.run(
        [
            "node",
            str(Path(__file__).with_name("memory_sampling_guard.mjs")),
            str(output),
        ],
        check=True,
        timeout=90,
    )
    result = json.loads(output.read_text())
    assert result["outcome"] == "passed"
    assert result["witness_value"] == 37
    assert result["released_backing_bytes"] >= 7 * 1024 * 1024
    for name in ["before_release", "after_release"]:
        sample = result[name]
        assert sample["cdp_collections"] == 2
        assert sample["after_collection"]["subjects"]["witness"] == {
            "object_alive": True,
            "buffer_alive": True,
        }
    assert result["before_release"]["after_collection"]["subjects"]["retained"][
        "object_alive"
    ]
    assert not result["after_release"]["after_collection"]["subjects"]["retained"][
        "object_alive"
    ]


def test_actual_plain_jupyter_memory_baseline(tmp_path):
    """Measure default Jupyter execution without molecular kernel imports."""
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / "jupyter-host-memory"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--scenario",
        "host-memory",
        "--host-groups",
        "3",
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=300)
    result = json.loads((output / "full-result.json").read_text())
    assert result["outcome"] == "passed" and result["groups"] == 3
    assert [sample["executions"] for sample in result["samples"]] == [0, 3, 6, 9]
    assert result["kernel"]["initial_forbidden_imports"] == []
    assert result["kernel"]["final_forbidden_imports"] == []
    assert result["settings_changed"] is False
    assert result["host_page_config"] == result["host_page_config_after"]
    assert result["cell_toolbar_settings"] == result["cell_toolbar_settings_after"]
    assert result["host_page_config"]["appVersion"]
    assert result["cell_toolbar_settings"]["available"] is True
    before = json.loads((output / "host-application-before.json").read_text())
    after = json.loads((output / "host-application-after.json").read_text())
    assert before["available"] is True and before == after
    assert (
        "application_package" in before["files"] or "static_package" in before["files"]
    )
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_molecular_import_snapshot_uses_actual_imported_files(tmp_path):
    """Keep inner-provider identity independent of the outer caller's label."""
    import hashlib

    from tests.molsysviewer_molsysmt import system_panel_jupyter as launcher

    path = tmp_path / "actual-imports.json"
    observed = launcher._record_molecular_imports(path)
    assert json.loads(path.read_text()) == observed
    for name, row in observed["modules"].items():
        if not row["loaded"]:
            assert name not in sys.modules
            continue
        module = sys.modules[name]
        origin = Path(vars(module)["__file__"]).resolve()
        assert Path(row["origin"]) == origin
        assert row["sha256"] == hashlib.sha256(origin.read_bytes()).hexdigest()
        assert row["module_version"] == vars(module).get("__version__")


def test_actual_jupyter_prolonged_popup_controls(tmp_path):
    """Activate Next from fully hidden controls before receiving a real cycle."""
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / "jupyter-prolonged-controls"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--scenario",
        "prolonged-session",
        "--cycles",
        "1",
        "--active-seconds",
        "10",
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=360)
    result = json.loads((output / "full-result.json").read_text())
    assert result["cycles"] == len(result["records"]) == len(result["native"]) == 1
    assert result["records"][0]["controls"] == {
        "started_hidden": True,
        "next_focused": True,
    }
    assert result["records"][0]["activity"]["distinct_frames"] >= 2
    assert result["active_seconds_per_cycle"] == 10
    imports = json.loads((output / "kernel-molecular-imports.json").read_text())
    source = Path(__file__).resolve().parents[2]
    assert (
        Path(imports["modules"]["molsysmt"]["origin"])
        == source / "molsysmt/__init__.py"
    )
    assert (
        Path(imports["modules"]["molsysviewer"]["origin"])
        == viewer / "molsysviewer/__init__.py"
    )
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_actual_jupyter_initial_canvas_diagnostics(tmp_path):
    """Receive opt-in diagnostics separately from the original Analysis verdict."""
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / "jupyter-initial-canvas"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--scenario",
        "analysis",
        "--initial-canvas-only",
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=360)
    result = json.loads((output / "full-result.json").read_text())
    assert result["checks"] == [
        "Load TcTIM and open Analysis without calculating implicitly"
    ]
    capture = json.loads((output / "initial-canvas.json").read_text())
    assert capture["outcome"] == "canvas_visible" and capture["capture"] == "available"
    trace = capture["trace"]
    assert trace["belongs_to_initial_cell"] is True
    assert trace["observed_atoms"] == trace["expected_atoms"] == 3983
    assert trace["canvas"]["connected"] and trace["observer_errors"] == 0
    assert trace["run_clicked_epoch_ms"] is not None
    assert trace["anchor"] == "observer_arm_before_run_click"
    if "first_native_draw" in trace["marks"]:
        assert (
            trace["marks"]["first_native_draw"] >= trace["marks"]["draw_observer_armed"]
        )
    kernel = [
        json.loads(line)
        for line in (output / "initial-canvas-kernel.jsonl").read_text().splitlines()
    ]
    assert [row["stage"] for row in kernel] == [
        "cell_started",
        "viewer_import_started",
        "viewer_imported",
        "molsysmt_import_started",
        "molsysmt_imported",
        "demo_load_started",
        "demo_loaded",
        "display_expression",
        "cell_completed",
    ]
    assert all(row["attempt"] == trace["attempt"] for row in kernel)
    assert all(
        math.isfinite(row["elapsed_ms"]) and row["elapsed_ms"] >= 0 for row in kernel
    )
    sessions = json.loads((output / "initial-canvas-sessions.json").read_text())
    assert sessions["attempt"] == trace["attempt"]
    assert sessions["anchor"] == "sampler_arm_before_run_click"
    assert sessions["outcome"] == "canvas_visible"
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_actual_jupyter_analysis_distance_family(tmp_path):
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / "jupyter-analysis"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--scenario",
        "analysis",
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=360)
    result = json.loads((output / "full-result.json").read_text())
    assert result["checks"] == [
        "Load TcTIM and open Analysis without calculating implicitly",
        "Calculate explicit atom populations and verify native distances against coordinates",
        "Inspect native minimum and maximum without changing molecular data",
        "Inspect evaluated-empty neighbors and explicit nearest-count results",
        "Page through TcTIM source indices without transferring the complete result",
        "Use independent Analysis panels in canvas popup and detached Studio",
        "Python verifies every molecular coordinate chemical domain and scene object unchanged",
        "Select participants and focus the visible structure without losing the row acknowledgement",
        "Mass-weighted observations retain participant actions and explain the disabled live conversion",
        "Create a centroid Measure from TcTIM and preserve its actual geometry after Clear",
        "Create core Measures through canvas and detached Studio popups with mirrored geometry",
        "A repeated-population live Measure uses the visible structure and follows a real ensemble",
        "Prepare independent conformation references from the unchanged real ensemble",
        "Inspect RMSD optimal RMSD gyration and atom-indexed RMSF with explicit source axes",
        "Add a correctly indexed core plot retain it after Clear and navigate by its actual point",
        "Inspect and adopt conformational results through both real popup boundaries",
        "Inspect directed vector components and repeated source structures against coordinates",
        "Inspect ordered atom-triplet angles with explicit angular display units",
        "Inspect signed quartet torsions and deliberate participant actions without navigating",
        "Inspect weighted PCA eigenvalues and source-indexed coefficients without a trajectory projection",
        "Inspect PCA through both popups and deliberately select coefficient participants without moving coordinates",
        "Python verifies retained native data separate plots and deliberate structure navigation",
    ]
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_actual_jupyter_chemistry_preparation_and_reviewed_replacement(tmp_path):
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / "jupyter-preparation"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--scenario",
        "chemistry-preparation",
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=300)
    result = json.loads((output / "full-result.json").read_text())
    assert len(result["checks"]) == 6
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_actual_jupyter_review_and_independent_popups(tmp_path):
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / "jupyter"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=300)
    result = json.loads((output / "full-result.json").read_text())
    assert len(result["checks"]) == 6
    assert result["final_atoms"] == 3817
    assert result["managed_edits"] == 2
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_actual_jupyter_independent_result_views(tmp_path):
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / "jupyter-results"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--scenario",
        "results",
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=300)
    result = json.loads((output / "full-result.json").read_text())
    assert len(result["checks"]) == 7
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_actual_jupyter_geometry_translation(tmp_path):
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / "jupyter-geometry"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--scenario",
        "geometry",
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=300)
    result = json.loads((output / "full-result.json").read_text())
    assert len(result["checks"]) == 7
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_actual_jupyter_geometry_centering(tmp_path):
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / "jupyter-center"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--scenario",
        "center",
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=300)
    result = json.loads((output / "full-result.json").read_text())
    assert len(result["checks"]) == 7
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_actual_jupyter_geometry_rotation(tmp_path):
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / "jupyter-rotate"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--scenario",
        "rotate",
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=300)
    result = json.loads((output / "full-result.json").read_text())
    assert len(result["checks"]) == 7
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_actual_jupyter_geometry_principal_axes(tmp_path):
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / "jupyter-axes"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--scenario",
        "axes",
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=300)
    result = json.loads((output / "full-result.json").read_text())
    assert len(result["checks"]) == 8
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_actual_jupyter_rejected_operation_diagnostic(tmp_path):
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / "jupyter-center-errors"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--scenario",
        "center-errors",
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=300)
    result = json.loads((output / "full-result.json").read_text())
    assert len(result["checks"]) == 5
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_actual_jupyter_geometry_superposition(tmp_path):
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / "jupyter-fit"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--scenario",
        "fit",
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=300)
    result = json.loads((output / "full-result.json").read_text())
    assert len(result["checks"]) == 8
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_actual_jupyter_geometry_external_reference(tmp_path):
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / "jupyter-fit-external"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--scenario",
        "fit-external",
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=300)
    result = json.loads((output / "full-result.json").read_text())
    assert len(result["checks"]) == 8
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_actual_jupyter_periodic_geometry(tmp_path):
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / "jupyter-periodic"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--scenario",
        "periodic",
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=300)
    result = json.loads((output / "full-result.json").read_text())
    assert len(result["checks"]) == 8
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_actual_jupyter_periodic_cell_assignment(tmp_path):
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / "jupyter-cell"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--scenario",
        "cell",
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=300)
    result = json.loads((output / "full-result.json").read_text())
    assert len(result["checks"]) == 8
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_actual_jupyter_general_periodic_geometry(tmp_path):
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / "jupyter-periodic-general"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--scenario",
        "periodic-general",
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=300)
    result = json.loads((output / "full-result.json").read_text())
    expected = json.loads((output / "periodic-expected.json").read_text())
    assert len(result["checks"]) == 8
    assert "changing general-row cells" in result["scope"]
    assert expected["general_cells"] is True
    assert expected["transition_control_difference_nm"] > 0.1
    boxes = expected["boxes_nm"]
    assert any(box != boxes[0] for box in boxes[1:])
    assert any(
        box[i][j] != 0 for box in boxes for i in range(3) for j in range(i + 1, 3)
    )
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


@pytest.mark.parametrize("standard", ["nm", "pm"])
def test_actual_jupyter_small_periodic_origins(tmp_path, standard):
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / f"jupyter-origins-{standard}"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--scenario",
        "periodic-origins",
        "--length-standard",
        standard,
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=300)
    result = json.loads((output / "full-result.json").read_text())
    expected = json.loads((output / "origins-expected.json").read_text())
    assert len(result["checks"]) == 7
    assert expected["standard"] == standard
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_actual_jupyter_chemistry_inspection(tmp_path):
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / "jupyter-chemistry"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--scenario",
        "chemistry",
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=300)
    result = json.loads((output / "full-result.json").read_text())
    assert len(result["checks"]) == 10
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_actual_jupyter_pending_chemistry_readers(tmp_path):
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / "jupyter-chemistry-pending"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--scenario",
        "chemistry-pending",
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=300)
    result = json.loads((output / "full-result.json").read_text())
    assert len(result["checks"]) == 8
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


@pytest.mark.parametrize("length_standard", ["nm", "pm"])
def test_actual_jupyter_geometry_sequence_alignment(tmp_path, length_standard):
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / "jupyter-sequence"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--scenario",
        "sequence",
        "--length-standard",
        length_standard,
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=300)
    result = json.loads((output / "full-result.json").read_text())
    assert len(result["checks"]) == 8
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_actual_jupyter_refinement_review_and_both_popup_boundaries(tmp_path):
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / "jupyter-refinement"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--scenario",
        "refinement",
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=300)
    result = json.loads((output / "full-result.json").read_text())
    assert len(result["checks"]) == 4
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_actual_jupyter_chemistry_repairs_and_assignments(tmp_path):
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / "jupyter-chemistry-repair"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--scenario",
        "chemistry-repair",
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=300)
    result = json.loads((output / "full-result.json").read_text())
    assert len(result["checks"]) == 6
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_actual_jupyter_property_reports_and_both_popups(tmp_path):
    output = tmp_path / "jupyter-properties"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        os.environ["MOLSYSVIEWER_ROOT"],
        "--scenario",
        "properties",
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=300)
    result = json.loads((output / "full-result.json").read_text())
    assert len(result["checks"]) == 7
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_actual_jupyter_visual_adoption_and_both_popups(tmp_path):
    output = tmp_path / "jupyter-visual-adoption"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        os.environ["MOLSYSVIEWER_ROOT"],
        "--scenario",
        "visual-adoption",
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=300)
    result = json.loads((output / "full-result.json").read_text())
    assert len(result["checks"]) == 6
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_actual_jupyter_interaction_mechanics_and_both_popups(tmp_path):
    output = tmp_path / "jupyter-interaction-mechanics"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        os.environ["MOLSYSVIEWER_ROOT"],
        "--scenario",
        "interaction-mechanics",
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=420)
    result = json.loads((output / "full-result.json").read_text())
    assert len(result["checks"]) == 7
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_actual_continuous_scientific_session_and_recovery(tmp_path):
    """One retained session combines molecular values, GUI actions and recovery."""
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / "continuous-session"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--scenario",
        "continuous-session",
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=420)
    result = json.loads((output / "full-result.json").read_text())
    assert len(result["checks"]) == 7
    ledger = json.loads((output / "scientific-ledger.json").read_text())
    assert [r["phase"] for r in ledger] == [
        "composed",
        "removed_and_copied",
        "prepared_independent",
        "transformed_and_fitted",
        "ensemble_observed",
        "native_empty_original_conformations",
        "interactions",
        "closed_and_recovered",
        "continued_after_recovery",
    ]
    assert ledger[-1]["preserved_evaluated"] == [0]
    assert ledger[-1]["source_ids_retained"] is True
    assert ledger[0]["atoms"] - ledger[1]["removed"] == ledger[1]["retained"]
    assert next(r for r in ledger if r["phase"] == "interactions")["occurrences"] > 0
    for name in ("composed", "ensemble"):
        assert (output / (name + ".msv")).is_file()
        assert (output / (name + ".h5msm")).is_file()
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_actual_jupyter_assessed_protonation_managed_and_independent(tmp_path):
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / "jupyter-assessed-protonation"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--scenario",
        "assessed-protonation",
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=300)
    result = json.loads((output / "full-result.json").read_text())
    assert len(result["checks"]) == 6
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()


def test_actual_jupyter_independent_construction_and_popups(tmp_path):
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / "jupyter-construction"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--scenario",
        "construction",
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=360)
    result = json.loads((output / "full-result.json").read_text())
    assert len(result["checks"]) == 6
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()
