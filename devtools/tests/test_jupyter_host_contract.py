"""Protect the corrected notebook kernel without adding a core dependency."""

import tomllib
from pathlib import Path

from packaging.requirements import Requirement

from devtools.scripts.audit_dependency_contract import _environment_routes, _name

ROOT = Path(__file__).resolve().parents[2]


def test_development_notebook_kernel_excludes_the_lost_read_edge_versions():
    conda, pip, _ = _environment_routes(
        ROOT / "devtools/conda-envs/development_env.yaml"
    )
    specifications = [item for item in conda + pip if _name(item) == "ipykernel"]
    assert len(specifications) == 1, "Declare one corrected Jupyter kernel route"
    requirement = Requirement(specifications[0])
    assert requirement.marker is None and requirement.url is None
    assert not requirement.extras
    for version in ("7.0.0", "7.2.0", "7.3.0", "7.3.99"):
        assert version not in requirement.specifier
    for version in ("7.4.0", "7.4.1"):
        assert version in requirement.specifier


def test_corrected_kernel_is_a_notebook_host_requirement_only():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]
    assert "ipykernel" not in {
        Requirement(item).name for item in project["dependencies"]
    }
    conda, pip, _ = _environment_routes(
        ROOT / "devtools/conda-envs/production_env.yaml"
    )
    assert all(_name(item) != "ipykernel" for item in conda + pip)
