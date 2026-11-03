import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.native import MolSys
from molsysmt.native._chemical_components import group_components, indices_from_bonds
from molsysmt.native._component_projection import prepare as prepare_components
from molsysmt.native._topology_infer import (
    fallback_ids,
    infer_group_types_from_topology,
    prepare_topology_for_chain_queries,
    prepare_topology_for_entity_queries,
    prepare_topology_for_molecule_queries,
    project_chain_index_from_topology,
    project_chain_name_from_topology,
    project_chain_type_from_topology,
    project_entity_index_from_topology,
    project_entity_name_from_topology,
    project_entity_type_from_topology,
    project_molecule_index_from_topology,
    project_molecule_name_from_topology,
    project_molecule_type_from_topology,
)


def test_fallback_ids_returns_string_ids():
    output = fallback_ids(4)
    assert output.tolist() == ["0", "1", "2", "3"]


def test_infer_group_types_matches_rebuild_groups(t4_h5msm_molsys):
    topology = t4_h5msm_molsys.topology.copy()
    inferred = infer_group_types_from_topology(topology)

    rebuilt = topology.copy()
    rebuilt.rebuild_groups(redefine_ids=False, redefine_types=True)

    assert inferred.tolist() == rebuilt.groups["group_type"].to_list()


def test_infer_component_indices_matches_rebuild_components(t4_h5msm_molsys):
    source = t4_h5msm_molsys.copy(deep=False)
    chemistry = source.chemical_states
    inferred = indices_from_bonds(chemistry.n_atoms, chemistry.get_bonds())
    source.rebuild_components(redefine_ids=False, force=True)
    assert inferred.tolist() == chemistry._get_component_indices().tolist()
    assert "component_index" not in source.topology.groups
    assert "component_index" not in source.topology.atoms


def test_component_inference_fails_closed_without_reference_chemical_state():
    source = MolSys(n_atoms=3)
    source.chemical_states._append_chemical_state_bonds([[0, 1]])
    source.chemical_states.append_state()
    source.chemical_states._set_reference_index(None)
    with pytest.raises(StructuralInconsistencyError, match="ambiguous"):
        msm.element.component.get_component_index(source, redefine_indices=True)


def test_prepare_component_queries_preserves_independent_domains(t4_h5msm_molsys):
    prepared = prepare_components(t4_h5msm_molsys, indices=True, names=True, types=True)
    assert "component_index" not in prepared.topology.groups
    assert "component_index" not in prepared.topology.atoms
    assert prepared.chemical_states._get_component_indices().isna().sum() == 0
    assert "component_name" in prepared.chemical_states._states[0].components
    assert "component_type" in prepared.chemical_states._states[0].components
    assert prepared.chemical_states is not t4_h5msm_molsys.chemical_states


def test_project_component_queries_follow_explicit_state(t4_h5msm_molsys):
    source = prepare_components(t4_h5msm_molsys, indices=True, names=True, types=True)
    topology, chemistry = source.topology, source.chemical_states
    state = chemistry._states[0]
    group_membership = group_components(topology, state.component_indices)
    names = state.components["component_name"].tolist()
    types = state.components["component_type"].tolist()
    membership = state.component_indices.to_numpy(dtype=np.int64)
    assert msm.element.component.get_component_index(source, element="group") == [
        int(value) if value >= 0 else None for value in group_membership
    ]
    assert msm.element.component.get_component_name(source) == names
    assert msm.element.component.get_component_type(source) == types
    assert msm.element.component.get_component_name(source, element="atom") == [
        names[i] for i in membership
    ]
    assert msm.element.component.get_component_type(source, element="atom") == [
        types[i] for i in membership
    ]


def test_prepare_topology_for_molecule_queries_populates_missing_columns(
    t4_h5msm_molsys,
):
    topology = t4_h5msm_molsys.topology.copy()

    prepared = prepare_topology_for_molecule_queries(topology, element="entity")

    assert "component_index" not in prepared.groups.columns
    assert "component_index" not in prepared.atoms.columns
    assert prepared.groups["molecule_index"].isnull().sum() == 0
    assert prepared.molecules["entity_index"].isnull().sum() == 0


