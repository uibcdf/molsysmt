"""Receive intended file-adapter references and current declaration portfolios."""

import importlib
import json
import re
from pathlib import Path

import pytest

from tests.documentation._form_reference_checks import (
    _FILE_OPERATIONS,
    ROOT,
    _assert_native_form_reference_contract,
)


@pytest.mark.parametrize("name", tuple(_FILE_OPERATIONS))
def test_file_tutorial_delivers_every_reviewed_hook_and_converter(name):
    _assert_native_form_reference_contract(name)


@pytest.mark.parametrize("name", tuple(_FILE_OPERATIONS))
def test_file_tutorial_declarations_match_the_adapter(name):
    page = ROOT / "docs/content/user/tools/form/file" / f"{name}.ipynb"
    source = "".join(json.loads(page.read_text())["cells"][2]["source"])
    rows = "\n".join(line for line in source.splitlines() if line.startswith("|"))
    attributes = importlib.import_module(f"molsysmt.form.{name}").attributes
    declared = {attribute for attribute, flag in attributes.items() if flag}
    assert set(re.findall(r"`([^`]+)`", rows)) == declared
    assert re.findall(r"\*\*(\d+) (?:declared )?attributes\*\*", source) == [
        str(len(declared))
    ]


def test_file_reference_guard_rejects_function_link_to_module_header(monkeypatch):
    page = ROOT / "docs/content/user/tools/form/file/file_gro.ipynb"
    original = Path.read_text
    text = original(page)
    altered, count = re.subn(r"(/file_gro/extract\.py#)L\d+", r"\g<1>L1", text)
    assert count and altered != text

    def read_text(path, *args, **kwargs):
        return altered if path == page else original(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", read_text)
    with pytest.raises(AssertionError):
        _assert_native_form_reference_contract("file_gro")
