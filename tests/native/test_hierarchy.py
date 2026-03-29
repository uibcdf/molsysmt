import numpy as np

from molsysmt.native._topology_infer import (
    fallback_ids,
    infer_component_indices_from_topology,
    infer_group_types_from_topology,
    prepare_topology_for_chain_queries,
    prepare_topology_for_component_queries,
    prepare_topology_for_entity_queries,
    prepare_topology_for_molecule_queries,
    project_chain_index_from_topology,
    project_chain_name_from_topology,
    project_chain_type_from_topology,
    project_component_index_from_topology,
    project_component_name_from_topology,
    project_component_type_from_topology,
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
    topology = t4_h5msm_molsys.topology.copy()
    # component_index is atom-level only — infer returns per-atom array
    atom_component_index = infer_component_indices_from_topology(topology)

    rebuilt = topology.copy()
    rebuilt.rebuild_groups(redefine_ids=False, redefine_types=True)
    rebuilt.rebuild_components(
        redefine_indices=True,
        redefine_ids=False,
        redefine_types=True,
        redefine_names=True,
        force=True,
    )

    assert atom_component_index.tolist() == rebuilt.atoms["component_index"].to_list()
    assert "component_index" not in rebuilt.groups.columns


def test_prepare_topology_for_component_queries_populates_missing_columns(t4_h5msm_molsys):
    topology = t4_h5msm_molsys.topology.copy()
    # component_index lives on atoms, not groups
    assert "component_index" not in topology.groups.columns

    prepared = prepare_topology_for_component_queries(
        topology,
        redefine_indices=False,
        redefine_names=False,
        redefine_types=False,
    )

    assert "component_index" not in prepared.groups.columns
    assert "component_index" in prepared.atoms.columns
    assert "component_name" in prepared.components.columns
    assert "component_type" in prepared.components.columns
    assert prepared.atoms["component_index"].isnull().sum() == 0


def test_project_component_queries_follow_prepared_topology(t4_h5msm_molsys):
    topology = prepare_topology_for_component_queries(t4_h5msm_molsys.topology.copy())

    # component_index is atom-level; derive per-group from atoms
    from molsysmt.native._topology_infer import _component_index_per_group
    group_component_index = _component_index_per_group(topology)
    component_names = topology.components["component_name"].to_numpy(dtype=object)
    component_types = topology.components["component_type"].to_numpy(dtype=object)
    group_index_from_atom = topology.atoms["group_index"].to_numpy(dtype=np.int64, na_value=-1)

    assert project_component_index_from_topology(topology, element="group") == group_component_index.tolist()
    assert project_component_name_from_topology(topology, element="component") == component_names.tolist()
    assert project_component_type_from_topology(topology, element="component") == component_types.tolist()
    assert project_component_name_from_topology(topology, element="atom") == component_names[group_component_index[group_index_from_atom]].tolist()
    assert project_component_type_from_topology(topology, element="atom") == component_types[group_component_index[group_index_from_atom]].tolist()


def test_prepare_topology_for_molecule_queries_populates_missing_columns(t4_h5msm_molsys):
    topology = t4_h5msm_molsys.topology.copy()

    prepared = prepare_topology_for_molecule_queries(topology, element="entity")

    assert "component_index" not in prepared.groups.columns
    assert "component_index" in prepared.atoms.columns
    assert prepared.groups["molecule_index"].isnull().sum() == 0
    assert prepared.molecules["entity_index"].isnull().sum() == 0


def test_project_molecule_queries_follow_prepared_topology(t4_h5msm_molsys):
    topology = prepare_topology_for_molecule_queries(t4_h5msm_molsys.topology.copy(), element="chain")

    molecule_names = topology.molecules["molecule_name"].to_numpy(dtype=object)
    molecule_types = topology.molecules["molecule_type"].to_numpy(dtype=object)
    molecule_index_from_group = topology.groups["molecule_index"].to_numpy(dtype=np.int64, na_value=-1)
    group_index_from_atom = topology.atoms["group_index"].to_numpy(dtype=np.int64, na_value=-1)
    # component_index is atom-level; derive per-group from atoms
    from molsysmt.native._topology_infer import _component_index_per_group
    component_index_from_group = _component_index_per_group(topology)
    entity_index_from_molecule = topology.molecules["entity_index"].to_numpy(dtype=np.int64, na_value=-1)

    assert project_molecule_index_from_topology(topology, element="group") == molecule_index_from_group.tolist()
    assert project_molecule_name_from_topology(topology, element="molecule") == molecule_names.tolist()
    assert project_molecule_type_from_topology(topology, element="molecule") == molecule_types.tolist()
    assert project_molecule_name_from_topology(topology, element="atom") == molecule_names[molecule_index_from_group[group_index_from_atom]].tolist()
    assert project_molecule_type_from_topology(topology, element="atom") == molecule_types[molecule_index_from_group[group_index_from_atom]].tolist()

    expected_component_indices = np.full(topology.n_components, -1, dtype=np.int64)
    for group_index, component_index in enumerate(component_index_from_group):
        if component_index >= 0 and expected_component_indices[component_index] < 0:
            expected_component_indices[component_index] = molecule_index_from_group[group_index]
    assert project_molecule_index_from_topology(topology, element="component") == expected_component_indices.tolist()

    expected_chain = []
    # chain_index is atom-level; derive per-group from atoms
    _adf = topology.atoms[["group_index", "chain_index"]].dropna()
    _gc = _adf.groupby("group_index", sort=False)["chain_index"].first()
    chain_index_from_group = np.full(topology.n_groups, -1, dtype=np.int64)
    chain_index_from_group[_gc.index.to_numpy(dtype=np.int64)] = _gc.to_numpy(dtype=np.int64)
    for chain_index in range(topology.n_chains):
        group_indices = np.where(chain_index_from_group == chain_index)[0]
        chain_molecule_indices = np.unique(molecule_index_from_group[group_indices])
        expected_chain.append(chain_molecule_indices[chain_molecule_indices >= 0].tolist())
    assert project_molecule_index_from_topology(topology, element="chain") == expected_chain

    expected_entity = []
    for entity_index in range(topology.n_entities):
        expected_entity.append(np.where(entity_index_from_molecule == entity_index)[0].tolist())
    assert project_molecule_index_from_topology(topology, element="entity") == expected_entity


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
    atom_chain_index = topology.atoms["chain_index"].to_numpy(dtype=np.int64, na_value=-1)
    # chain_index is atom-level; derive per-group from atoms
    from molsysmt.native._topology_infer import _component_index_per_group
    _adf = topology.atoms[["group_index", "chain_index"]].dropna()
    _gc = _adf.groupby("group_index", sort=False)["chain_index"].first()
    group_chain_index = np.full(topology.n_groups, -1, dtype=np.int64)
    group_chain_index[_gc.index.to_numpy(dtype=np.int64)] = _gc.to_numpy(dtype=np.int64)

    assert project_chain_index_from_topology(topology, element="atom") == atom_chain_index.tolist()
    assert project_chain_index_from_topology(topology, element="group") == group_chain_index.tolist()
    assert project_chain_name_from_topology(topology, element="chain") == chain_names.tolist()
    assert project_chain_type_from_topology(topology, element="chain") == chain_types.tolist()


def test_project_entity_queries_follow_prepared_topology(t4_h5msm_molsys):
    topology = prepare_topology_for_entity_queries(t4_h5msm_molsys.topology.copy())

    entity_names = topology.entities["entity_name"].to_numpy(dtype=object)
    entity_types = topology.entities["entity_type"].to_numpy(dtype=object)
    entity_index_from_molecule = topology.molecules["entity_index"].to_numpy(dtype=np.int64, na_value=-1)
    molecule_index_from_group = topology.groups["molecule_index"].to_numpy(dtype=np.int64, na_value=-1)
    group_index_from_atom = topology.atoms["group_index"].to_numpy(dtype=np.int64, na_value=-1)
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]

    assert project_entity_index_from_topology(topology, element="molecule") == entity_index_from_molecule.tolist()
    assert project_entity_name_from_topology(topology, element="entity") == entity_names.tolist()
    assert project_entity_type_from_topology(topology, element="entity") == entity_types.tolist()
    assert project_entity_name_from_topology(topology, element="atom") == entity_names[entity_index_from_molecule[molecule_index_from_atom]].tolist()
    assert project_entity_type_from_topology(topology, element="atom") == entity_types[entity_index_from_molecule[molecule_index_from_atom]].tolist()


