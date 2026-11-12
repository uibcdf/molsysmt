"""Match the native Topology tutorial to real stable-inventory capabilities."""

import importlib
import json
import re
from pathlib import Path

import pytest

from molsysmt.native import Topology
from tests.documentation._form_reference_checks import (
    _assert_native_form_reference_contract,
)

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "docs/content/user/tools/form/class/molsysmt/molsysmt_Topology.ipynb"


def test_topology_tutorial_attributes_are_the_actual_inventory_declarations():
    notebook = json.loads(PAGE.read_text())
    table = "".join(notebook["cells"][2]["source"])
    rows = "\n".join(line for line in table.splitlines() if line.startswith("|"))
    listed = set(re.findall(r"`([a-z][a-z_]+)`", rows))
    adapter = importlib.import_module("molsysmt.form.molsysmt_Topology")
    actual = {name for name, enabled in adapter.attributes.items() if enabled}
    assert listed == actual
    count = re.findall(r"\*\*(\d+) attributes\*\*", table)
    assert count == [str(len(actual))]
    topology = Topology(n_atoms=2)
    assert not any(
        hasattr(topology, name) for name in ["bonds", "components", "chemical_states"]
    )
    for attribute in ["formal_charge", "n_bonds", "component_index"]:
        assert not adapter.has_attribute(topology, attribute, include_none=True)


def test_topology_tutorial_function_targets_really_exist():
    _assert_native_form_reference_contract("Topology")


@pytest.mark.parametrize(
    "operation", ["add", "append_structures", "get_structural_attributes"]
)
def test_topology_tutorial_marks_unavailable_operations(operation):
    adapter = importlib.import_module("molsysmt.form.molsysmt_Topology")
    topology = Topology(n_atoms=2)
    notebook = json.loads(PAGE.read_text())
    source = "".join(notebook["cells"][3]["source"])
    rows = [
        line
        for line in source.splitlines()
        if line.startswith("|") and re.search(rf"[./]{operation}[.`]", line)
    ]
    assert len(rows) == 1
    description = rows[0].split("|")[2].strip()
    if operation == "add":
        from molsysmt._private.smonitor import NotImplementedMethodError

        with pytest.raises(NotImplementedMethodError):
            adapter.add(topology, topology)
    elif operation == "append_structures":
        with pytest.raises(NotImplementedError):
            adapter.append_structures(topology)
    else:
        from molsysmt._private.smonitor import NotWithThisFormError

        getters = importlib.import_module(
            "molsysmt.form.molsysmt_Topology.get_structural_attributes"
        )
        with pytest.raises(NotWithThisFormError):
            getters.get_n_structures_from_system(topology)
    assert description.startswith("Unavailable:"), description


def test_topology_tutorial_actual_usage_keeps_inventory_and_chunk_indices():
    notebook = json.loads(PAGE.read_text())
    source = "\n".join("".join(cell["source"]) for cell in notebook["cells"])
    blocks = re.findall(r"```python\n(.*?)\n```", source, re.S)
    assert len(blocks) == 1
    namespace = {}
    exec(compile(blocks[0], str(PAGE), "exec"), namespace)
    molsys = namespace["molsys"]
    assert molsys.n_atoms == 3
    assert namespace["chunks"] == [[0, 1], [2]]
    assert not any(
        hasattr(molsys, name) for name in ["bonds", "components", "chemical_states"]
    )
