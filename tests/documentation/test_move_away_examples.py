"""Execute placement examples as written, using local systems and numeric checks."""

import json
import re
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("units", [["nm", "ps"], ["pm", "fs"]])
def test_placement_recipe_preserves_centers_modes_and_ownership(units):
    text = (ROOT / "docs/content/user/cookbook/placing_selected_centers.md").read_text()
    blocks = re.findall(r"```python\n(.*?)```", text, re.DOTALL)
    assert blocks
    namespace = {}
    with msm.pyunitwizard.context(standard_units=units):
        for block in blocks:
            exec(compile(block, "placing_selected_centers.md", "exec"), namespace)
        expected_x = {
            "molsys_centered": [2, 4, 1, 3],
            "molsys_incremented": [2, 4, 12, 14],
            "molsys_offset": [2, 4, 4, 6],
            "molsys_reflected": [2, 4, -4, -6],
            "molsys_restored": [2, 4, 10, 12],
        }
        for name, values in expected_x.items():
            observed = msm.get(namespace[name], element="atom", coordinates=True)
            np.testing.assert_allclose(
                msm.pyunitwizard.get_value(observed, to_unit="nm")[0, :, 0],
                values,
                rtol=0,
                atol=1e-12,
            )
        rotated = msm.get(namespace["molsys_rotated"], element="atom", coordinates=True)
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(rotated, to_unit="nm"),
            [[[2, 0, 0], [4, 0, 0], [11, -1, 0], [11, 1, 0]]],
            rtol=0,
            atol=1e-12,
        )
        original = msm.get(namespace["molsys"], element="atom", coordinates=True)
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(original, to_unit="nm"),
            [[[2, 0, 0], [4, 0, 0], [10, 0, 0], [12, 0, 0]]],
            rtol=0,
            atol=1e-12,
        )
        snapshot = namespace["original_coordinates"]
        np.testing.assert_array_equal(
            msm.pyunitwizard.get_value(
                original, to_unit=msm.pyunitwizard.get_unit(snapshot)
            ),
            msm.pyunitwizard.get_value(snapshot),
        )


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
