"""Grounding the optional sequence provider floor in the consumed alignment API."""

import tomllib
from pathlib import Path

from packaging.requirements import Requirement


def test_optional_requirement_excludes_the_missing_alignment_row_api():
    project = tomllib.loads(
        (Path(__file__).resolve().parents[3] / "pyproject.toml").read_text()
    )["project"]
    requirement = next(
        item
        for item in map(Requirement, project["optional-dependencies"]["soft"])
        if item.name.lower() == "biopython"
    )
    assert requirement.specifier.contains("1.80")
    assert requirement.specifier.contains("1.86")
    assert not requirement.specifier.contains("1.79"), (
        "Integer alignment-row access raises NotImplementedError before Biopython1.80."
    )
    assert not any(
        Requirement(raw).name.lower() == "biopython" for raw in project["dependencies"]
    )
