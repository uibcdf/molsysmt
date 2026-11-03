"""Protect warning-free composition and independently mutable native tables."""

import warnings

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm


def _table(system, name):
    if name == "components":
        return system.chemical_states._resolve_chemical_state().components
    return getattr(system.topology, name)


@pytest.mark.parametrize("operation", ["merge", "add"])
def test_composition_preserves_values_without_copy_deprecations(
    alanine_molsys, operation
):
    left = alanine_molsys.copy()
    right = left.copy()
    left.chemical_states._set_chemical_state_atom_attribute(
        "formal_charge", [0] * left.topology.n_atoms
    )
    right.chemical_states._set_chemical_state_atom_attribute(
        "formal_charge", [1] * right.topology.n_atoms
    )
    snapshots = [item.copy() for item in (left, right)]
    with warnings.catch_warnings(record=True) as observed:
        warnings.simplefilter("always")
        if operation == "merge":
            combined = msm.merge([left, right], to_form="molsysmt.MolSys")
        else:
            combined = left.copy()
            combined.add(right)
    assert not [
        warning
        for warning in observed
        if issubclass(warning.category, (DeprecationWarning, FutureWarning))
    ]
    assert combined.topology.n_atoms == 2 * left.topology.n_atoms
    assert (
        combined.chemical_states._get_chemical_state_atom_attribute(
            "formal_charge"
        ).tolist()
        == [0] * left.topology.n_atoms + [1] * right.topology.n_atoms
    )
    expected = np.concatenate(
        [
            left.chemical_states.get_bonds()[["atom1_index", "atom2_index"]].to_numpy(
                dtype=np.int64
            ),
            right.chemical_states.get_bonds()[["atom1_index", "atom2_index"]].to_numpy(
                dtype=np.int64
            )
            + left.topology.n_atoms,
        ]
    )
    np.testing.assert_array_equal(
        combined.chemical_states.get_bonds()[["atom1_index", "atom2_index"]], expected
    )
    for original, snapshot in zip((left, right), snapshots):
        for table in (
            "atoms",
            "groups",
            "components",
            "molecules",
            "chains",
            "entities",
        ):
            pd.testing.assert_frame_equal(
                _table(original, table), _table(snapshot, table)
            )
        pd.testing.assert_frame_equal(
            original.chemical_states._states[0].atom_attributes,
            snapshot.chemical_states._states[0].atom_attributes,
        )
    for table, column in (
        ("atoms", "atom_name"),
        ("groups", "group_name"),
        ("components", "component_name"),
        ("molecules", "molecule_name"),
        ("chains", "chain_id"),
        ("entities", "entity_name"),
    ):
        output = _table(combined, table)
        output.at[0, column] = "output-only"
        assert _table(left, table).at[0, column] != "output-only"
        original = _table(right, table)
        snapshot = output.copy(deep=True)
        original.at[0, column] = "source-only"
        pd.testing.assert_frame_equal(output, snapshot)
    combined.chemical_states._states[0].atom_attributes.at[0, "formal_charge"] = 9
    assert (
        left.chemical_states._get_chemical_state_atom_attribute("formal_charge").iloc[0]
        == 0
    )
    right.chemical_states._states[0].atom_attributes.at[0, "formal_charge"] = 7
    assert (
        combined.chemical_states._get_chemical_state_atom_attribute(
            "formal_charge"
        ).iloc[left.topology.n_atoms]
        == 1
    )
