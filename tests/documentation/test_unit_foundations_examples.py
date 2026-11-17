"""Check the documented physical equivalence and scoped output policy."""

import re
from pathlib import Path

import numpy as np

import molsysmt as msm


def test_unit_foundations_examples_keep_physics_and_restore_application_policy():
    page = (
        Path(__file__).resolve().parents[2]
        / "docs/content/user/foundations/governance/quantities_and_units.md"
    )
    blocks = re.findall(r"^```python\n(.*?)^```", page.read_text(), re.M | re.S)
    puw = msm.pyunitwizard
    with puw.context(
        default_form="pint",
        default_parser="pint",
        standard_units=["pm", "fs", "degrees", "elementary_charge"],
    ):
        namespace = {}
        for block in blocks:
            exec(compile(block, str(page), "exec"), namespace)
        assert puw.get_form(namespace["after_context"]) == "pint"
        assert puw.get_unit(namespace["after_context"]) == puw.unit("pm")
        np.testing.assert_array_equal(
            puw.get_value(namespace["after_context"], to_unit="nm"),
            [np.diag([2.0, 3.0, 4.0])],
        )
