"""Require an optional MDAnalysis baseline compatible with NumPy2 and explicit guessing."""

import tomllib
from pathlib import Path

from packaging.requirements import Requirement


def test_optional_requirement_excludes_the_pre_numpy2_binary_baseline():
    project = tomllib.loads(
        (Path(__file__).resolve().parents[3] / "pyproject.toml").read_text()
    )["project"]
    requirement = next(
        item
        for item in map(Requirement, project["optional-dependencies"]["soft"])
        if item.name.lower() == "mdanalysis"
    )
    assert requirement.specifier.contains("2.8.0")
    assert requirement.specifier.contains("2.10.0")
    assert not requirement.specifier.contains("2.7.0"), (
        "The public2.7 wheel fails the NumPy2 ABI;2.8 publishes compatible "
        "binaries and supports the explicit to_guess topology-construction boundary."
    )
    assert not any(
        Requirement(raw).name.lower() == "mdanalysis" for raw in project["dependencies"]
    )
