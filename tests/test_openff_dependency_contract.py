"""Testing the dependency contract required by the OpenFF form adapters."""

import tomllib
from pathlib import Path

import pytest
from depdigest import DepConfig, dep_digest, get_info, temporary_package_config
from depdigest.core import checker
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
from packaging.version import Version

from devtools.scripts.audit_dependency_contract import audit
from devtools.scripts.validate_dependencies import SOFT_DEPENDENCIES
from molsysmt._depdigest import LIBRARIES

REPO = Path(__file__).resolve().parents[1]


def test_openff_runtime_bounds_are_in_ci_and_development_environments():
    contract = tomllib.loads((REPO / "devtools/dependency_contract.toml").read_text())
    environments = {entry["path"]: entry for entry in contract["environments"]}
    for relative_path in (
        "devtools/conda-envs/test_env.yaml",
        "devtools/conda-envs/development_env.yaml",
    ):
        assert {"openff.toolkit", "openff.units"} <= set(
            environments[relative_path]["conda_provider_required"]
        )
    assert audit(REPO) == []


def test_openff_runtime_bounds_are_noninstaller_provider_requirements():
    payload = tomllib.loads((REPO / "pyproject.toml").read_text(encoding="utf-8"))
    providers = payload["tool"]["molsysmt"]["provider-requirements"]
    installers = {
        canonicalize_name(Requirement(raw).name)
        for group in [
            payload["project"]["dependencies"],
            *payload["project"]["optional-dependencies"].values(),
        ]
        for raw in group
    }
    assert not {"openff-toolkit", "openff-toolkit-base", "openff-units"} & installers
    for capability, name, minimum in (
        ("openff.toolkit", "openff-toolkit", "0.17.1"),
        ("openff.units", "openff-units", "0.3.0"),
    ):
        requirement = Requirement(providers[capability])
        assert requirement.name == name
        assert requirement.marker is None
        assert not requirement.extras
        assert requirement.url is None
        assert any(
            spec.operator in {">=", ">"} and Version(spec.version) >= Version(minimum)
            for spec in requirement.specifier
        )


@pytest.mark.parametrize(
    ("capability", "package"),
    [("openff.toolkit", "openff-toolkit-base"), ("openff.units", "openff-units")],
)
def test_absent_openff_provider_reports_its_supported_conda_route(
    monkeypatch, capability, package
):
    metadata = LIBRARIES[capability]
    assert metadata == {
        "type": "soft",
        "pypi": None,
        "conda": package,
        "channel": "conda-forge",
    }
    monkeypatch.setattr(checker, "is_installed", lambda name: False)

    def operation():
        raise AssertionError("an absent provider must not execute its consumer")

    operation.__module__ = "openff_acquisition_probe.consumer"
    guarded = dep_digest(capability)(operation)
    with temporary_package_config(
        "openff_acquisition_probe", DepConfig(libraries={capability: metadata})
    ):
        info = get_info("openff_acquisition_probe", format="dict")["dependencies"][0]
        with pytest.raises(ImportError) as missing:
            guarded()
    command = f"conda install -c conda-forge {package}"
    assert info["installed"] is False
    assert info["package_name"] == {"pypi": None, "conda": package}
    assert info["install"] == {"pypi": None, "conda": command}
    assert command in str(missing.value)
    assert "pip install" not in str(missing.value)


def test_dependency_validator_reads_openff_from_the_normative_registry():
    assert {"openff", "rdkit"} <= SOFT_DEPENDENCIES
