"""Testing the dependency contract required by the OpenFF form adapters."""

import tomllib
from pathlib import Path

from packaging.requirements import Requirement
from packaging.version import Version

from devtools.scripts.audit_dependency_contract import audit
from devtools.scripts.validate_dependencies import SOFT_DEPENDENCIES

REPO = Path(__file__).resolve().parents[1]


def test_openff_runtime_bounds_are_in_ci_and_development_environments():
    contract = tomllib.loads((REPO / "devtools/dependency_contract.toml").read_text())
    environments = {entry["path"]: entry for entry in contract["environments"]}
    for relative_path in (
        "devtools/conda-envs/test_env.yaml",
        "devtools/conda-envs/development_env.yaml",
    ):
        assert {"openff-toolkit", "openff-units"} <= set(
            environments[relative_path]["optional_required"]
        )
    assert audit(REPO) == []


def test_openff_runtime_bounds_are_in_the_soft_dependency_extra():
    payload = tomllib.loads((REPO / "pyproject.toml").read_text(encoding="utf-8"))
    dependencies = {
        requirement.name: requirement
        for requirement in map(
            Requirement, payload["project"]["optional-dependencies"]["soft"]
        )
    }
    for name, minimum in (("openff-toolkit", "0.17.1"), ("openff-units", "0.3.0")):
        requirement = dependencies[name]
        assert requirement.marker is None
        assert any(
            spec.operator in {">=", ">"} and Version(spec.version) >= Version(minimum)
            for spec in requirement.specifier
        )


def test_dependency_validator_reads_openff_from_the_normative_registry():
    assert {"openff", "rdkit"} <= SOFT_DEPENDENCIES
