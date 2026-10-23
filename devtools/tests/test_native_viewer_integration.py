"""Protecting the new source/installed contract and rejecting retired addon code."""

import tomllib
from importlib.metadata import EntryPoint
from pathlib import Path
from types import SimpleNamespace

import pytest
from setuptools import find_namespace_packages

from devtools.scripts import validate_installed_molsysmt as installed
from devtools.scripts.viewer_tools_contract import TOOLS_ENTRY_POINTS, TOOLS_FILES

ROOT = Path(__file__).resolve().parents[2]


def test_current_source_distribution_does_not_advertise_or_include_legacy_addon():
    config = tomllib.loads((ROOT / "pyproject.toml").read_text())
    assert (
        config["project"]["entry-points"]["molsysviewer.addons"] == TOOLS_ENTRY_POINTS
    )
    discovery = config["tool"]["setuptools"]["packages"]["find"]
    packages = find_namespace_packages(
        where=str(ROOT),
        include=discovery["include"],
        exclude=discovery.get("exclude", []),
    )
    assert "molsysmt" in packages and "molsysviewer_molsysmt" in packages
    assert not any(
        name.startswith("molsysviewer_molsysmt.adapters") for name in packages
    )
    assert not any(name.startswith("molsysviewer_molsysmt.panels") for name in packages)
    sources = {
        p.relative_to(ROOT).as_posix()
        for p in (ROOT / "molsysviewer_molsysmt").rglob("*.py")
    }
    assert sources == TOOLS_FILES


def _distribution(*, entries=None, files=None):
    return SimpleNamespace(
        entry_points=entries
        if entries is not None
        else [
            EntryPoint(name=name, value=value, group="molsysviewer.addons")
            for name, value in TOOLS_ENTRY_POINTS.items()
        ],
        files=list(TOOLS_FILES) if files is None else files,
    )


def test_installed_metadata_requires_the_new_tools_package():
    installed.validate_native_viewer_metadata(_distribution())
    with pytest.raises(RuntimeError, match="files are missing"):
        installed.validate_native_viewer_metadata(
            _distribution(files=["molsysmt/__init__.py"])
        )


def test_installed_backend_requires_a_file_inventory():
    distribution = _distribution()
    distribution.files = None
    with pytest.raises(RuntimeError, match="file inventory"):
        installed.validate_native_viewer_metadata(distribution)


@pytest.mark.parametrize("name", ["molsysmt", "renamed-provider"])
def test_installed_backend_rejects_retired_addon_entry_point(name):
    distribution = _distribution(
        entries=[
            EntryPoint(
                name=name, value="molsysviewer_molsysmt", group="molsysviewer.addons"
            )
        ]
    )
    with pytest.raises(RuntimeError, match="retired"):
        installed.validate_native_viewer_metadata(distribution)


def test_installed_backend_rejects_retired_addon_files():
    distribution = _distribution(
        files=[*TOOLS_FILES, "molsysviewer_molsysmt/runtime.py"]
    )
    with pytest.raises(RuntimeError, match="retired"):
        installed.validate_native_viewer_metadata(distribution)


def test_no_addon_entry_point_cannot_qualify_the_new_distribution():
    with pytest.raises(RuntimeError, match="entry point is missing"):
        installed.validate_native_viewer_metadata(_distribution(entries=[]))
