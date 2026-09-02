"""Tests for the Conda ABI3 artifact contract."""

from __future__ import annotations

import json
from pathlib import Path

from devtools.scripts.validate_conda_abi3_artifact import (
    validate_extracted_artifact,
)


def _artifact(
    root: Path,
    *,
    dependencies: list[str] | None = None,
    extension: str = "site-packages/molsysmt/_rust.abi3.so",
) -> Path:
    """Creating a minimal extracted artifact for contract tests."""

    info = root / "info"
    info.mkdir(parents=True)
    payload = {
        "subdir": "linux-64",
        "noarch": "python",
        "build": "pyabi3h1234567_0",
        "depends": dependencies
        or [
            "python >=3.11,<3.14",
            "cpython >=3.11",
            "_python_abi3_support 1.*",
        ],
    }
    (info / "index.json").write_text(json.dumps(payload), encoding="utf-8")
    extension_path = root / extension
    extension_path.parent.mkdir(parents=True)
    extension_path.write_bytes(b"extension")
    return root


def test_accepts_platform_package_with_cep20_metadata(tmp_path):
    artifact = _artifact(tmp_path)

    assert validate_extracted_artifact(artifact, "linux-64") == []


def test_rejects_exact_python_abi_dependency(tmp_path):
    artifact = _artifact(
        tmp_path,
        dependencies=[
            "python >=3.11,<3.14",
            "cpython >=3.11",
            "_python_abi3_support 1.*",
            "python_abi 3.11.* *_cp311",
        ],
    )

    assert "package retains an exact python_abi runtime requirement" in (
        validate_extracted_artifact(artifact, "linux-64")
    )


def test_rejects_interpreter_specific_extension(tmp_path):
    artifact = _artifact(
        tmp_path,
        extension="site-packages/molsysmt/_rust.cpython-311-x86_64-linux-gnu.so",
    )

    problems = validate_extracted_artifact(artifact, "linux-64")
    assert any("does not declare abi3" in problem for problem in problems)


def test_accepts_windows_abi3_extension_name(tmp_path):
    artifact = _artifact(
        tmp_path,
        extension="site-packages/molsysmt/_rust.pyd",
    )
    index_path = artifact / "info" / "index.json"
    payload = json.loads(index_path.read_text(encoding="utf-8"))
    payload["subdir"] = "win-64"
    index_path.write_text(json.dumps(payload), encoding="utf-8")

    assert validate_extracted_artifact(artifact, "win-64") == []


def test_rejects_package_from_another_platform(tmp_path):
    artifact = _artifact(tmp_path)

    problems = validate_extracted_artifact(artifact, "osx-64")
    assert "package subdir is 'linux-64', expected 'osx-64'" in problems


def test_rejects_build_string_that_collides_with_python_variant(tmp_path):
    artifact = _artifact(tmp_path)
    index_path = artifact / "info" / "index.json"
    payload = json.loads(index_path.read_text(encoding="utf-8"))
    payload["build"] = "py311h1234567_0"
    index_path.write_text(json.dumps(payload), encoding="utf-8")

    problems = validate_extracted_artifact(artifact, "linux-64")
    assert "package build string does not identify the ABI3 artifact" in problems
