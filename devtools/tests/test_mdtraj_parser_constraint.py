"""Protecting the optional parser exclusion without raising Python's floor."""

import tomllib
from pathlib import Path

import pytest
import yaml
from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("surface", ["soft", "development_env.yaml", "test_env.yaml"])
def test_optional_mdtraj_routes_reject_the_demonstrated_parser_regression(surface):
    if surface == "soft":
        data = tomllib.loads((ROOT / "pyproject.toml").read_text())
        requirements = [
            Requirement(value)
            for value in data["project"]["optional-dependencies"]["soft"]
        ]
        specifier = next(
            value.specifier for value in requirements if value.name == "pyparsing"
        )
    else:
        data = yaml.safe_load((ROOT / "devtools/conda-envs" / surface).read_text())
        dependency = next(
            value
            for value in data["dependencies"]
            if isinstance(value, str) and value.split()[0] == "pyparsing"
        )
        specifier = SpecifierSet(dependency.split(maxsplit=1)[1])
    assert "3.3.3" not in specifier
    assert "3.2.5" in specifier
    assert "3.3.2" in specifier
