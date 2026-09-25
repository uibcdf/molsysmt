"""Regression tests for the read-only dependency-route auditor."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

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
    _replace(path, "- numpy >=1.26,<3", "- numpy")

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
    _replace(
        path,
        "      - name: Install the MolSysMT wheel without dependency resolution",
        "      - name: Duplicate old source install\n"
        "        run: python -m pip install git+https://github.com/uibcdf/pyunitwizard@"
        + "a" * 40
        + "\n\n      - name: Install the MolSysMT wheel without dependency resolution",
    )

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
    _replace(path, "7a1522662e30575caf580a9447e3e6d80b628e07", "b" * 40)

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
