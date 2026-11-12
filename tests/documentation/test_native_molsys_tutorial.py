"""Match the native MolSys tutorial to delivered attributes and chemical ownership."""

import importlib
import json
import re
from pathlib import Path

import pandas as pd
import pytest

import molsysmt as msm
from molsysmt.native import MolSys
from tests.documentation._form_reference_checks import (
    _assert_native_form_reference_contract,
)

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "docs/content/user/tools/form/class/molsysmt/molsysmt_MolSys.ipynb"


def test_molsys_tutorial_lists_the_complete_native_attribute_contract():
    notebook = json.loads(PAGE.read_text())
    text = "".join(notebook["cells"][2]["source"])
    rows = "\n".join(line for line in text.splitlines() if line.startswith("|"))
    listed = set(re.findall(r"`([a-z][a-z_]+)`", rows))
    adapter = importlib.import_module("molsysmt.form.molsysmt_MolSys")
    actual = {name for name, supported in adapter.attributes.items() if supported}
    assert listed == actual
    assert re.findall(r"\*\*(\d+) attributes\*\*", text) == [str(len(actual))]


def test_documented_explicit_hydrogens_are_stored_counts_not_atom_recounting():
    molsys = MolSys(n_atoms=3)
    assert molsys.get(element="atom", n_explicit_hydrogens=True) is None
    msm.set(molsys, element="atom", n_explicit_hydrogens=[0, 1, None])
    assert molsys.get(
        element="atom", selection=[2, 0, 1, 1], n_explicit_hydrogens=True
    ) == [None, 0, 1, 1]
    assert molsys.get(n_atoms=True, n_bonds=True) == [3, 0]
    assert molsys.get(connectivity_completeness=True) == "unavailable"


@pytest.mark.parametrize("operation", ["add_bonds", "remove_bonds"])
def test_form_bond_edit_descriptions_match_chemical_state_ownership(operation):
    notebook = json.loads(PAGE.read_text())
    text = "".join(notebook["cells"][3]["source"])
    rows = [
        line
        for line in text.splitlines()
        if line.startswith("|") and re.search(rf"[./]{operation}[.(]", line)
    ]
    assert len(rows) == 1
    description = rows[0].split("|")[2].lower()
    adapter = importlib.import_module("molsysmt.form.molsysmt_MolSys")
    molsys = MolSys(n_atoms=2)
    topology, chemistry = molsys.topology, molsys.chemical_states
    inventory = topology.atoms.copy(deep=True)
    if operation == "add_bonds":
        adapter.add_bonds(molsys, [[0, 1]])
        assert molsys.get(n_bonds=True) == 1
    else:
        chemistry.add_bonds([[0, 1]])
        adapter.remove_bonds(molsys, [0])
        assert molsys.get(n_bonds=True) == 0
    assert molsys.topology is topology and molsys.chemical_states is chemistry
    pd.testing.assert_frame_equal(topology.atoms, inventory)
    assert not hasattr(topology, "bonds")
    assert "chemical" in description and "topology" not in description
    if operation == "remove_bonds":
        assert "bond indices" in description


def test_molsys_implementation_references_cover_real_owned_source():
    _assert_native_form_reference_contract("MolSys")
