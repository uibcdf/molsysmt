"""Executing public graph examples with independent expected partitions."""

import re
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm


def execute_page(name):
    page = (
        Path(__file__).resolve().parents[2]
        / "docs/content/user/tools/chemical_states"
        / name
    )
    blocks = re.findall(r"```python\n(.*?)```", page.read_text(), re.S)
    assert len(blocks) == 1
    namespace = {}
    for block in blocks:
        exec(compile(block, str(page), "exec"), namespace)
    return namespace


def test_rigid_fragment_tutorial_uses_complete_public_chemical_state():
    namespace = execute_page("get_rigid_fragments.md")
    molsys, fragments = namespace["molsys"], namespace["fragments"]
    assert isinstance(molsys, msm.ChemicalStates)
    assert molsys.get(n_atoms=True, n_bonds=True, connectivity_completeness=True) == [
        4,
        3,
        "complete",
    ]
    expected = {
        "fragment_atom_indices": [0, 1, 2, 3],
        "fragment_offsets": [0, 2, 4],
        "atom_fragment_indices": [0, 0, 1, 1],
        "bond_indices": [1],
        "bonded_atom_pairs": [[1, 2]],
        "fragment_pairs": [[0, 1]],
    }
    for name, values in expected.items():
        np.testing.assert_array_equal(fragments[name], values)
        assert fragments[name].dtype == np.int64
    assert molsys.get_bonds()[["atom1_index", "atom2_index"]].values.tolist() == [
        [0, 1],
        [1, 2],
        [2, 3],
    ]


def test_chemical_states_portal_example_preserves_state_inventory():
    namespace = execute_page("index.md")
    assert namespace["restored"].n_chemical_states == 1


def test_rotatable_bond_tutorial_preserves_restricted_and_broader_partitions():
    pytest.importorskip("rdkit.Chem")
    namespace = execute_page("get_rotatable_bonds.md")
    assert namespace["result"]["rotatable_bonded_atom_pairs"].tolist() == [[3, 4]]
    assert namespace["broader"]["rotatable_bonded_atom_pairs"].tolist() == [
        [1, 3],
        [3, 4],
    ]
    assert namespace["fragments"]["fragment_atom_indices"].tolist() == list(range(6))
    assert namespace["fragments"]["fragment_offsets"].tolist() == [0, 4, 6]
