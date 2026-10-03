"""Separating indexed hydrogen neighbors from unresolved or virtual H counts."""

import numpy as np
import pandas as pd

import molsysmt as msm


def test_native_stored_inventory_separates_virtual_and_indexed_hydrogens():
    b = msm.MolSysBuilder()
    b.add_atom(atom_type="C", atom_name="C")
    b.add_atom(atom_type="H", atom_name="H")
    b.add_bond(0, 1)
    source = b.build()
    state = source.chemical_states._states[0]
    state.connectivity_completeness = "complete"
    state.bonds["bond_type"] = pd.array(["covalent"], dtype="string")
    for name, values in {
        "n_implicit_hydrogens": [2, 0],
        "n_explicit_hydrogens": [1, 0],
    }.items():
        source.topology._set_chemical_state_atom_attribute(name, values)
    result = msm.physchem.get_hydrogen_inventory(source)
    assert result["status"] == "available"
    assert result["missing_hydrogen_counts"].tolist() == [3, 0]
    assert result["indexed_hydrogen_counts"].tolist() == [1, 0]
    assert result["total_hydrogen_counts"].tolist() == [4, 0]
    assert result["parent_hydrogen_pairs"].tolist() == [[0, 1]]
    selected = msm.physchem.get_hydrogen_inventory(source, selection=[1, 1])
    assert selected["atom_indices"].tolist() == [1]
    assert selected["parent_hydrogen_pairs"].shape == (0, 2)
    empty = msm.physchem.get_hydrogen_inventory(source, selection=[])
    assert empty["status"] == "empty"
    assert empty["missing_hydrogen_counts"].dtype == np.int64
    state.atom_attributes.loc[0, "n_implicit_hydrogens"] = pd.NA
    assert msm.physchem.get_hydrogen_inventory(source)["status"] == "unassessed"
    state.atom_attributes.loc[1, "n_explicit_hydrogens"] = 1
    assert msm.physchem.get_hydrogen_inventory(source)["status"] == "conflict"


def test_sdf_counts_are_not_invented_from_explicit_neighbor_graph():
    result = msm.physchem.get_hydrogen_inventory(
        msm.systems["caffeine"]["caffeine.sdf"]
    )
    assert result["status"] == "unassessed"
    assert result["indexed_hydrogen_counts"].sum() == 10
    assert np.all(result["missing_hydrogen_counts"] == -1)
