"""Protecting component labels only while their atom membership stays unchanged."""

import numpy as np
import pandas as pd
import pytest

from molsysmt.native import Topology
from molsysmt.native.topology import Bonds_DataFrame


def component_topology():
    topology = Topology(n_atoms=6, n_components=3)
    topology._set_component_indices([2, 2, 0, 0, 1, 1])
    topology.components["component_id"] = ["ligand", "water", "protein"]
    topology.components["component_name"] = ["Ligand", "Water", "Protein"]
    topology.components["component_type"] = ["small molecule", "water", "protein"]
    bonds = Bonds_DataFrame(n_bonds=3)
    bonds["atom1_index"] = [0, 2, 4]
    bonds["atom2_index"] = [1, 3, 5]
    topology.bonds = bonds
    return topology


def test_rebuild_preserves_labels_by_membership_after_row_reordering():
    topology = component_topology()
    topology.rebuild_components(
        redefine_ids=False, redefine_names=False, redefine_types=False
    )
    np.testing.assert_array_equal(topology._get_component_indices(), [0, 0, 1, 1, 2, 2])
    assert topology.components.component_id.tolist() == ["protein", "ligand", "water"]
    assert topology.components.component_name.tolist() == ["Protein", "Ligand", "Water"]
    assert topology.components.component_type.tolist() == [
        "protein",
        "small molecule",
        "water",
    ]


@pytest.mark.parametrize("operation", ["merge", "split", "unknown", "outside_table"])
def test_changed_or_unresolved_memberships_do_not_inherit_labels(operation):
    topology = component_topology()
    if operation == "merge":
        topology._append_chemical_state_bonds([[1, 2]], orders=[1])
    elif operation == "split":
        topology.bonds = topology.bonds.iloc[1:].reset_index(drop=True)
    elif operation == "unknown":
        topology._set_component_indices(pd.NA, atom_indices=[1])
    else:
        topology._set_component_indices(100000000, atom_indices=[0, 1])
    topology.rebuild_components(
        redefine_ids=False, redefine_names=False, redefine_types=False
    )
    new_indices = topology._get_component_indices().to_numpy(dtype=np.int64)
    touched = np.unique(new_indices[:4] if operation == "merge" else new_indices[:2])
    assert topology.components.iloc[touched].isna().all().all()
    outside = new_indices[4]
    assert topology.components.loc[outside].tolist() == ["water", "Water", "water"]
    assert topology._resolve_chemical_state().component_completeness == "partial"


@pytest.mark.parametrize("field", ["ids", "types", "names"])
def test_each_redefinition_only_replaces_its_requested_column(field):
    topology = component_topology()
    kwargs = dict(redefine_ids=False, redefine_types=False, redefine_names=False)
    kwargs[f"redefine_{field}"] = True
    topology.rebuild_components(**kwargs)
    expected = {
        "component_id": ["protein", "ligand", "water"],
        "component_type": ["protein", "small molecule", "water"],
        "component_name": ["Protein", "Ligand", "Water"],
    }
    expected[
        {"ids": "component_id", "types": "component_type", "names": "component_name"}[
            field
        ]
    ] = {
        "ids": ["0", "1", "2"],
        "types": ["unknown"] * 3,
        "names": ["protein 0", "small molecule 0", "water"],
    }[field]
    for column, values in expected.items():
        assert topology.components[column].tolist() == values


def test_forced_rebuild_preserves_only_the_resolved_state():
    topology = component_topology()
    second = topology._append_chemical_state(state_id="alternative")
    original_membership = topology._get_component_indices(state_index=0).copy()
    original_components = topology._chemical_states[0].components.copy(deep=True)
    original_bonds = topology.bonds.copy(deep=True)
    with topology._using_chemical_state(second):
        topology._set_component_indices(original_membership)
        topology.components = original_components.copy(deep=True)
        topology.bonds = original_bonds
        topology.components["component_id"] = ["a", "b", "c"]
        topology.rebuild_components(
            redefine_indices=False,
            force=True,
            redefine_ids=False,
            redefine_names=False,
            redefine_types=False,
        )
        assert topology.components.component_id.tolist() == ["c", "a", "b"]
    pd.testing.assert_series_equal(
        topology._get_component_indices(state_index=0), original_membership
    )
    pd.testing.assert_frame_equal(
        topology._chemical_states[0].components, original_components
    )


def test_empty_and_unknown_component_tables_do_not_synthesize_labels():
    for n_atoms in (0, 3):
        topology = Topology(n_atoms=n_atoms)
        topology.rebuild_components(
            redefine_ids=False, redefine_types=False, redefine_names=False
        )
        assert topology.components.shape[0] == n_atoms
        assert topology.components.isna().all().all()


def test_molsys_wrapper_preserves_unredefined_component_fields():
    from molsysmt.native import MolSys

    molsys = MolSys()
    molsys.topology = component_topology()
    molsys.rebuild_components(redefine_ids=False, redefine_types=False)
    assert molsys.topology.components.component_id.tolist() == [
        "protein",
        "ligand",
        "water",
    ]
    assert molsys.topology.components.component_type.tolist() == [
        "protein",
        "small molecule",
        "water",
    ]
