"""Receive RDKit, OpenFF and ParmEd form references and distinguish declarations from operations."""

import importlib
import json
import re

import pytest

from tests.documentation._form_reference_checks import (
    _CHEMICAL_CLASS_OPERATIONS,
    ROOT,
    _assert_native_form_reference_contract,
)


@pytest.mark.parametrize("name", tuple(_CHEMICAL_CLASS_OPERATIONS))
def test_chemical_form_tutorial_delivers_every_reviewed_hook_and_converter(name):
    _assert_native_form_reference_contract(name)


@pytest.mark.parametrize("name", tuple(_CHEMICAL_CLASS_OPERATIONS))
def test_chemical_form_tutorial_declarations_match_the_adapter(name):
    page = (
        ROOT
        / f"docs/content/user/tools/form/class/{name.split('_', 1)[0]}/{name}.ipynb"
    )
    source = "".join(json.loads(page.read_text())["cells"][2]["source"])
    rows = "\n".join(line for line in source.splitlines() if line.startswith("|"))
    declared = {
        key
        for key, flag in importlib.import_module(
            f"molsysmt.form.{name}"
        ).attributes.items()
        if flag
    }
    assert set(re.findall(r"`([^`]+)`", rows)) == declared
    assert re.findall(r"\*\*(\d+) (?:declared )?attributes\*\*", source) == [
        str(len(declared))
    ]
