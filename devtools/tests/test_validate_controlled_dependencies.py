"""Regression tests for the controlled-source runtime floor gate."""

import pytest

from devtools.scripts import validate_controlled_dependencies as gate
from devtools.scripts.validate_controlled_dependencies import (
    controlled_names,
    find_violations,
)


def test_released_argdigest_floor_rejects_the_old_smonitor_incompatible_source():
    requirements = ["argdigest>=0.13.0", "smonitor>=0.16.0"]
    versions = {"argdigest": "0.12.1", "smonitor": "0.16.0"}

    assert find_violations(requirements, list(versions), versions.__getitem__) == [
        "argdigest: installed 0.12.1 violates argdigest>=0.13.0"
    ]

    versions["argdigest"] = "0.13.0"
    assert find_violations(requirements, list(versions), versions.__getitem__) == []


def test_pyunitwizard_floor_rejects_a_version_without_active_policy_api():
    requirements = ["pyunitwizard>=0.25.0"]
    versions = {"pyunitwizard": "0.24.0"}
    assert find_violations(requirements, list(versions), versions.__getitem__) == [
        "pyunitwizard: installed 0.24.0 violates pyunitwizard>=0.25.0"
    ]
    versions["pyunitwizard"] = "0.25.0"
    assert find_violations(requirements, list(versions), versions.__getitem__) == []


def test_controlled_source_pins_must_be_full_unique_commit_references():
    valid = "git+https://github.com/uibcdf/argdigest@" + "a" * 40
    assert controlled_names(valid) == ["argdigest"]
    with pytest.raises(ValueError, match="invalid controlled source pin"):
        controlled_names("git+https://github.com/uibcdf/argdigest@main")
    with pytest.raises(ValueError, match="duplicate controlled source pin"):
        controlled_names(f"{valid}\n{valid}")


def test_cli_checks_the_real_runtime_contract_against_installed_versions(monkeypatch):
    versions = {
        "smonitor": "0.16.0",
        "depdigest": "0.11.0",
        "pyunitwizard": "0.25.0",
        "argdigest": "0.13.0",
    }
    monkeypatch.setattr(gate.importlib.metadata, "version", versions.__getitem__)
    assert gate.main() == 0

    versions["argdigest"] = "0.12.1"
    assert gate.main() == 1
