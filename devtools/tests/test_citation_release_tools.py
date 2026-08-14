from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "devtools" / "scripts"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _citation_tree(tmp_path: Path) -> Path:
    files = (
        "CITATION.cff",
        ".zenodo.json",
        "README.md",
        "docs/index.ipynb",
        "docs/content/about/citation.md",
        "docs/_bibtex/software.bib",
        "docs/index.AGENTS.md",
    )
    for relative in files:
        source = REPO / relative
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    return tmp_path


def test_repository_citation_metadata_is_coherent():
    validator = _load("validate_citation")
    assert validator.validate_repository(REPO, "1.0.0") == []


def test_validator_rejects_a_historical_doi_on_a_public_surface(tmp_path):
    validator = _load("validate_citation")
    repo = _citation_tree(tmp_path)
    readme = repo / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8").replace(
            validator.CONCEPT_DOI, "10.5281/zenodo.2530946"
        ),
        encoding="utf-8",
    )
    errors = validator.validate_repository(repo, "1.0.0")
    assert any("MolModMT" not in error and "2530946" in error for error in errors)


def test_prepare_release_updates_every_versioned_surface(tmp_path):
    validator = _load("validate_citation")
    repo = _citation_tree(tmp_path)
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "prepare_release.py"),
            "1.2.3",
            "--date",
            "2027-02-03",
            "--repo-root",
            str(repo),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert validator.validate_repository(repo, "1.2.3") == []


def test_zenodo_record_requires_the_exact_tag_and_distinct_version_doi():
    verifier = _load("verify_zenodo_release")
    record = {
        "conceptdoi": "10.5281/zenodo.1298752",
        "doi": "10.5281/zenodo.99999999",
        "status": "published",
        "files": [{"key": "uibcdf/molsysmt-1.0.0.zip"}],
        "metadata": {
            "version": "1.0.0",
            "related_identifiers": [
                {"identifier": "https://github.com/uibcdf/molsysmt/tree/1.0.0"}
            ],
        },
    }
    assert verifier.validate_record(
        record,
        "1.0.0",
        "10.5281/zenodo.1298752",
        "https://github.com/uibcdf/molsysmt",
    ) == []

    wrong = json.loads(json.dumps(record))
    wrong["metadata"]["version"] = "0.12.0"
    errors = verifier.validate_record(
        wrong,
        "1.0.0",
        "10.5281/zenodo.1298752",
        "https://github.com/uibcdf/molsysmt",
    )
    assert any("metadata.version" in error for error in errors)


def test_release_gate_and_workflow_enforce_the_two_citation_phases():
    release_gate = (SCRIPTS / "release_gate.py").read_text(encoding="utf-8")
    assert '("validate_citation.py", "Citation and Zenodo metadata")' in release_gate

    workflow_path = REPO / ".github/workflows/verify-zenodo-release.yaml"
    workflow = yaml.load(workflow_path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    assert workflow["on"]["release"]["types"] == ["released", "prereleased"]
    step = workflow["jobs"]["verify"]["steps"][-1]
    assert "verify_zenodo_release.py" in step["run"]
    assert step["env"]["RELEASE_VERSION"]
