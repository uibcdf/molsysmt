"""Behavioral tests for Conda staging provenance validation."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from devtools.scripts import validate_conda_staging


class _Distribution:
    def __init__(self, root: Path, *, editable: bool) -> None:
        self._root = root
        self._editable = editable

    def read_text(self, filename: str) -> str | None:
        if filename != "direct_url.json":
            return None
        return json.dumps({"dir_info": {"editable": self._editable}})

    def locate_file(self, filename: str) -> Path:
        return self._root / filename


def _set_distribution(monkeypatch, prefix: Path, *, editable: bool) -> None:
    distribution = _Distribution(prefix / "lib" / "site-packages", editable=editable)
    monkeypatch.setattr(
        validate_conda_staging.importlib.metadata,
        "distribution",
        lambda name: distribution,
    )
    monkeypatch.setattr(validate_conda_staging.sys, "prefix", str(prefix))


def _write_conda_record(
    prefix: Path,
    *,
    build: str = "pyabi3h1234567_2",
    dependencies: list[str] | None = None,
) -> None:
    conda_meta = prefix / "conda-meta"
    conda_meta.mkdir()
    payload = {
        "build": build,
        "depends": dependencies
        or [
            "python >=3.11,<3.14",
            "cpython >=3.11",
            "_python_abi3_support 1.*",
        ],
    }
    (conda_meta / f"molsysmt-0.22.0-{build}.json").write_text(
        json.dumps(payload), encoding="utf-8"
    )


def test_noneditable_build_metadata_is_accepted_with_a_conda_record(
    monkeypatch, tmp_path
):
    _set_distribution(monkeypatch, tmp_path, editable=False)
    _write_conda_record(tmp_path)

    validate_conda_staging._require_conda_install(
        "molsysmt", "0.22.0", require_abi3=True
    )


def test_editable_install_is_rejected_even_with_a_conda_record(monkeypatch, tmp_path):
    _set_distribution(monkeypatch, tmp_path, editable=True)
    _write_conda_record(tmp_path)

    with pytest.raises(RuntimeError, match="editable installation"):
        validate_conda_staging._require_conda_install("molsysmt", "0.22.0")


def test_install_without_a_conda_record_is_rejected(monkeypatch, tmp_path):
    _set_distribution(monkeypatch, tmp_path, editable=False)
    (tmp_path / "conda-meta").mkdir()

    with pytest.raises(RuntimeError, match="Expected one Conda record"):
        validate_conda_staging._require_conda_install("molsysmt", "0.22.0")


def test_legacy_python_specific_build_is_rejected(monkeypatch, tmp_path):
    _set_distribution(monkeypatch, tmp_path, editable=False)
    _write_conda_record(tmp_path, build="py313h1234567_1")

    with pytest.raises(RuntimeError, match="non-ABI3 Conda build"):
        validate_conda_staging._require_conda_install(
            "molsysmt", "0.22.0", require_abi3=True
        )


def test_abi3_build_with_exact_python_abi_is_rejected(monkeypatch, tmp_path):
    _set_distribution(monkeypatch, tmp_path, editable=False)
    _write_conda_record(
        tmp_path,
        dependencies=[
            "python >=3.11,<3.14",
            "cpython >=3.11",
            "_python_abi3_support 1.*",
            "python_abi 3.11.* *_cp311",
        ],
    )

    with pytest.raises(RuntimeError, match="exact python_abi requirement"):
        validate_conda_staging._require_conda_install(
            "molsysmt", "0.22.0", require_abi3=True
        )
