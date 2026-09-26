"""Guards for exact-file public Conda verification without registry writes."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "devtools" / "conda-build" / "verify_public_package.py"
PROMOTION = ROOT / ".github" / "workflows" / "promote_conda_package.yaml"
READ_ONLY = ROOT / ".github" / "workflows" / "verify_public_conda_package.yaml"
PACKAGE = "molsysmt"
VERSION = "0.22.4"
SUBDIR = "linux-64"
FILENAME = "molsysmt-0.22.4-pyabi3h03bb3b7_3.conda"
SHA256 = "e2ac3c779f17b2ca2aa7655fc6a2a349de558de229f479525826b5deaa6f8d3e"

spec = importlib.util.spec_from_file_location("conda_public_verifier", SCRIPT)
assert spec is not None and spec.loader is not None
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


def _records(*, labels=("staging", "main"), release_sha=SHA256, index_sha=SHA256):
    release = {
        "distributions": [
            {
                "basename": f"{SUBDIR}/{FILENAME}",
                "sha256": release_sha,
                "labels": list(labels),
                "attrs": {"subdir": SUBDIR},
            }
        ]
    }
    index = {
        "info": {"subdir": SUBDIR},
        "packages.conda": {
            FILENAME: {
                "name": PACKAGE,
                "version": VERSION,
                "sha256": index_sha,
            }
        },
    }
    return release, index


def test_exact_public_record_requires_label_and_solver_index():
    release, index = _records()
    assert (
        verifier.verify_snapshot(
            release, index, PACKAGE, VERSION, SUBDIR, FILENAME, SHA256
        )
        == f"https://conda.anaconda.org/uibcdf/{SUBDIR}/{FILENAME}"
    )

    release["distributions"][0]["labels"] = ["staging"]
    with pytest.raises(verifier.VerificationPending, match="main label"):
        verifier.verify_snapshot(
            release, index, PACKAGE, VERSION, SUBDIR, FILENAME, SHA256
        )
    release["distributions"][0]["labels"].append("main")
    del index["packages.conda"][FILENAME]
    with pytest.raises(verifier.VerificationPending, match="solver-visible"):
        verifier.verify_snapshot(
            release, index, PACKAGE, VERSION, SUBDIR, FILENAME, SHA256
        )


@pytest.mark.parametrize("changed", ["release", "index"])
def test_digest_mismatch_is_a_hard_failure(changed):
    kwargs = {f"{changed}_sha": "0" * 64}
    release, index = _records(**kwargs)
    with pytest.raises(verifier.VerificationError, match="SHA-256 differs"):
        verifier.verify_snapshot(
            release, index, PACKAGE, VERSION, SUBDIR, FILENAME, SHA256
        )


def test_rejects_ambiguous_or_unsafe_coordinates():
    release, index = _records()
    release["distributions"].append(release["distributions"][0].copy())
    with pytest.raises(verifier.VerificationError, match="duplicate"):
        verifier.verify_snapshot(
            release, index, PACKAGE, VERSION, SUBDIR, FILENAME, SHA256
        )
    with pytest.raises(verifier.VerificationError, match="single Conda coordinate"):
        verifier.validate_coordinate(PACKAGE, VERSION, SUBDIR, "../wrong.conda", SHA256)


def test_bounded_retry_then_success(monkeypatch):
    release, index = _records()
    release["distributions"][0]["labels"] = ["staging"]
    ready, ready_index = _records()
    documents = iter((release, index, ready, ready_index))
    urls = []
    sleeps = []

    def fetch(url):
        urls.append(url)
        return next(documents)

    monkeypatch.setattr(verifier, "fetch_json", fetch)
    monkeypatch.setattr(verifier.time, "sleep", sleeps.append)
    assert verifier.verify_public(
        PACKAGE, VERSION, SUBDIR, FILENAME, SHA256, attempts=2, interval=0.5
    ).endswith(FILENAME)
    assert len(urls) == 4
    assert sleeps == [0.5]


def test_workflows_share_a_read_only_verifier():
    promotion = yaml.safe_load(PROMOTION.read_text(encoding="utf-8"))
    verify_step = promotion["jobs"]["promote"]["steps"][-1]
    assert "verify_public_package.py" in verify_step["run"]
    assert "conda search" not in verify_step["run"]
    assert "--package molsysmt" in verify_step["run"]

    read_only = yaml.safe_load(READ_ONLY.read_text(encoding="utf-8"))
    assert read_only["permissions"] == {"contents": "read"}
    steps = read_only["jobs"]["verify"]["steps"]
    assert any("verify_public_package.py" in step.get("run", "") for step in steps)
    assert all("/promote@" not in step.get("uses", "") for step in steps)
    assert all("ANACONDA_UIBCDF_TOKEN" not in str(step) for step in steps)
