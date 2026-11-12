"""Regression tests for the read-only dependency-route auditor."""

from __future__ import annotations

import ast
import shutil
import tomllib
from pathlib import Path

import pytest
import yaml

from devtools.scripts.audit_dependency_contract import _registry_findings, audit

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def contract_tree(tmp_path):
    """Copy every audited surface without touching the working repository."""
    paths = [
        ROOT / "pyproject.toml",
        ROOT / "molsysmt/_depdigest.py",
        ROOT / "devtools/dependency_contract.toml",
        ROOT / "devtools/controlled_sources.txt",
        *sorted((ROOT / "devtools/conda-build").glob("*.yaml")),
        *sorted((ROOT / "devtools/rattler-build").glob("*.yaml")),
        *sorted((ROOT / "devtools/conda-envs").glob("*.yaml")),
        *sorted((ROOT / ".github/workflows").glob("*.yaml")),
        *sorted((ROOT / ".github/workflows").glob("*.yml")),
    ]
    for path in paths:
        destination = tmp_path / path.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
    return tmp_path


def _replace(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert old in text
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def _replace_provider_table(root: Path, replacement: str) -> None:
    path = root / "pyproject.toml"
    text = path.read_text()
    start = text.index("[tool.molsysmt.provider-requirements]")
    end = text.index("\n[", start + 1)
    path.write_text(text[:start] + replacement + "\n" + text[end:])


def test_current_dependency_routes_are_coherent():
    assert audit(ROOT) == []


def test_optional_conda_only_route_does_not_require_a_pypi_alias(contract_tree):
    _replace(
        contract_tree / "molsysmt/_depdigest.py",
        "LIBRARIES = {",
        'LIBRARIES = {\n    "example_engine": {"type": "soft", "pypi": None, '
        '"conda": "example-bundle", "channel": "conda-forge"},',
    )
    assert audit(contract_tree) == []


@pytest.mark.parametrize(
    ("metadata", "message"),
    [
        ('{"type": "hard", "pypi": None}', "has no public Python distribution route"),
        ('{"type": "unknown", "pypi": None}', "unknown dependency classification"),
        ('{"type": "soft", "pypi": false}', "invalid Python distribution route"),
        ('{"type": "soft", "pypi": ""}', "invalid Python distribution route"),
    ],
)
def test_disabled_pip_route_does_not_hide_invalid_classification(
    contract_tree, metadata, message
):
    # The fixture is Python source, not JSON.
    metadata = metadata.replace("false", "False")
    _replace(
        contract_tree / "molsysmt/_depdigest.py",
        "LIBRARIES = {",
        f'LIBRARIES = {{\n    "example_engine": {metadata},',
    )
    assert any(message in finding.message for finding in audit(contract_tree))


@pytest.mark.parametrize("environment", ["development_env.yaml", "test_env.yaml"])
def test_required_conda_provider_cannot_be_removed(contract_tree, environment):
    path = f"devtools/conda-envs/{environment}"
    _replace(contract_tree / path, "- ambertools\n", "")
    assert any(
        finding.path == path
        and "missing Conda provider pytraj: ambertools" in finding.message
        for finding in audit(contract_tree)
    )


@pytest.mark.parametrize(
    ("conda", "pip", "message"),
    [
        (["ambertools", "pytraj >=2.0.6"], [], "standalone dependency pytraj"),
        (["ambertools"], ["pytraj>=2.0.6"], "standalone dependency pytraj"),
        (["ambertools"], ["ambertools"], "pip override for Conda provider pytraj"),
        (["ambertools", "ambertools"], [], "duplicate Conda provider pytraj"),
        (["ambertools", "ambertools <23.0"], [], "duplicate Conda provider pytraj"),
        (["ambertools >=26"], [], "unqualified constraint for Conda provider pytraj"),
        (
            ["ambertools[unreviewed]"],
            [],
            "unqualified constraint for Conda provider pytraj",
        ),
        (
            ["ambertools; python_version < '3.0'"],
            [],
            "unqualified constraint for Conda provider pytraj",
        ),
        (
            ["ambertools @ https://example.invalid/bundle.whl"],
            [],
            "unqualified constraint for Conda provider pytraj",
        ),
    ],
)
def test_required_conda_provider_rejects_overrides_and_invented_floors(
    contract_tree, conda, pip, message
):
    path = "devtools/conda-envs/test_env.yaml"
    payload = yaml.safe_load((contract_tree / path).read_text())
    payload["dependencies"].remove("ambertools")
    payload["dependencies"].extend(conda)
    if pip:
        payload["dependencies"].append({"pip": pip})
    (contract_tree / path).write_text(yaml.safe_dump(payload, sort_keys=False))
    assert any(
        finding.path == path and message in finding.message
        for finding in audit(contract_tree)
    )


@pytest.mark.parametrize(
    ("channels", "message"),
    [
        (["uibcdf", "ambermd"], "missing declared channel conda-forge"),
        ("conda-forge", "environment channels must be a list"),
        ([False], "environment channels must be a list"),
    ],
)
def test_conda_provider_requires_its_declared_channel(contract_tree, channels, message):
    path = "devtools/conda-envs/test_env.yaml"
    payload = yaml.safe_load((contract_tree / path).read_text())
    payload["channels"] = channels
    (contract_tree / path).write_text(yaml.safe_dump(payload, sort_keys=False))
    assert any(
        finding.path == path and message in finding.message
        for finding in audit(contract_tree)
    )


@pytest.mark.parametrize(
    ("value", "message"),
    [
        ('"pytraj"', "must be a list of registry capability names"),
        ("[false]", "must be a list of registry capability names"),
        ('["pytraj", "pytraj"]', "declares a capability more than once"),
        ('["not_a_provider"]', "unknown Conda provider capability not_a_provider"),
        ('["pytraj>=2.0.6"]', "unknown Conda provider capability pytraj>=2.0.6"),
        ('["nglview"]', "is not a soft Conda-only provider"),
    ],
)
def test_conda_provider_inventory_uses_unique_known_capabilities(
    contract_tree, value, message
):
    _replace(
        contract_tree / "devtools/dependency_contract.toml",
        'conda_provider_required = ["pytraj", "openff.toolkit", "openff.units"]',
        f"conda_provider_required = {value}",
    )
    assert any(message in finding.message for finding in audit(contract_tree))


def test_misspelled_provider_inventory_cannot_disable_acquisition_checks(contract_tree):
    _replace(
        contract_tree / "devtools/dependency_contract.toml",
        'conda_provider_required = ["pytraj", "openff.toolkit", "openff.units"]',
        'conda_providers_required = ["pytraj"]',
    )
    assert any(
        "unknown environment inventory fields" in finding.message
        for finding in audit(contract_tree)
    )


@pytest.mark.parametrize(
    ("old", "new", "message"),
    [
        ('"pypi": None', '"pypi": "pytraj"', "is not a soft Conda-only provider"),
        ('"conda": "ambertools"', '"conda": None', "invalid Conda package route"),
        ('"conda": "ambertools"', '"conda": False', "invalid Conda package route"),
        ('"conda": "ambertools"', '"conda": ""', "invalid Conda package route"),
        (
            '"conda": "ambertools"',
            '"conda": "ambertools>=26"',
            "invalid Conda package route",
        ),
        ('"channel": "conda-forge"', '"channel": None', "invalid Conda channel"),
        ('"channel": "conda-forge"', '"channel": False', "invalid Conda channel"),
        ('"channel": "conda-forge"', '"channel": ""', "invalid Conda channel"),
    ],
)
def test_conda_provider_routes_come_from_valid_registry_metadata(
    contract_tree, old, new, message
):
    path = contract_tree / "molsysmt/_depdigest.py"
    text = path.read_text()
    start = text.index('    "pytraj": {')
    end = text.index("    },", start) + len("    },")
    provider = text[start:end]
    assert old in provider
    path.write_text(text[:start] + provider.replace(old, new, 1) + text[end:])
    assert any(message in finding.message for finding in audit(contract_tree))


@pytest.mark.parametrize(
    ("route", "channel", "requirements", "message"),
    [
        ("molsysviewer", "uibcdf", {"molsysviewer"}, None),
        ("molsysviewer", "uibcdf", set(), "is absent from pyproject.toml"),
        (None, "uibcdf", {"molsysviewer"}, "has no public Python distribution route"),
        ("molsysviewer", None, {"molsysviewer"}, "invalid hard Conda"),
        ("molsysviewer", False, {"molsysviewer"}, "invalid hard Conda"),
        ("molsysviewer", "", {"molsysviewer"}, "invalid hard Conda"),
        ("molsysviewer>=0.24", "uibcdf", {"molsysviewer"}, "invalid hard Conda"),
        ("molsysviewer[extra]", "uibcdf", {"molsysviewer"}, "invalid hard Conda"),
        ("molsysviewer; python_version<'3.12'", "uibcdf", set(), "invalid hard Conda"),
        ("not a package name", "uibcdf", set(), "invalid hard Conda"),
    ],
)
def test_hard_conda_hint_still_requires_valid_route_and_runtime_metadata(
    route, channel, requirements, message
):
    findings = _registry_findings(
        {
            "molsysviewer": {
                "type": "hard",
                "pypi": None,
                "conda": route,
                "channel": channel,
            }
        },
        requirements,
    )
    if message is None:
        assert findings == []
    else:
        assert len(findings) == 1 and message in findings[0].message


@pytest.mark.parametrize("requirement", ["pytraj>=2.0.6", "ambertools>=26"])
@pytest.mark.parametrize("extra", ["soft", "test"])
def test_conda_only_provider_cannot_gain_a_fake_public_pip_route(
    contract_tree, requirement, extra
):
    _replace(
        contract_tree / "pyproject.toml",
        f"{extra} = [",
        f'{extra} = [\n  "{requirement}",',
    )
    assert any(
        "Conda-only provider pytraj has a public pip requirement" in finding.message
        for finding in audit(contract_tree)
    )


def test_another_required_conda_provider_uses_its_own_registry_route(contract_tree):
    _replace(
        contract_tree / "molsysmt/_depdigest.py",
        "LIBRARIES = {",
        'LIBRARIES = {\n    "example_engine": {"type": "soft", "pypi": None, '
        '"conda": "example-bundle", "channel": "example-channel"},',
    )
    _replace(
        contract_tree / "devtools/dependency_contract.toml",
        'conda_provider_required = ["pytraj", "openff.toolkit", "openff.units"]',
        'conda_provider_required = ["pytraj", "openff.toolkit", "openff.units", "example_engine"]',
    )
    path = contract_tree / "devtools/conda-envs/development_env.yaml"
    payload = yaml.safe_load(path.read_text())
    payload["dependencies"].append("example-bundle")
    payload["channels"].append("example-channel")
    path.write_text(yaml.safe_dump(payload, sort_keys=False))
    assert audit(contract_tree) == []


@pytest.mark.parametrize(
    ("replacement", "message"),
    [
        ("[tool.molsysmt]\nprovider-requirements = false", "must be a table"),
        ("[tool.molsysmt]\nprovider-requirements = []", "must be a table"),
        (
            '[tool.molsysmt.provider-requirements]\n"openff.toolkit" = false',
            "invalid provider requirement",
        ),
        (
            '[tool.molsysmt.provider-requirements]\n"openff.toolkit" = []',
            "invalid provider requirement",
        ),
        (
            '[tool.molsysmt.provider-requirements]\n"unknown.engine" = "example>=1"',
            "unknown provider-requirements capability",
        ),
        (
            '[tool.molsysmt.provider-requirements]\n"nglview" = "nglview>=3.0.4"',
            "is not Conda-only",
        ),
        (
            '[tool.molsysmt.provider-requirements]\n"openff.toolkit" = "openff-toolkit"',
            "must declare only version constraints",
        ),
        (
            '[tool.molsysmt.provider-requirements]\n"openff.toolkit" = "openff-toolkit>=0.17.1; python_version < \'3.0\'"',
            "must declare only version constraints",
        ),
        (
            '[tool.molsysmt.provider-requirements]\n"openff.toolkit" = "openff-toolkit[extra]>=0.17.1"',
            "must declare only version constraints",
        ),
        (
            '[tool.molsysmt.provider-requirements]\n"openff.toolkit" = "openff-toolkit @ https://example.invalid/toolkit.whl"',
            "must declare only version constraints",
        ),
        (
            '[tool.molsysmt.provider-requirements]\n"openff.toolkit" = "openff-toolkit>=0.17.1"\n"openff.units" = "OpenFF_Toolkit>=0.3.0"',
            "duplicate provider requirement distribution",
        ),
    ],
)
def test_noninstaller_provider_requirements_validate_schema_and_identity(
    contract_tree, replacement, message
):
    _replace_provider_table(contract_tree, replacement)
    with pytest.raises(ValueError, match=message):
        audit(contract_tree)


def test_provider_conda_packages_cannot_be_duplicated(contract_tree):
    _replace(
        contract_tree / "molsysmt/_depdigest.py",
        '"conda": "openff-units"',
        '"conda": "openff-toolkit-base"',
    )
    with pytest.raises(ValueError, match="duplicate provider Conda package"):
        audit(contract_tree)


def test_derived_provider_alias_cannot_be_redeclared_in_the_inventory(contract_tree):
    _replace(
        contract_tree / "devtools/dependency_contract.toml",
        "[conda_names]",
        '[conda_names]\nopenff-toolkit = "openff-toolkit-base"',
    )
    with pytest.raises(ValueError, match="must be derived from DepDigest only"):
        audit(contract_tree)


def test_an_alternate_alias_cannot_invent_a_conda_provider_package(contract_tree):
    _replace(
        contract_tree / "devtools/dependency_contract.toml",
        "[conda_names]",
        '[conda_names]\nopenff-toolkit = "made-up-toolkit"',
    )
    path = contract_tree / "devtools/conda-envs/docs_env.yaml"
    payload = yaml.safe_load(path.read_text())
    payload["dependencies"].append("made-up-toolkit >=0.17.1")
    path.write_text(yaml.safe_dump(payload, sort_keys=False))
    with pytest.raises(ValueError, match="must be derived from DepDigest only"):
        audit(contract_tree)


@pytest.mark.parametrize("extra", ["soft", "test"])
@pytest.mark.parametrize(
    "requirement",
    ["openff-toolkit>=0.17.1", "openff-toolkit-base>=0.17.1", "openff-units>=0.3.0"],
)
def test_versioned_conda_provider_cannot_be_advertised_as_a_pip_installer(
    contract_tree, extra, requirement
):
    _replace(
        contract_tree / "pyproject.toml",
        f"{extra} = [",
        f'{extra} = [\n  "{requirement}",',
    )
    with pytest.raises(ValueError, match="has a public pip requirement"):
        audit(contract_tree)


@pytest.mark.parametrize(
    "requirement",
    ["openff-toolkit>=0.17.1", "openff-toolkit-base>=0.17.1", "openff-units>=0.3.0"],
)
def test_observed_nonrequired_provider_still_uses_its_conda_route(
    contract_tree, requirement
):
    path = "devtools/conda-envs/docs_env.yaml"
    payload = yaml.safe_load((contract_tree / path).read_text())
    payload["dependencies"].append({"pip": [requirement]})
    (contract_tree / path).write_text(yaml.safe_dump(payload, sort_keys=False))
    assert any(
        finding.path == path
        and (
            "standalone dependency openff-toolkit" in finding.message
            or "pip override for Conda provider openff." in finding.message
        )
        for finding in audit(contract_tree)
    )


def test_absent_nonrequired_versioned_providers_remain_optional(contract_tree):
    path = contract_tree / "devtools/dependency_contract.toml"
    path.write_text(path.read_text().replace(', "openff.toolkit", "openff.units"', ""))
    for environment in ("development_env.yaml", "test_env.yaml"):
        path = contract_tree / "devtools/conda-envs" / environment
        _replace(path, "- openff-toolkit-base >=0.17.1\n", "")
        _replace(path, "- openff-units >=0.3.0\n", "")
    assert audit(contract_tree) == []


def test_provider_floor_changes_are_read_from_pyproject_not_a_second_registry(
    contract_tree,
):
    _replace(
        contract_tree / "pyproject.toml",
        '"openff.units" = "openff-units>=0.3.0"',
        '"openff.units" = "openff-units>=0.3.1"',
    )
    assert any(
        "openff-units declares >=0.3.0; pyproject.toml requires >=0.3.1"
        in finding.message
        for finding in audit(contract_tree)
    )


@pytest.mark.parametrize(
    ("old", "new", "provider"),
    [
        ("- mdtraj >=1.11.0", "- mdtraj", "mdtraj"),
        ("- mdtraj >=1.11.0", "- mdtraj >=1.10.2", "mdtraj"),
        ("- mdtraj >=1.11.0", "- mdtraj >=1.11.2", "mdtraj"),
        ("- pyparsing !=3.3.3", "- pyparsing", "pyparsing"),
        ("- pyparsing !=3.3.3", "- pyparsing <3.3.3", "pyparsing"),
    ],
)
def test_runtime_optional_constraints_cannot_drift(contract_tree, old, new, provider):
    path = "devtools/conda-envs/test_env.yaml"
    _replace(contract_tree / path, old, new)
    assert any(
        finding.path == path and f"{provider} declares" in finding.message
        for finding in audit(contract_tree)
    )


def test_required_optional_coverage_cannot_be_removed(contract_tree):
    path = "devtools/conda-envs/development_env.yaml"
    _replace(contract_tree / path, "- mdtraj >=1.11.0\n", "")
    assert any(
        finding.path == path and finding.message == "missing mdtraj>=1.11.0"
        for finding in audit(contract_tree)
    )


def test_unselected_optional_engines_remain_optional():
    production = yaml.safe_load(
        (ROOT / "devtools/conda-envs/production_env.yaml").read_text()
    )["dependencies"]
    assert not any(str(item).startswith("mdtraj") for item in production)
    assert audit(ROOT) == []


def test_new_runtime_optional_requirements_are_discovered_from_the_public_extra(
    contract_tree,
):
    _replace(
        contract_tree / "pyproject.toml",
        "soft = [",
        'soft = [\n  "example-optional>=2",',
    )
    path = "devtools/conda-envs/test_env.yaml"
    _replace(
        contract_tree / path,
        "- pyparsing !=3.3.3",
        "- pyparsing !=3.3.3\n- example-optional >=1",
    )
    assert any(
        finding.path == path and "example-optional declares >=1" in finding.message
        for finding in audit(contract_tree)
    )


def test_unknown_runtime_extra_cannot_silently_disable_optional_auditing(contract_tree):
    _replace(
        contract_tree / "devtools/dependency_contract.toml",
        'runtime_extras = ["soft"]',
        'runtime_extras = ["not-a-public-extra"]',
    )
    with pytest.raises(ValueError, match="runtime extra"):
        audit(contract_tree)


def test_conda_alias_retains_the_public_optional_floor(contract_tree):
    path = "devtools/conda-envs/test_env.yaml"
    _replace(
        contract_tree / path,
        "- openff-toolkit-base >=0.17.1",
        "- openff-toolkit-base >=0.16",
    )
    assert any(
        finding.path == path and "openff-toolkit declares >=0.16" in finding.message
        for finding in audit(contract_tree)
    )


@pytest.mark.parametrize("environment", ["test_env.yaml", "development_env.yaml"])
def test_existing_openff_coverage_remains_required(contract_tree, environment):
    path = f"devtools/conda-envs/{environment}"
    _replace(contract_tree / path, "- openff-units >=0.3.0\n", "")
    assert any(
        finding.path == path and finding.message == "missing openff-units>=0.3.0"
        for finding in audit(contract_tree)
    )


def test_optional_alias_cannot_hide_duplicate_providers(contract_tree):
    path = "devtools/conda-envs/test_env.yaml"
    _replace(
        contract_tree / path,
        "- openff-toolkit-base >=0.17.1",
        "- openff-toolkit-base >=0.17.1\n- openff-toolkit >=0.17.1",
    )
    assert any(
        finding.path == path
        and finding.message == "duplicate runtime dependency: openff-toolkit"
        for finding in audit(contract_tree)
    )


@pytest.mark.parametrize(
    "replacement",
    [
        'openff-toolkit>=0.17.1; python_version < "3.0"',
        'openff-toolkit>=0.17.1; sys_platform == "win32"',
        "openff-toolkit[unreviewed]>=0.17.1",
        "openff-toolkit @ https://example.invalid/unreviewed.whl",
    ],
)
def test_required_optional_provider_must_not_hide_behind_a_pip_override(
    contract_tree, replacement
):
    path = "devtools/conda-envs/test_env.yaml"
    payload = yaml.safe_load((contract_tree / path).read_text())
    payload["dependencies"].remove("openff-toolkit-base >=0.17.1")
    pip = []
    payload["dependencies"].append({"pip": pip})
    pip.append(replacement)
    (contract_tree / path).write_text(yaml.safe_dump(payload, sort_keys=False))
    assert any(
        finding.path == path and "openff-toolkit declares" in finding.message
        for finding in audit(contract_tree)
    )


def test_absent_nonrequired_optional_provider_does_not_become_mandatory(contract_tree):
    _replace(
        contract_tree / "pyproject.toml",
        "soft = [",
        'soft = [\n  "example-optional>=2",',
    )
    assert audit(contract_tree) == []


def test_matching_optional_extra_declarations_remain_parseable(contract_tree):
    _replace(
        contract_tree / "pyproject.toml",
        "soft = [",
        'soft = [\n  "example-optional[analysis]>=2",',
    )
    path = contract_tree / "devtools/conda-envs/test_env.yaml"
    payload = yaml.safe_load(path.read_text())
    payload["dependencies"].append({"pip": ["example-optional[analysis]>=2"]})
    path.write_text(yaml.safe_dump(payload, sort_keys=False))
    assert audit(contract_tree) == []


def test_required_optional_provider_must_have_a_public_declaration(contract_tree):
    _replace(
        contract_tree / "devtools/dependency_contract.toml",
        'optional_required = ["mdtraj",',
        'optional_required = ["not-a-provider",',
    )
    assert any(
        "required optional dependency not-a-provider is not in runtime extras"
        == finding.message
        for finding in audit(contract_tree)
    )


@pytest.mark.parametrize("value", ['"mdtraj"', '["mdtraj", "mdtraj"]', "[false]"])
def test_invalid_optional_coverage_declarations_fail(contract_tree, value):
    _replace(
        contract_tree / "devtools/dependency_contract.toml",
        'optional_required = ["mdtraj", "pyparsing", "openmm", "pdbfixer", "mdanalysis", "rdkit", "parmed", "biopython", "nglview"]',
        f"optional_required = {value}",
    )
    assert any(
        "optional_required" in finding.message for finding in audit(contract_tree)
    )


def test_runtime_extras_cannot_disagree_about_the_same_provider(contract_tree):
    _replace(
        contract_tree / "pyproject.toml",
        "[project.optional-dependencies]",
        '[project.optional-dependencies]\nother = ["mdtraj>=1.11.2"]',
    )
    _replace(
        contract_tree / "devtools/dependency_contract.toml",
        'runtime_extras = ["soft"]',
        'runtime_extras = ["soft", "other"]',
    )
    with pytest.raises(ValueError, match="conflicting runtime optional requirements"):
        audit(contract_tree)


def test_hosted_audit_covers_dependency_only_changes():
    workflow = yaml.safe_load(
        (ROOT / ".github/workflows/ci-dependency-contract.yaml").read_text(
            encoding="utf-8"
        )
    )
    triggers = workflow.get("on", workflow.get(True))
    required_paths = {
        "pyproject.toml",
        "molsysmt/_depdigest.py",
        "devtools/controlled_sources.txt",
        "devtools/dependency_contract.toml",
        "devtools/conda-build/**",
        "devtools/rattler-build/**",
        "devtools/conda-envs/**",
        "devtools/scripts/audit_dependency_contract.py",
        ".github/workflows/**",
    }
    for event in ("push", "pull_request"):
        assert required_paths <= set(triggers[event]["paths"])
    assert any(
        step.get("run") == "python devtools/scripts/audit_dependency_contract.py"
        for step in workflow["jobs"]["audit"]["steps"]
    )


def test_conda_recipe_cannot_omit_a_public_runtime_dependency(contract_tree):
    path = contract_tree / "devtools/rattler-build/recipe.yaml"
    _replace(path, "    - py-mmcif >=1.1.1\n", "")

    assert any(
        finding.path == "devtools/rattler-build/recipe.yaml"
        and finding.message == "missing mmcif>=1.1.1"
        for finding in audit(contract_tree)
    )


def test_unbounded_conda_environment_cannot_hide_a_public_floor(contract_tree):
    path = contract_tree / "devtools/conda-envs/test_env.yaml"
    _replace(path, "- numpy >=1.26", "- numpy")

    assert any(
        finding.path == "devtools/conda-envs/test_env.yaml"
        and "numpy declares (unbounded)" in finding.message
        for finding in audit(contract_tree)
    )


def test_workflow_must_actually_install_its_declared_source_overlay(contract_tree):
    path = contract_tree / ".github/workflows/benchmarks.yml"
    _replace(
        path,
        "-r devtools/controlled_sources.txt",
        "-r devtools/unused.txt",
    )

    assert any(
        finding.path == ".github/workflows/benchmarks.yml"
        and "omits controlled source install" in finding.message
        for finding in audit(contract_tree)
    )


def test_a_second_hardcoded_sibling_sha_is_rejected(contract_tree):
    path = contract_tree / ".github/workflows/ci-rust-wheels.yaml"
    workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
    job = next(iter(workflow["jobs"].values()))
    job["steps"].append(
        {
            "name": "Duplicate old source install",
            "run": "python -m pip install git+https://github.com/uibcdf/pyunitwizard@"
            + "a" * 40,
        }
    )
    path.write_text(yaml.safe_dump(workflow, sort_keys=False), encoding="utf-8")

    assert any(
        finding.path == ".github/workflows/ci-rust-wheels.yaml"
        and "pyunitwizard repeats a controlled SHA" in finding.message
        for finding in audit(contract_tree)
    )


def test_a_new_environment_cannot_escape_inventory(contract_tree):
    path = contract_tree / "devtools/conda-envs/new_env.yaml"
    path.write_text("dependencies:\n- python\n", encoding="utf-8")

    assert any(
        finding.path == "devtools/conda-envs/new_env.yaml"
        and finding.message == "environment is not classified by the audit"
        for finding in audit(contract_tree)
    )


def test_a_new_recipe_cannot_escape_inventory(contract_tree):
    path = contract_tree / "devtools/alternate-build/recipe.yaml"
    path.parent.mkdir(parents=True)
    path.write_text(
        "requirements:\n  run:\n    - python >=3.11,<3.15\n", encoding="utf-8"
    )

    assert any(
        finding.path == "devtools/alternate-build/recipe.yaml"
        and finding.message == "Conda recipe is not classified by the audit"
        for finding in audit(contract_tree)
    )


def test_routine_viewer_sha_cannot_drift_between_workflows(contract_tree):
    path = contract_tree / ".github/workflows/benchmarks.yml"
    contract = tomllib.loads(
        (contract_tree / "devtools/dependency_contract.toml").read_text()
    )
    _replace(path, contract["routine_viewer_source"]["sha"], "b" * 40)

    assert any(
        finding.path == ".github/workflows/benchmarks.yml"
        and "routine Viewer source must be" in finding.message
        for finding in audit(contract_tree)
    )


def test_hard_form_dependency_must_be_a_public_runtime_requirement(contract_tree):
    path = contract_tree / "molsysmt/_depdigest.py"
    _replace(path, '"mdtraj": {"type": "soft"', '"mdtraj": {"type": "hard"')

    assert any(
        finding.path == "molsysmt/_depdigest.py"
        and "hard form dependency mdtraj is absent" in finding.message
        for finding in audit(contract_tree)
    )


def test_docs_extra_supplies_the_configured_theme_and_extensions():
    config = ast.parse((ROOT / "docs/conf.py").read_text())
    assignments = {
        node.targets[0].id: ast.literal_eval(node.value)
        for node in config.body
        if isinstance(node, ast.Assign)
        and isinstance(node.targets[0], ast.Name)
        and node.targets[0].id in {"extensions", "html_theme"}
    }
    dependencies = set(
        tomllib.loads((ROOT / "pyproject.toml").read_text())["project"][
            "optional-dependencies"
        ]["docs"]
    )
    modules = [assignments["html_theme"], *assignments["extensions"]]
    providers = {
        "sphinxcontrib.bibtex": "sphinxcontrib-bibtex",
        "myst_nb": "myst-nb",
    }
    for module in modules:
        local_source = ROOT / "docs" / "_ext" / module.replace(".", "/")
        if (
            local_source.with_suffix(".py").is_file()
            or (local_source / "__init__.py").is_file()
        ):
            # conf.py puts docs/_ext on sys.path: this is the delivery route,
            # not a missing third-party distribution.
            continue
        provider = (
            "sphinx"
            if module.startswith("sphinx.ext.")
            else providers.get(module, module.replace("_", "-"))
        )
        assert provider in dependencies, f"Missing documentation provider for {module}"
