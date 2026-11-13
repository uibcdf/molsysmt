"""Receive MDAnalysis form references and distinguish declarations from operations."""

import importlib
import json
import re

import pytest

from tests.documentation._form_reference_checks import (
    _MDANALYSIS_CLASS_OPERATIONS,
    ROOT,
    _assert_native_form_reference_contract,
)


@pytest.mark.parametrize("name", tuple(_MDANALYSIS_CLASS_OPERATIONS))
def test_mdanalysis_tutorial_delivers_every_reviewed_hook_and_converter(name):
    _assert_native_form_reference_contract(name)


@pytest.mark.parametrize("name", tuple(_MDANALYSIS_CLASS_OPERATIONS))
def test_mdanalysis_tutorial_declarations_match_the_adapter(name):
    page = ROOT / f"docs/content/user/tools/form/class/mdanalysis/{name}.ipynb"
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


def test_declared_conversion_cannot_be_delivered_by_an_empty_setter_module(monkeypatch):
    from pathlib import Path

    adapter = importlib.import_module("molsysmt.form.MDAnalysis_Topology")
    page = (
        ROOT / "docs/content/user/tools/form/class/mdanalysis/MDAnalysis_Topology.ipynb"
    )
    notebook = json.loads(page.read_text())
    source = "".join(notebook["cells"][3]["source"])
    empty_module_url = re.search(
        r"\]\((https://github.com/uibcdf/molsysmt/blob/[^)]+/set\.py)\)", source
    )[1]
    routes = {**adapter._convert_to, "file:unavailable": "set"}
    conversions = "".join(notebook["cells"][4]["source"])
    conversions = conversions.replace("**3 registered", "**4 registered")
    conversions += f"| `file:unavailable` | `file` | [set]({empty_module_url}) |\n"
    notebook["cells"][4]["source"] = conversions.splitlines(keepends=True)
    original_read = Path.read_text

    def read_text(path, *args, **kwargs):
        if path == page:
            return json.dumps(notebook)
        return original_read(path, *args, **kwargs)

    monkeypatch.setattr(adapter, "_convert_to", routes)
    monkeypatch.setattr(Path, "read_text", read_text)
    with pytest.raises(AssertionError, match="empty module cannot deliver a converter"):
        _assert_native_form_reference_contract("MDAnalysis_Topology")
