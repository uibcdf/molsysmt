"""Reject synthetic incomplete draw evidence through the actual opt-in guard."""

import json
import os
import shutil
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest

from tests.molsysviewer_molsysmt import jupyter_receiving_guard as guard


def receive(tmp_path, monkeypatch, change=None):
    capture = {
        "outcome": "canvas_visible",
        "capture": "available",
        "trace": {
            "attempt": "synthetic-acceptance-control",
            "belongs_to_initial_cell": True,
            "observed_atoms": 3983,
            "expected_atoms": 3983,
            "canvas": {"connected": True, "width": 640, "height": 480},
            "observer_errors": 0,
            "anchor": "observer_arm_before_run_click",
            "run_clicked_epoch_ms": 1001,
            "elapsed_ms": 32000,
            "marks": {
                "run_clicked": 1,
                "controller_ready": 100,
                "draw_observer_armed": 101,
                "scene_registered": 200,
                "first_native_draw": 220,
            },
        },
    }
    if change == "missing_draw":
        del capture["trace"]["marks"]["first_native_draw"]
    elif change == "cached_draw":
        capture["trace"]["marks"]["first_native_draw"] = 99
    elif change == "draw_before_scene":
        capture["trace"]["marks"]["scene_registered"] = 221
    elif change == "late_draw":
        capture["trace"]["marks"]["first_native_draw"] = 31001
    original = deepcopy(capture)

    def deliver(command, **kwargs):
        assert "--initial-canvas-only" in command
        assert kwargs == {"check": True, "timeout": 360}
        output = tmp_path / "jupyter-initial-canvas"
        output.mkdir()
        (output / "initial-canvas.json").write_text(json.dumps(capture))
        (output / "full-result.json").write_text(
            json.dumps(
                {
                    "checks": [
                        "Load TcTIM and open Analysis without calculating implicitly"
                    ]
                }
            )
        )
        stages = [
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
        rows = [
            {
                "stage": stage,
                "attempt": capture["trace"]["attempt"],
                "elapsed_ms": index,
            }
            for index, stage in enumerate(stages)
        ]
        (output / "initial-canvas-kernel.jsonl").write_text(
            "\n".join(json.dumps(row) for row in rows) + "\n"
        )
        (output / "initial-canvas-sessions.json").write_text(
            json.dumps(
                {
                    "attempt": capture["trace"]["attempt"],
                    "anchor": "sampler_arm_before_run_click",
                    "outcome": "canvas_visible",
                }
            )
        )

    monkeypatch.setenv("MOLSYSVIEWER_ROOT", str(tmp_path))
    monkeypatch.setattr(guard.subprocess, "run", deliver)
    guard.test_actual_jupyter_initial_canvas_diagnostics(tmp_path)
    assert capture == original


def test_actual_guard_accepts_complete_correlated_synthetic_evidence(
    tmp_path, monkeypatch
):
    receive(tmp_path, monkeypatch)


@pytest.mark.parametrize(
    "change", ["missing_draw", "cached_draw", "draw_before_scene", "late_draw"]
)
def test_actual_guard_refuses_missing_stale_or_late_draw(tmp_path, monkeypatch, change):
    with pytest.raises(AssertionError):
        receive(tmp_path, monkeypatch, change)


def test_observer_ignores_cached_and_wrong_scene_draws():
    node = shutil.which("node")
    if node is None:
        pytest.skip("Node.js is required for the receiving-observer controls")
    script = Path(__file__).with_name("initial_canvas_trace.test.mjs")
    result = subprocess.run(
        [node, "--test", str(script)],
        env={**os.environ, "INITIAL_CANVAS_TEST_PYTHON": sys.executable},
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
