"""Match the native MolSys tutorial to delivered attributes and chemical ownership."""

import importlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

import pandas as pd
import pytest

import molsysmt as msm
from molsysmt.native import MolSys

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
    notebook = json.loads(PAGE.read_text())
    source = "\n".join("".join(cell["source"]) for cell in notebook["cells"])
    adapter = importlib.import_module("molsysmt.form.molsysmt_MolSys")
    directory = Path("molsysmt/form/molsysmt_MolSys")
    operations = {
        "__init__",
        "extract",
        "copy",
        "add",
        "merge",
        "append_structures",
        "add_bonds",
        "remove_bonds",
        "get_topological_attributes",
        "get_structural_attributes",
        "get_mechanical_attributes",
        "set",
        "iterators",
        "has_attribute",
        "is_form",
    }
    expected = {directory / f"{name}.py" for name in operations}
    expected.update(
        directory / f"{value if isinstance(value, str) else value.__name__}.py"
        for value in adapter._convert_to.values()
    )
    conversions = "".join(notebook["cells"][4]["source"])
    listed = set(re.findall(r"^\| `([^`]+)` \|", conversions, re.M))
    assert listed == set(adapter._convert_to)
    assert re.findall(
        r"\*\*(\d+) registered direct conversion routes\*\*", conversions
    ) == [str(len(adapter._convert_to))]
    observed = set()
    for url in re.findall(
        r"\]\((https://github.com/uibcdf/molsysmt/blob/[^)]+)\)", source
    ):
        parsed = urlsplit(url)
        parts = parsed.path.split("/")
        assert re.fullmatch(r"[a-f0-9]{40}", parts[4])
        path = Path(*parts[5:])
        assert path in expected and (ROOT / path).is_file()
        line = re.fullmatch(r"L([1-9][0-9]*)", parsed.fragment)
        assert line is not None
        assert int(line[1]) <= len((ROOT / path).read_text().splitlines())
        observed.add(path)
    assert observed == expected
    assert not re.search(r"\{(?:func|mod)\}`~?molsysmt\.form\.molsysmt_MolSys", source)
