"""Explicit local GUI guard, separate from the default scientific test lane.

Select this node with pytest in the qualified GUI environment. Set
MOLSYSVIEWER_ROOT and, for the recorded overlay, MOLSYSVIEWER_PROVIDER_ROOT.
Missing browser/Jupyter prerequisites fail; they are not silently skipped.
"""

import json
import os
import subprocess
import sys
from pathlib import Path


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
    subprocess.run(command, check=True, timeout=300)
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
    assert len(result["checks"]) == 7
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
