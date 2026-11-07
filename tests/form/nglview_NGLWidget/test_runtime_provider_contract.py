"""Grounding optional HTML export in the ipywidgets8-compatible provider API."""

import tomllib
from pathlib import Path

from packaging.requirements import Requirement


def test_optional_requirement_excludes_the_legacy_widget_state_exporter():
    project = tomllib.loads(
        (Path(__file__).resolve().parents[3] / "pyproject.toml").read_text()
    )["project"]
    requirement = next(
        item
        for item in map(Requirement, project["optional-dependencies"]["soft"])
        if item.name.lower() == "nglview"
    )
    assert requirement.specifier.contains("3.0.4")
    assert requirement.specifier.contains("4.0.1")
    assert not requirement.specifier.contains("3.0.3"), (
        "Public NGLView3.0.3 uses the removed instance.widgets exporter with ipywidgets8."
    )
    assert not any(
        Requirement(raw).name.lower() == "nglview" for raw in project["dependencies"]
    )
