"""Receive Biopython adapter references and actual operation availability."""

import importlib
import json
import re

import pytest

from molsysmt._private.smonitor import (
    NotImplementedIteratorError,
    NotImplementedMethodError,
)
from tests.documentation._form_reference_checks import (
    _EXTERNAL_CLASS_OPERATIONS,
    ROOT,
    _assert_native_form_reference_contract,
)


@pytest.mark.parametrize("name", tuple(_EXTERNAL_CLASS_OPERATIONS))
def test_biopython_tutorial_delivers_every_reviewed_hook_and_converter(name):
    _assert_native_form_reference_contract(name)


@pytest.mark.parametrize("name", tuple(_EXTERNAL_CLASS_OPERATIONS))
def test_biopython_tutorial_declarations_match_the_adapter(name):
    page = ROOT / f"docs/content/user/tools/form/class/biopython/{name}.ipynb"
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


@pytest.mark.parametrize("name", ["biopython_Seq", "biopython_SeqRecord"])
@pytest.mark.parametrize("operation", ["add", "merge", "iterators"])
def test_biopython_sequence_unavailable_hooks_are_explicit(name, operation):
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord

    item = Seq("AGX") if name == "biopython_Seq" else SeqRecord(Seq("AGX"))
    module = importlib.import_module(f"molsysmt.form.{name}")
    assert module.is_form(item)
    if operation == "iterators":
        with pytest.raises(NotImplementedIteratorError):
            module.TopologyIterator(item, skip_digestion=True)
    else:
        arguments = (item, item) if operation == "add" else ([item, item],)
        with pytest.raises(NotImplementedMethodError):
            getattr(module, operation)(*arguments, skip_digestion=True)
    page = ROOT / f"docs/content/user/tools/form/class/biopython/{name}.ipynb"
    operations = "".join(json.loads(page.read_text())["cells"][3]["source"])
    row = next(line for line in operations.splitlines() if f"/{operation}.py#L" in line)
    assert "Unavailable" in row
