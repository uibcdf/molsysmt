"""Explicit native Qt receiving; not part of the default scientific lane.

Run on the qualified WebGL-capable native display with the Viewer/provider
source routes recorded. This is automated transport/geometry evidence, not
human visual acceptance. Missing prerequisites fail when explicitly selected.
"""

import json
import subprocess
import sys
from pathlib import Path


def test_actual_qt_reviewed_geometry_and_independent_windows(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).with_name("geometry_panel_qt.py")),
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads((tmp_path / "report.json").read_text())
    assert len(report["checks"]) == 24
    assert report["qt_platform"] not in ("offscreen", "minimal")


def test_actual_qt_minimization_review_and_independent_window(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).with_name("refinement_panel_qt.py")),
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads((tmp_path / "report.json").read_text())
    assert len(report["checks"]) == 6
    assert report["qt_platform"] not in ("offscreen", "minimal")


def test_actual_qt_chemical_repairs_assignments_and_result_window(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).with_name("chemistry_panel_qt.py")),
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads((tmp_path / "report.json").read_text())
    assert len(report["checks"]) == 6
    assert report["qt_platform"] not in ("offscreen", "minimal")


def test_actual_qt_properties_reports_and_participants(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).with_name("property_report_qt.py")),
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads((tmp_path / "report.json").read_text())
    assert len(report["checks"]) == 6
    assert report["qt_platform"] not in ("offscreen", "minimal")


def test_actual_qt_scalar_colors_and_selected_structure_plot(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).with_name("visual_adoption_qt.py")),
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads((tmp_path / "report.json").read_text())
    assert len(report["checks"]) == 4
    assert report["qt_platform"] not in ("offscreen", "minimal")


def test_actual_qt_interaction_mechanics_and_separate_adoption(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).with_name("interaction_mechanics_qt.py")),
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
        timeout=240,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads((tmp_path / "report.json").read_text())
    assert len(report["checks"]) == 4
    assert report["qt_platform"] not in ("offscreen", "minimal")
