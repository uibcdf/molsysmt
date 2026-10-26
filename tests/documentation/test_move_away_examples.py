"""Execute placement examples as written, using local systems and numeric checks."""

import json
import re
from pathlib import Path

import numpy as np

import molsysmt as msm

ROOT = Path(__file__).resolve().parents[2]


def test_placement_recipe_preserves_centers_modes_and_ownership():
    text = (ROOT / "docs/content/user/cookbook/placing_selected_centers.md").read_text()
    blocks = re.findall(r"```python\n(.*?)```", text, re.DOTALL)
    assert len(blocks) == 4
    namespace = {}
    for block in blocks:
        exec(compile(block, "placing_selected_centers.md", "exec"), namespace)


def test_course_displacement_modes_and_no_write_rejection():
    path = ROOT / "docs/content/course/Common_Core/16_Structural_Operations.ipynb"
    notebook = json.loads(path.read_text())
    source = msm.convert(
        msm.systems["T4 lysozyme L99A"]["181l.bcif.gz"], to_form="molsysmt.MolSys"
    )
    centered = msm.structure.center(source)
    shifted = msm.structure.translate(centered, translation="[1, 0, 0] nm")
    namespace = {
        "msm": msm,
        "np": np,
        "lysozyme_centered": centered,
        "lysozyme_shifted": shifted,
    }
    cells = [
        cell
        for cell in notebook["cells"]
        if "move-away-contract" in cell.get("metadata", {}).get("tags", [])
    ]
    assert len(cells) == 1
    exec(compile("".join(cells[0]["source"]), str(path), "exec"), namespace)


def test_course_reflection_default_scaling_and_inverse():
    path = ROOT / "docs/content/course/Common_Core/16_Structural_Operations.ipynb"
    notebook = json.loads(path.read_text())
    source = msm.convert(
        msm.systems["T4 lysozyme L99A"]["181l.bcif.gz"], to_form="molsysmt.MolSys"
    )
    namespace = {
        "msm": msm,
        "np": np,
        "lysozyme_centered": msm.structure.center(source),
    }
    cells = [
        cell
        for cell in notebook["cells"]
        if "reflection-contract" in cell.get("metadata", {}).get("tags", [])
    ]
    assert len(cells) == 1
    exec(compile("".join(cells[0]["source"]), str(path), "exec"), namespace)
