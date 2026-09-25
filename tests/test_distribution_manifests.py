"""Testing agreement between the Python and Conda distribution manifests."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

import pytest
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

ROOT = Path(__file__).resolve().parents[1]
CONDA_TO_PYTHON_NAMES = {"py-mmcif": "mmcif"}


def _python_runtime_requirements(pyproject_text: str) -> dict[str, Requirement]:
    pyproject = tomllib.loads(pyproject_text)
    requirements = (Requirement(item) for item in pyproject["project"]["dependencies"])
    return {canonicalize_name(item.name): item for item in requirements}


def _conda_runtime_requirements(recipe_text: str) -> dict[str, Requirement]:
    match = re.search(
        r"(?m)^requirements:\n(?:.*\n)*?^  run:\n(?P<body>(?:  - [^\n]*\n)+)",
        recipe_text,
    )
    assert match is not None, "The Conda recipe has no requirements.run block"

    requirements = []
    for line in match.group("body").splitlines():
        item = line.strip().removeprefix("- ").split("#", 1)[0].strip()
        requirements.append(Requirement(item))

    return {
        CONDA_TO_PYTHON_NAMES.get(
            canonicalize_name(item.name), canonicalize_name(item.name)
        ): item
        for item in requirements
    }


def _manifest_mismatches(
    pyproject_text: str, recipe_text: str
) -> dict[str, tuple[str, str | None]]:
    python_requirements = _python_runtime_requirements(pyproject_text)
    conda_requirements = _conda_runtime_requirements(recipe_text)
    mismatches = {}

    for name, python_requirement in python_requirements.items():
        conda_requirement = conda_requirements.get(name)
        python_specifier = str(python_requirement.specifier)
        conda_specifier = (
            str(conda_requirement.specifier) if conda_requirement is not None else None
        )
        if conda_specifier != python_specifier:
            mismatches[name] = (python_specifier, conda_specifier)

    return mismatches


def test_conda_runtime_requirements_match_pyproject():
    pyproject_text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    recipe_text = (ROOT / "devtools" / "conda-build" / "meta.yaml").read_text(
        encoding="utf-8"
    )

    assert _manifest_mismatches(pyproject_text, recipe_text) == {}


def test_nglview_remains_an_optional_backend():
    pyproject_text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    recipe_text = (ROOT / "devtools" / "conda-build" / "meta.yaml").read_text(
        encoding="utf-8"
    )
    pyproject = tomllib.loads(pyproject_text)

    assert "nglview" not in _python_runtime_requirements(pyproject_text)
    assert "nglview" not in _conda_runtime_requirements(recipe_text)
    assert "nglview" in {
        canonicalize_name(Requirement(item).name)
        for item in pyproject["project"]["optional-dependencies"]["soft"]
    }


def test_mmcif_conda_alias_is_required():
    """The Conda distribution is py-mmcif, but its Python import is mmcif."""
    pyproject_text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    recipe_text = (ROOT / "devtools" / "conda-build" / "meta.yaml").read_text(
        encoding="utf-8"
    )
    assert "  - py-mmcif >=1.1.1\n" in recipe_text

    without_mmcif = recipe_text.replace("  - py-mmcif >=1.1.1\n", "", 1)
    assert _manifest_mismatches(pyproject_text, without_mmcif)["mmcif"] == (
        ">=1.1.1",
        None,
    )


@pytest.mark.parametrize(
    "dependency",
    ["argdigest", "depdigest", "numpy", "pyunitwizard", "smonitor"],
)
def test_manifest_guard_detects_a_removed_constraint(dependency):
    pyproject_text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    recipe_text = (ROOT / "devtools" / "conda-build" / "meta.yaml").read_text(
        encoding="utf-8"
    )
    mutated_recipe = re.sub(
        rf"(?m)^(  - {re.escape(dependency)})\s+[^\n]+$",
        r"\1",
        recipe_text,
        count=1,
    )

    assert mutated_recipe != recipe_text
    assert dependency in _manifest_mismatches(pyproject_text, mutated_recipe)
