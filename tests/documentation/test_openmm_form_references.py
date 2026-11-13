"""Receive OpenMM form links, actual declarations and explicit refusals."""

import importlib
import json
import re
from pathlib import Path

import pytest

from molsysmt._private.smonitor import (
    NotImplementedIteratorError,
    NotImplementedMethodError,
)
from tests.documentation._form_reference_checks import (
    _OPENMM_CLASS_OPERATIONS,
    ROOT,
    _assert_native_form_reference_contract,
)


@pytest.mark.parametrize("name", tuple(_OPENMM_CLASS_OPERATIONS))
def test_openmm_tutorial_delivers_every_reviewed_hook_and_converter(name):
    _assert_native_form_reference_contract(name)


@pytest.mark.parametrize("name", tuple(_OPENMM_CLASS_OPERATIONS))
def test_openmm_tutorial_declarations_match_the_adapter(name):
    page = ROOT / f"docs/content/user/tools/form/class/openmm/{name}.ipynb"
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


@pytest.mark.parametrize(
    "name", ["openmm_PDBFile", "openmm_Modeller", "openmm_State", "openmm_System"]
)
@pytest.mark.parametrize(
    "operation", ["add", "merge", "append_structures", "iterators"]
)
def test_openmm_unavailable_hooks_match_actual_refusals(name, operation, request):
    from openmm import System
    from openmm.app import Modeller

    if name == "openmm_State":
        item = request.getfixturevalue("openmm_position_snapshot")
    elif name == "openmm_System":
        item = System()
        item.addParticle(12)
    else:
        pdb = request.getfixturevalue("openmm_pdb_ensemble")
        item = (
            pdb if name == "openmm_PDBFile" else Modeller(pdb.topology, pdb.positions)
        )
    module = importlib.import_module(f"molsysmt.form.{name}")
    assert module.is_form(item)
    if operation == "iterators":
        with pytest.raises(NotImplementedIteratorError):
            next(module.TopologyIterator(item))
    else:
        arguments = (
            (item, item) if operation in ["add", "append_structures"] else ([item],)
        )
        with pytest.raises(NotImplementedMethodError):
            getattr(module, operation)(*arguments, skip_digestion=True)
    page = ROOT / f"docs/content/user/tools/form/class/openmm/{name}.ipynb"
    operations = "".join(json.loads(page.read_text())["cells"][3]["source"])
    row = next(line for line in operations.splitlines() if f"/{operation}.py#L" in line)
    assert "Unavailable" in row


def test_reference_receiving_rejects_invented_line_in_empty_module(monkeypatch):
    page = ROOT / "docs/content/user/tools/form/class/openmm/openmm_System.ipynb"
    original = Path.read_text
    text = original(page)
    altered = text.replace("/openmm_System/set.py)", "/openmm_System/set.py#L1)")
    assert altered != text
    monkeypatch.setattr(
        Path,
        "read_text",
        lambda path, *args, **kwargs: (
            altered if path == page else original(path, *args, **kwargs)
        ),
    )
    with pytest.raises(AssertionError):
        _assert_native_form_reference_contract("openmm_System")


def test_reference_receiving_requires_a_real_callable_anchor(monkeypatch):
    page = ROOT / "docs/content/user/tools/form/class/openmm/openmm_System.ipynb"
    original = Path.read_text
    text = original(page)
    altered, count = re.subn(r"(/openmm_System/to_openmm_System.py)#L\d+", r"\1", text)
    assert count and altered != text
    monkeypatch.setattr(
        Path,
        "read_text",
        lambda path, *args, **kwargs: (
            altered if path == page else original(path, *args, **kwargs)
        ),
    )
    with pytest.raises(AssertionError):
        _assert_native_form_reference_contract("openmm_System")