def test_project_molecule_queries_follow_prepared_topology(t4_h5msm_molsys):
    topology = prepare_topology_for_molecule_queries(
        t4_h5msm_molsys.topology.copy(), element="chain"
    )

    molecule_names = topology.molecules["molecule_name"].to_numpy(dtype=object)
    molecule_types = topology.molecules["molecule_type"].to_numpy(dtype=object)
    molecule_index_from_group = topology.groups["molecule_index"].to_numpy(
        dtype=np.int64, na_value=-1
    )
    group_index_from_atom = topology.atoms["group_index"].to_numpy(
        dtype=np.int64, na_value=-1
    )
    # component_index is atom-level; derive per-group from atoms
    state = t4_h5msm_molsys.chemical_states._states[0]
    component_index_from_group = group_components(topology, state.component_indices)
    entity_index_from_molecule = topology.molecules["entity_index"].to_numpy(
        dtype=np.int64, na_value=-1
    )

    assert (
        project_molecule_index_from_topology(topology, element="group")
        == molecule_index_from_group.tolist()
    )
    assert (
        project_molecule_name_from_topology(topology, element="molecule")
        == molecule_names.tolist()
    )
    assert (
        project_molecule_type_from_topology(topology, element="molecule")
        == molecule_types.tolist()
    )
    assert (
        project_molecule_name_from_topology(topology, element="atom")
        == molecule_names[molecule_index_from_group[group_index_from_atom]].tolist()
    )
    assert (
        project_molecule_type_from_topology(topology, element="atom")
        == molecule_types[molecule_index_from_group[group_index_from_atom]].tolist()
    )

    expected_component_indices = np.full(len(state.components), -1, dtype=np.int64)
    for group_index, component_index in enumerate(component_index_from_group):
        if component_index >= 0 and expected_component_indices[component_index] < 0:
            expected_component_indices[component_index] = molecule_index_from_group[
                group_index
            ]
    assert (
        msm.element.molecule.get_molecule_index(
            [topology, t4_h5msm_molsys.chemical_states], element="component"
        )
        == expected_component_indices.tolist()
    )

    expected_chain = []
    # chain_index is atom-level; derive per-group from atoms
    _adf = topology.atoms[["group_index", "chain_index"]].dropna()
    _gc = _adf.groupby("group_index", sort=False)["chain_index"].first()
    chain_index_from_group = np.full(topology.n_groups, -1, dtype=np.int64)
    chain_index_from_group[_gc.index.to_numpy(dtype=np.int64)] = _gc.to_numpy(
        dtype=np.int64
    )
    for chain_index in range(topology.n_chains):
        group_indices = np.where(chain_index_from_group == chain_index)[0]
        chain_molecule_indices = np.unique(molecule_index_from_group[group_indices])
        expected_chain.append(
            chain_molecule_indices[chain_molecule_indices >= 0].tolist()
        )
    assert (
        project_molecule_index_from_topology(topology, element="chain")
        == expected_chain
    )

    expected_entity = []
    for entity_index in range(topology.n_entities):
        expected_entity.append(
            np.where(entity_index_from_molecule == entity_index)[0].tolist()
        )
    assert (
        project_molecule_index_from_topology(topology, element="entity")
        == expected_entity
    )


def test_prepare_topology_for_chain_queries_populates_missing_columns(t4_h5msm_molsys):
    topology = t4_h5msm_molsys.topology.copy()

    prepared = prepare_topology_for_chain_queries(topology)

    assert "chain_index" in prepared.atoms.columns
    assert "chain_index" not in prepared.groups.columns
    assert prepared.chains["chain_name"].isnull().sum() == 0
    assert prepared.chains["chain_type"].isnull().sum() == 0


