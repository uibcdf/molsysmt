"""Receive MDTraj form references and distinguish declarations from operations."""

import importlib
import json
import re

import pytest

from molsysmt._private.smonitor import (
    NotImplementedIteratorError,
    NotImplementedMethodError,
)
from tests.documentation._form_reference_checks import (
    _MDTRAJ_CLASS_OPERATIONS,
    ROOT,
    _assert_native_form_reference_contract,
)


@pytest.mark.parametrize("name", tuple(_MDTRAJ_CLASS_OPERATIONS))
def test_mdtraj_tutorial_delivers_every_reviewed_hook_and_converter(name):
    _assert_native_form_reference_contract(name)


@pytest.mark.parametrize("name", tuple(_MDTRAJ_CLASS_OPERATIONS))
def test_mdtraj_tutorial_declarations_match_the_adapter(name):
    page = ROOT / f"docs/content/user/tools/form/class/mdtraj/{name}.ipynb"
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


@pytest.mark.parametrize("name", ["mdtraj_Topology", "mdtraj_Trajectory"])
@pytest.mark.parametrize(
    "operation", ["add", "merge", "append_structures", "iterators"]
)
def test_resident_mdtraj_unavailable_hooks_match_the_documented_limits(
    name, operation, mdtraj_selection_ensemble
):
    item = mdtraj_selection_ensemble
    if name == "mdtraj_Topology":
        item = item.topology
    module = importlib.import_module(f"molsysmt.form.{name}")
    assert module.is_form(item)
    if operation == "iterators":
        iterator_class = (
            module.TopologyIterator
            if name == "mdtraj_Topology"
            else module.StructuresIterator
        )
        with pytest.raises(NotImplementedIteratorError):
            next(iterator_class(item))
    else:
        arguments = ([item],) if operation == "merge" else (item, item)
        with pytest.raises(NotImplementedMethodError):
            getattr(module, operation)(*arguments, skip_digestion=True)
