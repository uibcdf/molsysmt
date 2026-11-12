"""Receive string-form references and actual declared attribute portfolios."""

import importlib
import json
import re

import pytest

from molsysmt._private.smonitor import (
    NotImplementedIteratorError,
    NotImplementedMethodError,
)
from tests.documentation._form_reference_checks import (
    _STRING_OPERATIONS,
    ROOT,
    _assert_native_form_reference_contract,
)

_SAMPLES = {
    "string_alphafold_id": "AF-P05067-F1",
    "string_amino_acids_1": "amino_acids_1:ACD",
    "string_amino_acids_3": "amino_acids_3:ALACYSASP",
    "string_pdb_id": "pdb_id:1L2Y",
    "string_pdb_text": (
        "ATOM      1  CA  ALA A   1       0.000   0.000   0.000  1.00  0.00           C  \n"
        "END\n"
    ),
    "string_smiles": "smiles:CCO",
    "string_uniprot_id": "uniprot_id:P05067",
}


@pytest.mark.parametrize("name", tuple(_STRING_OPERATIONS))
def test_string_tutorial_delivers_every_reviewed_hook_and_converter(name):
    _assert_native_form_reference_contract(name)


@pytest.mark.parametrize("name", tuple(_STRING_OPERATIONS))
def test_string_tutorial_declarations_match_the_adapter(name):
    page = ROOT / f"docs/content/user/tools/form/string/{name}.ipynb"
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


@pytest.mark.parametrize("name", tuple(_STRING_OPERATIONS))
def test_string_merge_is_documented_as_an_unavailable_hook(name):
    module = importlib.import_module(f"molsysmt.form.{name}")
    item = _SAMPLES[name]
    assert module.is_form(item)
    with pytest.raises(NotImplementedMethodError):
        module.merge([item, item], skip_digestion=True)
    page = ROOT / f"docs/content/user/tools/form/string/{name}.ipynb"
    operations = "".join(json.loads(page.read_text())["cells"][3]["source"])
    row = next(line for line in operations.splitlines() if "/merge.py#L" in line)
    assert "Unavailable" in row and "NotImplementedMethodError" in row


@pytest.mark.parametrize("name", tuple(_STRING_OPERATIONS))
def test_string_iterator_is_documented_as_unavailable(name):
    module = importlib.import_module(f"molsysmt.form.{name}.iterators")
    item = _SAMPLES[name]
    assert importlib.import_module(f"molsysmt.form.{name}").is_form(item)
    with pytest.raises(NotImplementedIteratorError):
        next(module.TopologyIterator(item))
    page = ROOT / f"docs/content/user/tools/form/string/{name}.ipynb"
    operations = "".join(json.loads(page.read_text())["cells"][3]["source"])
    row = next(line for line in operations.splitlines() if "/iterators.py#L" in line)
    assert "Unavailable" in row and "NotImplementedIteratorError" in row