def test_topology_rebuilds_generate_string_ids_and_non_null_metadata(t4_h5msm_molsys):
    topology = t4_h5msm_molsys.topology.copy()

    topology.rebuild_groups(redefine_ids=True, redefine_types=True)
    topology.rebuild_components(redefine_indices=True, redefine_ids=True, redefine_types=True, redefine_names=True, force=True)
    topology.rebuild_molecules(redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True, force=True)
    topology.rebuild_chains(redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True)
    topology.rebuild_entities(redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True, force=True)

    assert topology.groups["group_id"].map(type).eq(str).all()
    assert topology.components["component_id"].map(type).eq(str).all()
    assert topology.molecules["molecule_id"].map(type).eq(str).all()
    assert topology.chains["chain_id"].map(type).eq(str).all()
    assert topology.entities["entity_id"].map(type).eq(str).all()

    assert topology.groups["group_type"].isnull().sum() == 0
    assert topology.components["component_type"].isnull().sum() == 0
    assert topology.components["component_name"].isnull().sum() == 0
    assert topology.molecules["molecule_type"].isnull().sum() == 0
    assert topology.molecules["molecule_name"].isnull().sum() == 0
    assert topology.chains["chain_type"].isnull().sum() == 0
    assert topology.chains["chain_name"].isnull().sum() == 0
    assert topology.entities["entity_type"].isnull().sum() == 0
    assert topology.entities["entity_name"].isnull().sum() == 0
