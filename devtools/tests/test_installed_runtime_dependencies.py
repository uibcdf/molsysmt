"""Protecting installed-runtime dependency closure against incomplete gates."""

from importlib import metadata
from types import SimpleNamespace

import pytest

from devtools.scripts import validate_controlled_dependencies as controlled
from devtools.scripts import validate_installed_molsysmt as installed


@pytest.mark.parametrize("version", [None, "1.0.0"])
def test_installed_public_runtime_rejects_missing_or_old_mmcif(monkeypatch, version):
    distribution = SimpleNamespace(read_text=lambda name: None)
    monkeypatch.setattr(installed.metadata, "distribution", lambda name: distribution)
    monkeypatch.setattr(installed.metadata, "requires", lambda name: ["mmcif>=1.1.1"])

    def version_for(name):
        if version is None:
            raise metadata.PackageNotFoundError(name)
        return version

    monkeypatch.setattr(installed.metadata, "version", version_for)
    with pytest.raises(RuntimeError, match="mmcif>=1.1.1"):
        installed.validate_public_runtime()


def test_controlled_gate_rejects_transitive_conflict_above_direct_floor(
    tmp_path, monkeypatch, capsys
):
    # This scenario exercises transitive closure, not today's provider versions.
    (tmp_path / "pyproject.toml").write_text(
        '[project]\ndependencies = ["pyunitwizard>=1.0", "argdigest>=1.0"]\n'
    )
    pins = tmp_path / "controlled_sources.txt"
    pins.write_text(
        f"git+https://github.com/uibcdf/pyunitwizard@{'0' * 40}\n"
        f"git+https://github.com/uibcdf/argdigest@{'1' * 40}\n"
    )
    monkeypatch.setattr(controlled, "ROOT", tmp_path)
    monkeypatch.setattr(controlled, "PINS", pins)
    versions = {"argdigest": "1.0", "pyunitwizard": "1.0"}
    monkeypatch.setattr(controlled.importlib.metadata, "version", versions.__getitem__)
    monkeypatch.setattr(
        controlled.importlib.metadata,
        "requires",
        lambda name: ["argdigest>=2.0"] if name == "pyunitwizard" else [],
    )
    assert (
        controlled.find_violations(
            ["pyunitwizard>=1.0", "argdigest>=1.0"],
            list(versions),
            versions.__getitem__,
        )
        == []
    )
    assert controlled.main() == 1
    assert capsys.readouterr().out.splitlines() == [
        "[CONTROLLED_DEPENDENCY] pyunitwizard: installed argdigest 1.0 violates argdigest>=2.0"
    ]
    versions["argdigest"] = "2.0"
    assert controlled.main() == 0


def test_runtime_closure_honors_markers_and_terminates_cycles():
    requirements = {
        "molsysmt": [
            "molsysviewer>=0.23",
            'optional-backend; extra == "soft"',
            'other-platform; python_version < "3.0"',
        ],
        "molsysviewer": ["molsysmt>=0.22"],
    }
    versions = {"molsysmt": "0.22.4", "molsysviewer": "0.23.4"}
    assert (
        installed.find_runtime_dependency_violations(
            ["molsysmt"], requirements.__getitem__, versions.__getitem__
        )
        == []
    )


def test_runtime_closure_checks_extras_requested_by_required_dependencies():
    requirements = {
        "molsysmt": ["widget[renderer]>=1"],
        "widget": ['render-backend>=2; extra == "renderer"'],
    }
    versions = {"widget": "1.0", "render-backend": "1.0"}
    assert installed.find_runtime_dependency_violations(
        ["molsysmt"], requirements.__getitem__, versions.__getitem__
    ) == [
        'widget: installed render-backend 1.0 violates render-backend>=2; extra == "renderer"'
    ]
