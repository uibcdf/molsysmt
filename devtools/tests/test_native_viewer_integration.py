"""Protecting native Viewer integration without the retired MolSysMT addon."""

import tomllib
from fnmatch import fnmatchcase
from importlib.metadata import EntryPoint
from pathlib import Path
from types import SimpleNamespace

import pytest
from setuptools import find_namespace_packages

from devtools.scripts import validate_installed_molsysmt as installed

ROOT = Path(__file__).resolve().parents[2]


def test_current_source_distribution_does_not_advertise_or_include_legacy_addon(
    tmp_path,
):
    config = tomllib.loads((ROOT / "pyproject.toml").read_text())
    entries = config["project"].get("entry-points", {})
    assert not entries.get("molsysviewer.addons")
    discovery = config["tool"]["setuptools"]["packages"]["find"]
    # Exercise real discovery with both providers present, without traversing
    # unrelated documentation/build trees in a development checkout.
    for name in ("molsysmt", "molsysviewer_molsysmt"):
        package = tmp_path / name
        package.mkdir()
        (package / "__init__.py").write_text("")
    packages = find_namespace_packages(
        where=str(tmp_path),
        include=discovery["include"],
        exclude=discovery.get("exclude", []),
    )
    assert "molsysmt" in packages
    assert not any(
        fnmatchcase(package, "molsysviewer_molsysmt*") for package in packages
    )
    assert not list((ROOT / "molsysviewer_molsysmt").rglob("*.py"))


def test_installed_backend_metadata_needs_no_addon():
    distribution = SimpleNamespace(
        entry_points=[
            EntryPoint(name="other-tool", value="tool:main", group="console_scripts")
        ],
        files=["molsysmt/__init__.py"],
    )
    installed.validate_native_viewer_metadata(distribution)


def test_installed_backend_requires_a_file_inventory():
    with pytest.raises(RuntimeError, match="file inventory"):
        installed.validate_native_viewer_metadata(
            SimpleNamespace(entry_points=[], files=None)
        )


@pytest.mark.parametrize("name", ["molsysmt", "renamed-provider"])
def test_installed_backend_rejects_retired_addon_entry_point(name):
    distribution = SimpleNamespace(
        entry_points=[
            EntryPoint(
                name=name, value="molsysviewer_molsysmt", group="molsysviewer.addons"
            )
        ],
        files=["molsysmt/__init__.py"],
    )
    with pytest.raises(RuntimeError, match="retired"):
        installed.validate_native_viewer_metadata(distribution)


def test_installed_backend_rejects_retired_addon_files():
    distribution = SimpleNamespace(
        entry_points=[], files=["molsysviewer_molsysmt/runtime.py"]
    )
    with pytest.raises(RuntimeError, match="retired"):
        installed.validate_native_viewer_metadata(distribution)
