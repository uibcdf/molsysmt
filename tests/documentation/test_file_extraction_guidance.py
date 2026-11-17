"""Execute the stored-coordinate recipe with source and unit-policy controls."""

import re
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.session_files import discard_copy

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("length_unit,time_unit", [("nm", "ps"), ("pm", "fs")])
def test_complete_copy_recipe_keeps_bytes_and_native_geometry_independent(
    length_unit, time_unit
):
    page = ROOT / "docs/content/user/cookbook/copying_disk_systems.md"
    blocks = re.findall(r"^```python\n(.*?)^```", page.read_text(), re.M | re.S)
    namespace = {}
    try:
        with msm.pyunitwizard.context(
            standard_units=[length_unit, time_unit, "radians", "elementary_charge"]
        ):
            for block in blocks:
                exec(compile(block, str(page), "exec"), namespace)
            original = msm.pyunitwizard.get_value(
                namespace["molsys"].structures.coordinates, to_unit="nm"
            )
            edited = msm.pyunitwizard.get_value(
                namespace["molsys_working"].structures.coordinates, to_unit="nm"
            )
            expected = np.zeros_like(original)
            expected[0, 0, 0] = 1
            np.testing.assert_allclose(edited - original, expected, atol=1e-15)
            assert namespace["restored"].coordinates.shape == (2, 2, 3)
    finally:
        for name in ("automatic", "whole", "selected"):
            if isinstance(namespace.get(name), str):
                discard_copy(namespace[name])


@pytest.mark.parametrize("length_unit,time_unit", [("nm", "ps"), ("pm", "fs")])
def test_stored_coordinate_recipe_preserves_source_and_independent_outputs(
    length_unit, time_unit
):
    source = (ROOT / "docs/content/user/cookbook/copying_disk_systems.md").read_text()
    section = source.split("## Extracting stored coordinates safely\n", 1)[1].split(
        "\n## ", 1
    )[0]
    blocks = re.findall(r"```python\n(.*?)\n```", section, re.S)
    assert len(blocks) == 1
    namespace = {}
    try:
        with msm.pyunitwizard.context(
            standard_units=[length_unit, time_unit, "radians", "elementary_charge"]
        ):
            exec(
                compile(
                    blocks[0],
                    "copying_disk_systems.md#extracting-stored-coordinates-safely",
                    "exec",
                ),
                namespace,
            )
    finally:
        for name in ("whole", "selected"):
            if name in namespace:
                discard_copy(namespace[name])
