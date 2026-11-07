"""Regression tests for the read-only dependency-route auditor."""

from __future__ import annotations

import ast
import shutil
import tomllib
from pathlib import Path

import pytest
import yaml

from devtools.scripts.audit_dependency_contract import audit

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


def test_current_dependency_routes_are_coherent():
    assert audit(ROOT) == []


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
    pip = next(
        item["pip"] for item in payload["dependencies"] if isinstance(item, dict)
    )
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
    _replace(
        contract_tree / "devtools/conda-envs/test_env.yaml",
        "  - pytraj",
        "  - pytraj\n  - example-optional[analysis]>=2",
    )
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
        'optional_required = ["mdtraj", "pyparsing", "openmm", "pdbfixer", "rdkit", "openff-toolkit", "openff-units"]',
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
