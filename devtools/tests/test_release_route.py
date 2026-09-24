"""Guards for the committed Conda route and exact-file promotion."""

from __future__ import annotations

import importlib.util
import io
import subprocess
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
ROUTE_FILE = ROOT / "devtools" / "conda-build" / "release_route.py"
PROMOTION = ROOT / ".github" / "workflows" / "promote_conda_package.yaml"

spec = importlib.util.spec_from_file_location("conda_release_route", ROUTE_FILE)
assert spec is not None and spec.loader is not None
route = importlib.util.module_from_spec(spec)
spec.loader.exec_module(route)


def test_staged_plan_is_bound_to_the_new_version():
    plan = route.read_plan()
    assert plan["version"] == "0.22.4"
    assert plan["route"] == "staged"
    assert plan["reason"].strip()
    assert route.select_route("0.22.4", "workflow_dispatch") == "staged"
    assert route.select_route("0.22.4", "release") == "staged"
    with pytest.raises(ValueError, match="release plan is for"):
        route.select_route("9.9.9", "release")


def test_dispatch_command_emits_the_selected_route(tmp_path):
    output = tmp_path / "route-output"
    subprocess.run(
        [sys.executable, str(ROUTE_FILE), "--version", "0.22.4", "--event", "workflow_dispatch",
         "--github-output", str(output)],
        check=True,
        capture_output=True,
        text=True,
    )
    assert output.read_text() == "route=staged\n"


def test_direct_route_fails_closed_if_any_label_contains_the_version(tmp_path, monkeypatch):
    plan = tmp_path / "release_plan.toml"
    plan.write_text('version = "9.9.9"\nroute = "direct"\nreason = "Independent patch"\n')
    with pytest.raises(ValueError, match="requires a staged plan"):
        route.select_route("9.9.9", "workflow_dispatch", plan)

    def occupied(_version):
        raise ValueError("coordinate occupied")

    monkeypatch.setattr(route, "assert_version_unoccupied", occupied)
    with pytest.raises(ValueError, match="coordinate occupied"):
        route.select_route("9.9.9", "release", plan)


def test_registry_query_accepts_only_explicit_404(monkeypatch):
    def missing(_request, timeout):
        assert timeout == 20
        raise HTTPError("https://api.anaconda.org/", 404, "missing", {}, None)

    monkeypatch.setattr(route, "urlopen", missing)
    route.assert_version_unoccupied("9.9.9")

    def network_failure(_request, timeout):
        raise URLError("offline")

    monkeypatch.setattr(route, "urlopen", network_failure)
    with pytest.raises(URLError):
        route.assert_version_unoccupied("9.9.9")

    class Existing:
        def __enter__(self):
            return io.BytesIO(b'{"distributions": []}')

        def __exit__(self, *_args):
            return False

    monkeypatch.setattr(route, "urlopen", lambda _request, timeout: Existing())
    with pytest.raises(ValueError, match="already exists"):
        route.assert_version_unoccupied("9.9.9")


def test_promotion_requires_exact_release_and_installed_pair_evidence():
    workflow = yaml.safe_load(PROMOTION.read_text(encoding="utf-8"))
    inputs = workflow[True]["workflow_dispatch"]["inputs"]
    for name in (
        "candidate_sha", "version", "target", "filename", "build_number", "sha256",
        "pair_run_id", "molsysviewer_version", "molsysviewer_build_number",
    ):
        assert inputs[name]["required"] is True
    job = workflow["jobs"]["promote"]
    steps = job["steps"]
    identity = next(step for step in steps if step.get("name") == "Validate release identity and installed-pair gate")
    promotion = next(step for step in steps if step.get("id") == "promotion")
    receipt = next(step for step in steps if step.get("name") == "Retain the bounded promotion receipt")
    assert "git rev-list -n 1" in identity["run"]
    assert "release_route.py" in identity["run"]
    assert "validate_conda_staging.yaml" in identity["run"]
    assert "--jq .total_count" in identity["run"]
    assert "--jq .display_title" in identity["run"]
    assert promotion["uses"] == "uibcdf/action-build-and-upload-conda-packages/promote@v2.2.2"
    assert promotion["with"]["from-label"] == "staging"
    assert promotion["with"]["to-label"] == "main"
    assert promotion["with"]["expected-sha256"] == "${{ inputs.sha256 }}"
    assert receipt["with"]["path"] == "${{ steps.promotion.outputs.receipt }}"
    for step in steps:
        if "run" in step:
            syntax = subprocess.run(["bash", "-n"], input=step["run"], text=True, capture_output=True)
            assert syntax.returncode == 0, f"{step['name']}: {syntax.stderr}"
