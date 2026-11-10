"""Closed-form endpoints of a declared nine-node backbone graph."""

import numpy as np
import pytest

import molsysmt as msm


def _path():
    builder = msm.MolSysBuilder()
    for group in range(3):
        indices = [
            builder.add_atom(atom_name=name, atom_type=element)
            for name, element in [("N", "N"), ("CA", "C"), ("C", "C")]
        ]
        builder.add_group(indices, group_name="GLY", group_id=["z", "a", "x"][group])
        builder.add_bond(indices[0], indices[1])
        builder.add_bond(indices[1], indices[2])
    builder.add_chain([1, 2, 0], chain_id="A")
    builder.add_bond(5, 6)
    builder.add_bond(8, 0)
    return builder.build()


def test_declared_path_endpoints_are_not_inventory_or_id_order():
    molsys = _path()
    report = msm.chemical_states.get_peptide_termini(molsys)
    np.testing.assert_array_equal(report["chains"][0]["group_indices"], [1, 2, 0])
    np.testing.assert_array_equal(report["n_terminal_group_indices"], [1])
    np.testing.assert_array_equal(report["c_terminal_group_indices"], [0])
    msm.set(molsys, element="group", group_id=["12A", "-1", "anything"])
    renamed = msm.chemical_states.get_peptide_termini(molsys)
    np.testing.assert_array_equal(renamed["n_terminal_group_indices"], [1])
    np.testing.assert_array_equal(renamed["c_terminal_group_indices"], [0])


def test_closing_the_declared_path_gives_no_free_endpoints():
    molsys = _path()
    molsys.chemical_states.add_bonds([[2, 3]])
    report = msm.chemical_states.get_peptide_termini(molsys)
    assert report["chains"][0]["cyclic"]
    assert report["n_terminal_group_indices"].shape == (0,)
    assert report["c_terminal_group_indices"].shape == (0,)


def test_a_missing_declared_link_is_unknown_not_new_terminal_chemistry():
    molsys = _path()
    bonds = molsys.chemical_states.get_bonds()
    link = next(
        i
        for i, row in bonds.iterrows()
        if {int(row["atom1_index"]), int(row["atom2_index"])} == {5, 6}
    )
    molsys.chemical_states.remove_bonds([int(link)])
    with pytest.raises(msm.StructuralInconsistencyError, match="Disconnected"):
        msm.chemical_states.get_peptide_termini(molsys)
    report = msm.chemical_states.get_peptide_termini(molsys, on_ambiguous="report")
    assert report["unassessed_chain_indices"].tolist() == [0]
    assert report["n_terminal_group_indices"].shape == (0,)
    assert report["c_terminal_group_indices"].shape == (0,)
