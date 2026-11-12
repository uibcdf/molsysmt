"""Execute the stored-coordinate recipe with source and unit-policy controls."""

import re
from pathlib import Path

import pytest

import molsysmt as msm
from molsysmt._private.session_files import discard_copy

ROOT = Path(__file__).resolve().parents[2]


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
