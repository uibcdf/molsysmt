"""Validate the exact-byte boundary between installed tests and promotion."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from devtools.scripts import validate_conda_staging
from devtools.scripts import verify_conda_pair_receipts as pair

_STAGING = "https://conda.anaconda.org/uibcdf/label/staging"
_PLATFORMS = ("linux-64", "linux-aarch64", "osx-arm64", "win-64")
_PYTHONS = ("3.11", "3.12", "3.13", "3.14")
_SPECS = dict(
    molsysmt_version="1.0.0",
    molsysmt_build=1,
    viewer_version="1.0.0",
    viewer_build=2,
)
_ROOT = Path(__file__).resolve().parents[2]


def _record(subdir, filename, digest):
    return dict(
        channel=_STAGING,
        url=f"{_STAGING}/{subdir}/{filename}",
        fn=filename,
        sha256=digest,
    )


@pytest.fixture
def installed_pair(tmp_path, request):
    root = tmp_path / "installed-pair"
    viewer_suffix = getattr(request, "param", "tar.bz2")
    matrix = dict(
        schema="molsyssuite.installed-matrix@1",
        state="verified",
        candidate_sha="a" * 40,
        run_id=50000,
        run_attempt=2,
        jobs=[
            dict(kind="installed", platform=subdir, python=python)
            for subdir in _PLATFORMS
            for python in _PYTHONS
        ],
    )
    for job in matrix["jobs"]:
        subdir = job["platform"]
        index = _PLATFORMS.index(subdir)
        python = job["python"]
        receipt = {
            "schema": "molsysmt.installed-conda-pair@1",
            "candidate_sha": matrix["candidate_sha"],
            "run_id": matrix["run_id"],
            "run_attempt": matrix["run_attempt"],
            "python": python,
            "packages": {
                "molsysmt": _record(
                    subdir,
                    f"molsysmt-1.0.0-pyabi3h123456{index}_1.conda",
                    str(index) * 64,
                ),
                "molsysviewer": _record(
                    "noarch", f"molsysviewer-1.0.0-py_2.{viewer_suffix}", "f" * 64
                ),
            },
        }
        path = (
            root
            / f"conda-staging-{subdir}-py{python}-attempt-2"
            / "installed-pair.json"
        )
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(receipt), encoding="utf-8")
    return matrix, root


@pytest.mark.parametrize("installed_pair", ["tar.bz2", "conda"], indirect=True)
def test_complete_matrix_qualifies_only_its_tested_digests(installed_pair):
    files = pair.verify_installations(*installed_pair, **_SPECS)
    assert set(files["molsysmt"]) == set(_PLATFORMS)
    assert files["molsysviewer"]["sha256"] == "f" * 64
    target = "osx-arm64"
    filename = "molsysmt-1.0.0-pyabi3h1234562_1.conda"
    pair.require_tested_artifact(files, target, filename, "2" * 64)
    with pytest.raises(ValueError, match="filename and digest were not tested"):
        pair.require_tested_artifact(files, target, filename, "e" * 64)
    with pytest.raises(ValueError, match="filename and digest were not tested"):
        pair.require_tested_artifact(
            files, target, "molsysmt-1.0.0-pyabi3h7654321_1.conda", "2" * 64
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("run_attempt", 1),
        ("run_id", 49999),
        ("candidate_sha", "1" * 40),
        ("python", "3.12"),
    ],
)
def test_cross_run_or_cross_cell_receipt_is_rejected(installed_pair, field, value):
    matrix, root = installed_pair
    path = root / "conda-staging-linux-64-py3.14-attempt-2" / "installed-pair.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data[field] = value
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="Wrong source, run, attempt or Python"):
        pair.verify_installations(matrix, root, **_SPECS)


@pytest.mark.parametrize("package", ["molsysmt", "molsysviewer"])
def test_same_version_and_filename_with_different_digest_fails(installed_pair, package):
    matrix, root = installed_pair
    path = root / "conda-staging-linux-64-py3.14-attempt-2" / "installed-pair.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["packages"][package]["sha256"] = "e" * 64
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="artifact identity differs"):
        pair.verify_installations(matrix, root, **_SPECS)


@pytest.mark.parametrize(
    ("suffix", "message"),
    [
        ("conda", "Installed MolSysViewer artifact identity differs"),
        ("zip", "Unexpected molsysviewer staging artifact"),
    ],
)
def test_viewer_archive_format_is_part_of_its_identity(installed_pair, suffix, message):
    matrix, root = installed_pair
    path = root / "conda-staging-linux-64-py3.14-attempt-2" / "installed-pair.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["packages"]["molsysviewer"] = _record(
        "noarch", f"molsysviewer-1.0.0-py_2.{suffix}", "f" * 64
    )
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match=message):
        pair.verify_installations(matrix, root, **_SPECS)


def test_missing_cell_is_rejected(installed_pair):
    matrix, root = installed_pair
    (root / "conda-staging-osx-arm64-py3.11-attempt-2" / "installed-pair.json").unlink()
    with pytest.raises(ValueError, match="exact cells"):
        pair.verify_installations(matrix, root, **_SPECS)


def test_wrong_staged_build_is_rejected_even_with_consistent_records(installed_pair):
    with pytest.raises(ValueError, match="Unexpected molsysmt staging artifact"):
        pair.verify_installations(*installed_pair, **{**_SPECS, "molsysmt_build": 9})


def test_receipt_writer_keeps_observed_package_bytes_and_run_identity(
    monkeypatch, tmp_path
):
    for key, value in {
        "GITHUB_SHA": "b" * 40,
        "GITHUB_RUN_ID": "713",
        "GITHUB_RUN_ATTEMPT": "3",
    }.items():
        monkeypatch.setenv(key, value)
    package = _record("linux-64", "molsysmt-1.0.0-pyabi3h1234567_1.conda", "b" * 64)
    output = tmp_path / "installed-pair.json"
    validate_conda_staging._write_pair_receipt(
        output, {"molsysmt": {**package, "path": "local"}}
    )
    record = json.loads(output.read_text(encoding="utf-8"))
    assert record["candidate_sha"] == "b" * 40
    assert record["run_id"] == 713
    assert record["run_attempt"] == 3
    assert record["python"] == f"{sys.version_info.major}.{sys.version_info.minor}"
    assert record["packages"]["molsysmt"] == package


@pytest.mark.skipif(sys.platform == "win32", reason="Promotion executes Bash on Ubuntu")
@pytest.mark.parametrize("matching", [True, False])
def test_actual_promotion_gate_checks_the_requested_digest(installed_pair, matching):
    matrix, directory = installed_pair
    workflow_file = _ROOT / ".github/workflows/promote_conda_package.yaml"
    workflow = yaml.safe_load(workflow_file.read_text(encoding="utf-8"))
    step = next(
        step
        for step in workflow["jobs"]["promote"]["steps"]
        if step.get("name") == "Bind promotion to the tested package digests"
    )
    matrix_path = directory.parent / "matrix.json"
    matrix_path.write_text(json.dumps(matrix), encoding="utf-8")
    env = {
        **os.environ,
        "MATRIX_RECEIPT": str(matrix_path),
        "RUNNER_TEMP": str(directory.parent),
        "RELEASE_VERSION": "1.0.0",
        "BUILD_NUMBER": "1",
        "TARGET": "linux-64",
        "FILENAME": "molsysmt-1.0.0-pyabi3h1234560_1.conda",
        "EXPECTED_SHA256": ("0" if matching else "e") * 64,
        "VIEWER_VERSION": "1.0.0",
        "VIEWER_BUILD": "2",
    }
    result = subprocess.run(
        ["bash", "-eo", "pipefail", "-c", step["run"]],
        cwd=_ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=10,
    )
    receipt = directory.parent / "molsysmt-tested-conda-pair.json"
    if matching:
        assert result.returncode == 0, result.stderr
        files = json.loads(receipt.read_text(encoding="utf-8"))
        assert files["molsysmt"]["linux-64"]["sha256"] == "0" * 64
        assert files["molsysviewer"]["fn"] == "molsysviewer-1.0.0-py_2.tar.bz2"
    else:
        assert result.returncode == 1, result.stderr
        assert "filename and digest were not tested" in result.stderr
        assert not receipt.exists()
