"""Ground the optional ParmEd floor in consumed NumPy array and import boundaries."""

import tomllib
from pathlib import Path

from packaging.requirements import Requirement


def test_optional_requirement_excludes_known_numpy2_incompatibilities():
    project = tomllib.loads(
        (Path(__file__).resolve().parents[3] / "pyproject.toml").read_text()
    )["project"]
    requirement = next(
        item
        for item in map(Requirement, project["optional-dependencies"]["soft"])
        if item.name.lower() == "parmed"
    )
    assert requirement.specifier.contains("4.3.1")
    for version in ("4.0.0", "4.3.0"):
        assert not requirement.specifier.contains(version), (
            "Consumed coordinates/box setters fail on NumPy2 in4.0; "
            "4.3.0 imports the removed numpy.compat module with NumPy>=2.3."
        )
    assert not any(
        Requirement(raw).name.lower() == "parmed" for raw in project["dependencies"]
    )