def test_project_chain_queries_follow_prepared_topology(t4_h5msm_molsys):
    topology = prepare_topology_for_chain_queries(t4_h5msm_molsys.topology.copy())

    chain_names = topology.chains["chain_name"].to_numpy(dtype=object)
    chain_types = topology.chains["chain_type"].to_numpy(dtype=object)
    atom_chain_index = topology.atoms["chain_index"].to_numpy(
        dtype=np.int64, na_value=-1
    )
    # chain_index is atom-level; derive per-group from atoms

    _adf = topology.atoms[["group_index", "chain_index"]].dropna()
    _gc = _adf.groupby("group_index", sort=False)["chain_index"].first()
    group_chain_index = np.full(topology.n_groups, -1, dtype=np.int64)
    group_chain_index[_gc.index.to_numpy(dtype=np.int64)] = _gc.to_numpy(dtype=np.int64)

    assert (
        project_chain_index_from_topology(topology, element="atom")
        == atom_chain_index.tolist()
    )
    assert (
        project_chain_index_from_topology(topology, element="group")
        == group_chain_index.tolist()
    )
    assert (
        project_chain_name_from_topology(topology, element="chain")
        == chain_names.tolist()
    )
    assert (
        project_chain_type_from_topology(topology, element="chain")
        == chain_types.tolist()
    )


def test_project_entity_queries_follow_prepared_topology(t4_h5msm_molsys):
    topology = prepare_topology_for_entity_queries(t4_h5msm_molsys.topology.copy())

    entity_names = topology.entities["entity_name"].to_numpy(dtype=object)
    entity_types = topology.entities["entity_type"].to_numpy(dtype=object)
    entity_index_from_molecule = topology.molecules["entity_index"].to_numpy(
        dtype=np.int64, na_value=-1
    )
    molecule_index_from_group = topology.groups["molecule_index"].to_numpy(
        dtype=np.int64, na_value=-1
    )
    group_index_from_atom = topology.atoms["group_index"].to_numpy(
        dtype=np.int64, na_value=-1
    )
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]

    assert (
        project_entity_index_from_topology(topology, element="molecule")
        == entity_index_from_molecule.tolist()
    )
    assert (
        project_entity_name_from_topology(topology, element="entity")
        == entity_names.tolist()
    )
    assert (
        project_entity_type_from_topology(topology, element="entity")
        == entity_types.tolist()
    )
    assert (
        project_entity_name_from_topology(topology, element="atom")
        == entity_names[entity_index_from_molecule[molecule_index_from_atom]].tolist()
    )
    assert (
        project_entity_type_from_topology(topology, element="atom")
        == entity_types[entity_index_from_molecule[molecule_index_from_atom]].tolist()
    )


def test_independent_rebuilds_generate_string_ids_and_metadata(t4_h5msm_molsys):
    source = t4_h5msm_molsys.copy()
    topology = source.topology
    state = source.chemical_states._states[0]

    topology.rebuild_groups(redefine_ids=True, redefine_types=True)
    source.rebuild_components(
        redefine_indices=True,
        redefine_ids=True,
        redefine_types=True,
        redefine_names=True,
        force=True,
    )
    topology.rebuild_molecules(
        redefine_indices=True,
        redefine_ids=True,
        redefine_names=True,
        redefine_types=True,
        force=True,
    )
    topology.rebuild_chains(
        redefine_indices=True,
        redefine_ids=True,
        redefine_names=True,
        redefine_types=True,
    )
    topology.rebuild_entities(
        redefine_indices=True,
        redefine_ids=True,
        redefine_names=True,
        redefine_types=True,
        force=True,
    )

    assert topology.groups["group_id"].map(type).eq(str).all()
    assert state.components["component_id"].map(type).eq(str).all()
    assert topology.molecules["molecule_id"].map(type).eq(str).all()
    assert topology.chains["chain_id"].map(type).eq(str).all()
    assert topology.entities["entity_id"].map(type).eq(str).all()

    assert topology.groups["group_type"].isnull().sum() == 0
    assert state.components["component_type"].isnull().sum() == 0
    assert state.components["component_name"].isnull().sum() == 0
    assert topology.molecules["molecule_type"].isnull().sum() == 0
    assert topology.molecules["molecule_name"].isnull().sum() == 0
    assert topology.chains["chain_type"].isnull().sum() == 0
    assert topology.chains["chain_name"].isnull().sum() == 0
    assert topology.entities["entity_type"].isnull().sum() == 0
    assert topology.entities["entity_name"].isnull().sum() == 0
