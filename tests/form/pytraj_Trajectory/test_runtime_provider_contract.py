"""Keeping PyTraj acquisition tied to the supported AmberTools bundle."""

import tomllib
from pathlib import Path

import pytest
import yaml
from depdigest import DepConfig, dep_digest, get_info, temporary_package_config
from depdigest.core import checker
from packaging.requirements import Requirement

from molsysmt._depdigest import LIBRARIES
from molsysmt._private.smonitor import LibraryNotFoundError


def test_optional_pytraj_declares_only_the_supported_conda_route():
    root = Path(__file__).resolve().parents[3]
    project = tomllib.loads((root / "pyproject.toml").read_text())["project"]
    requirements = [*project["dependencies"], *project["optional-dependencies"]["soft"]]
    assert not any(Requirement(item).name.lower() == "pytraj" for item in requirements)
    assert LIBRARIES["pytraj"] == {
        "type": "soft",
        "pypi": None,
        "conda": "ambertools",
        "channel": "conda-forge",
    }
    inventory = tomllib.loads((root / "devtools/dependency_contract.toml").read_text())
    for filename in ("development_env.yaml", "test_env.yaml"):
        entry = next(
            item
            for item in inventory["environments"]
            if item["path"] == f"devtools/conda-envs/{filename}"
        )
        assert "pytraj" in entry.get("conda_provider_required", [])
        dependencies = yaml.safe_load(
            (root / "devtools/conda-envs" / filename).read_text()
        )["dependencies"]
        assert "ambertools" in dependencies
        assert not any(
            Requirement(raw).name.lower() == "pytraj"
            for item in dependencies
            if isinstance(item, dict)
            for raw in item.get("pip", [])
        )


def test_absent_pytraj_reports_the_bundle_route_without_importing_the_engine(
    monkeypatch,
):
    original = checker.is_installed
    monkeypatch.setattr(
        checker,
        "is_installed",
        lambda name: False if name == "pytraj" else original(name),
    )

    def operation():
        raise AssertionError("The operation must not run without the optional engine.")

    operation.__module__ = "molsysmt_pytraj_route_guard.operation"
    wrapped = dep_digest("pytraj")(operation)
    config = DepConfig(
        libraries={"pytraj": LIBRARIES["pytraj"]}, exception_class=LibraryNotFoundError
    )
    with temporary_package_config("molsysmt_pytraj_route_guard", config):
        info = get_info("molsysmt_pytraj_route_guard", format="dict")["dependencies"][0]
        assert info["package_name"] == {"pypi": None, "conda": "ambertools"}
        assert info["install"] == {
            "pypi": None,
            "conda": "conda install -c conda-forge ambertools",
        }
        with pytest.raises(LibraryNotFoundError) as caught:
            wrapped()
    assert "conda install -c conda-forge ambertools" in str(caught.value)
    assert "pip install" not in str(caught.value)
    assert "Install 'pytraj'" not in str(caught.value)
