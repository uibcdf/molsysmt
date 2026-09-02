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


def test_noneditable_build_metadata_is_accepted_with_a_conda_record(
    monkeypatch, tmp_path
):
    _set_distribution(monkeypatch, tmp_path, editable=False)
    conda_meta = tmp_path / "conda-meta"
    conda_meta.mkdir()
    (conda_meta / "molsysmt-0.22.0-py313_1.json").write_text(
        "{}", encoding="utf-8"
    )

    validate_conda_staging._require_conda_install("molsysmt", "0.22.0")


def test_editable_install_is_rejected_even_with_a_conda_record(monkeypatch, tmp_path):
    _set_distribution(monkeypatch, tmp_path, editable=True)
    conda_meta = tmp_path / "conda-meta"
    conda_meta.mkdir()
    (conda_meta / "molsysmt-0.22.0-py313_1.json").write_text(
        "{}", encoding="utf-8"
    )

    with pytest.raises(RuntimeError, match="editable installation"):
        validate_conda_staging._require_conda_install("molsysmt", "0.22.0")


def test_install_without_a_conda_record_is_rejected(monkeypatch, tmp_path):
    _set_distribution(monkeypatch, tmp_path, editable=False)
    (tmp_path / "conda-meta").mkdir()

    with pytest.raises(RuntimeError, match="Expected one Conda record"):
        validate_conda_staging._require_conda_install("molsysmt", "0.22.0")
