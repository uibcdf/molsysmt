import numpy as np


def fallback_ids(n_items):
    return np.arange(n_items, dtype=int).astype(str)


def _group_atom_names(topology):
    atom_group_indices = topology.atoms["group_index"].to_numpy(dtype=np.int64, na_value=-1)
    atom_names = topology.atoms["atom_name"].to_numpy(dtype=object)
    names_by_group = {}
    for atom_name, group_index in zip(atom_names, atom_group_indices):
        if group_index < 0:
            continue
        names_by_group.setdefault(int(group_index), set()).add(atom_name)
    return names_by_group


def infer_group_types_from_topology(topology):
    from molsysmt.element.group import get_group_type_from_group_name
    from molsysmt.element.group.small_molecule.group_names import group_names as reserved_small_molecule_names

    group_names = topology.groups["group_name"].to_numpy(dtype=object)
    atom_names_by_group = _group_atom_names(topology)

    output = []
    for group_index, group_name in enumerate(group_names):
        group_type = get_group_type_from_group_name(group_name)
        if group_type == "small molecule" and group_name in reserved_small_molecule_names:
            atom_names = atom_names_by_group.get(group_index, set())
            if {"N", "CA", "C", "O", "CB"}.issubset(atom_names):
                group_type = "amino acid"
        output.append(group_type)

    return np.array(output, dtype=object)


def infer_component_indices_from_topology(topology):
    from molsysmt.lib.topology import get_component_index_from_bonded_atom_pairs

    n_atoms = topology.n_atoms
    bonded_atom_pairs = topology.bonds[["atom1_index", "atom2_index"]].to_numpy()
    bonded_atom_pairs = np.asarray(bonded_atom_pairs, dtype=np.int64)

    if bonded_atom_pairs.size == 0:
        bonded_atom_pairs = np.empty((0, 2), dtype=np.int64)
    else:
        bonded_atom_pairs = bonded_atom_pairs.reshape((-1, 2))

    atom_component_index = get_component_index_from_bonded_atom_pairs(
        bonded_atom_pairs, np.int64(n_atoms)
    ).astype(np.int64)

    group_index_of_atoms = topology.atoms["group_index"].to_numpy(dtype=np.int64, na_value=-1)
    n_groups = topology.n_groups
    group_component_index = np.full(n_groups, -1, dtype=np.int64)
    for atom_component, group_index in zip(atom_component_index, group_index_of_atoms):
        if group_index >= 0 and group_component_index[group_index] < 0:
            group_component_index[group_index] = atom_component

    return atom_component_index, group_component_index


def infer_component_types_from_topology(topology):
    from molsysmt.element.component.get_component_type import _get_component_type_from_group_names_and_types

    component_index_of_groups = topology.groups["component_index"].to_numpy(dtype=np.int64, na_value=-1)
    group_names = topology.groups["group_name"].to_numpy(dtype=object)
    group_types = topology.groups["group_type"].to_numpy(dtype=object)

    n_components = topology.n_components
    output = np.empty(n_components, dtype=object)

    for component_index in range(n_components):
        mask = component_index_of_groups == component_index
        if np.any(mask):
            output[component_index] = _get_component_type_from_group_names_and_types(
                group_names[mask], group_types[mask]
            )
        else:
            output[component_index] = "unknown"

    return output


def infer_component_names_from_topology(topology):
    component_index_of_groups = topology.groups["component_index"].to_numpy(dtype=np.int64, na_value=-1)
    component_types = topology.components["component_type"].to_numpy(dtype=object)
    group_names = topology.groups["group_name"].to_numpy(dtype=object)

    output = []
    counters = {"peptide": 0, "protein": 0, "small molecule": 0, "unknown": 0}
    peptides = {}

    for component_index, component_type in enumerate(component_types):
        mask = component_index_of_groups == component_index
        names_in_component = group_names[mask].tolist()

        if component_type == "peptide":
            peptide_key = ",".join(names_in_component)
            if peptide_key in peptides:
                name = peptides[peptide_key]
            else:
                name = f"{component_type} {counters[component_type]}"
                peptides[peptide_key] = name
                counters[component_type] += 1
        elif component_type in ["protein", "small molecule"]:
            name = f"{component_type} {counters[component_type]}"
            counters[component_type] += 1
        elif component_type in ["ion", "lipid"]:
            name = names_in_component[0] if names_in_component else f"unknown {counters['unknown']}"
        elif component_type == "water":
            name = "water"
        else:
            name = f"unknown {counters['unknown']}"
            counters["unknown"] += 1

        output.append(name)

    return np.array(output, dtype=object)


def infer_molecule_indices_from_topology(topology):
    return topology.groups["component_index"].to_numpy(dtype=np.int64, na_value=-1).copy()


def infer_molecule_types_from_topology(topology):
    molecule_index_of_groups = topology.groups["molecule_index"].to_numpy(dtype=np.int64, na_value=-1)
    component_types = topology.components["component_type"].to_numpy(dtype=object)
    output = np.empty(topology.n_molecules, dtype=object)
    for molecule_index in range(topology.n_molecules):
        group_indices = np.where(molecule_index_of_groups == molecule_index)[0]
        if len(group_indices) == 0:
            output[molecule_index] = "unknown"
            continue
        component_index = int(topology.groups.iloc[group_indices[0]]["component_index"])
        output[molecule_index] = component_types[component_index]
    return output


def infer_molecule_names_from_topology(topology):
    molecule_index_of_groups = topology.groups["molecule_index"].to_numpy(dtype=np.int64, na_value=-1)
    component_names = topology.components["component_name"].to_numpy(dtype=object)
    output = np.empty(topology.n_molecules, dtype=object)
    for molecule_index in range(topology.n_molecules):
        group_indices = np.where(molecule_index_of_groups == molecule_index)[0]
        if len(group_indices) == 0:
            output[molecule_index] = f"unknown {molecule_index}"
            continue
        component_index = int(topology.groups.iloc[group_indices[0]]["component_index"])
        output[molecule_index] = component_names[component_index]
    return output


def infer_entity_indices_from_topology(topology):
    molecule_names = topology.molecules["molecule_name"].to_numpy(dtype=object)
    molecule_types = topology.molecules["molecule_type"].to_numpy(dtype=object)

    entity_indices = []
    keys = {}
    count = 0

    for molecule_name, molecule_type in zip(molecule_names, molecule_types):
        key = "water" if molecule_type == "water" else molecule_name
        if key not in keys:
            keys[key] = count
            count += 1
        entity_indices.append(keys[key])

    return np.array(entity_indices, dtype=np.int64)


def infer_entity_names_from_topology(topology):
    entity_index_of_molecules = topology.molecules["entity_index"].to_numpy(dtype=np.int64, na_value=-1)
    molecule_names = topology.molecules["molecule_name"].to_numpy(dtype=object)
    molecule_types = topology.molecules["molecule_type"].to_numpy(dtype=object)

    output = np.empty(topology.n_entities, dtype=object)
    for entity_index in range(topology.n_entities):
        molecule_indices = np.where(entity_index_of_molecules == entity_index)[0]
        if len(molecule_indices) == 0:
            output[entity_index] = f"unknown {entity_index}"
            continue
        first_molecule_index = molecule_indices[0]
        if molecule_types[first_molecule_index] == "water":
            output[entity_index] = "water"
        else:
            output[entity_index] = molecule_names[first_molecule_index]
    return output


def infer_entity_types_from_topology(topology):
    entity_index_of_molecules = topology.molecules["entity_index"].to_numpy(dtype=np.int64, na_value=-1)
    molecule_types = topology.molecules["molecule_type"].to_numpy(dtype=object)

    output = np.empty(topology.n_entities, dtype=object)
    for entity_index in range(topology.n_entities):
        molecule_indices = np.where(entity_index_of_molecules == entity_index)[0]
        if len(molecule_indices) == 0:
            output[entity_index] = "unknown"
            continue
        output[entity_index] = molecule_types[molecule_indices[0]]
    return output


def infer_chain_indices_from_topology(topology):
    n_atoms = topology.n_atoms
    n_groups = topology.n_groups

    if n_atoms == 0:
        return np.empty(0, dtype=np.int64), np.empty(n_groups, dtype=np.int64)

    atom_chain_index = topology.atoms["chain_index"].to_numpy(dtype=np.int64, na_value=-1)
    if np.all(atom_chain_index < 0):
        atom_chain_index = np.zeros(n_atoms, dtype=np.int64)
    else:
        atom_chain_index = atom_chain_index.copy()
        atom_chain_index[atom_chain_index < 0] = 0

    group_index_of_atoms = topology.atoms["group_index"].to_numpy(dtype=np.int64, na_value=-1)
    group_chain_index = np.full(n_groups, -1, dtype=np.int64)
    for chain_index, group_index in zip(atom_chain_index, group_index_of_atoms):
        if group_index >= 0 and group_chain_index[group_index] < 0:
            group_chain_index[group_index] = chain_index

    if np.any(group_chain_index < 0):
        group_chain_index[group_chain_index < 0] = 0

    return atom_chain_index, group_chain_index


def infer_chain_ids_from_topology(topology):
    return fallback_ids(topology.n_chains)


def infer_chain_names_from_topology(topology):
    from molsysmt.element.chain.chain_names import all_chain_names

    n_chains = topology.n_chains
    return np.array([all_chain_names[ii] for ii in range(n_chains)], dtype=object)


def infer_chain_types_from_topology(topology):
    from molsysmt.element.molecule import _singular_molecule_type_to_plural

    atom_chain_index, _ = infer_chain_indices_from_topology(topology)
    molecule_index_from_group = topology.groups["molecule_index"].to_numpy(dtype=np.int64, na_value=-1)
    group_index_from_atom = topology.atoms["group_index"].to_numpy(dtype=np.int64, na_value=-1)
    molecule_types = topology.molecules["molecule_type"].to_numpy(dtype=object)

    if topology.n_chains == 1 and topology.n_molecules > 0:
        if np.all(atom_chain_index == atom_chain_index[0]):
            return np.array(["system"], dtype=object)

    output = []
    for chain_index in range(topology.n_chains):
        atom_indices = np.where(atom_chain_index == chain_index)[0]
        if len(atom_indices) == 0:
            output.append("unknown")
            continue
        chain_group_indices = np.unique(group_index_from_atom[atom_indices])
        chain_group_indices = chain_group_indices[chain_group_indices >= 0]
        if len(chain_group_indices) == 0:
            output.append("unknown")
            continue
        chain_molecule_indices = np.unique(molecule_index_from_group[chain_group_indices])
        chain_molecule_indices = chain_molecule_indices[chain_molecule_indices >= 0]
        chain_molecule_types = molecule_types[chain_molecule_indices].tolist()

        aux = []
        array_molecule_types = np.array(chain_molecule_types, dtype=object)
        for aux_type in [
            "protein",
            "peptide",
            "dna",
            "rna",
            "polysaccharide",
            "small molecule",
            "lipid",
            "ion",
            "water",
            "unknown",
        ]:
            if aux_type in chain_molecule_types:
                counter = np.sum(array_molecule_types == aux_type)
                if counter == 1 or aux_type == "water":
                    aux.append(aux_type)
                else:
                    aux.append(_singular_molecule_type_to_plural[aux_type])
        output.append(" + ".join(aux))

    return np.array(output, dtype=object)



def _needs_columns(table, columns):
    return any(column not in table.columns for column in columns)



def prepare_topology_for_molecule_queries(topology, *, element="molecule", redefine_indices=False, redefine_names=False, redefine_types=False):
    need_groups = redefine_indices or redefine_names or redefine_types or _needs_columns(topology.groups, ["molecule_index"])
    need_components = redefine_indices or redefine_names or redefine_types or _needs_columns(
        topology.groups, ["component_index"]
    ) or _needs_columns(topology.components, ["component_type", "component_name"])
    need_molecules = redefine_indices or redefine_names or redefine_types or _needs_columns(
        topology.molecules, ["molecule_name", "molecule_type"]
    )
    need_chains = element == "chain" and (
        _needs_columns(topology.atoms, ["chain_index"])
        or _needs_columns(topology.groups, ["chain_index"])
    )
    need_entities = element == "entity" and (
        _needs_columns(topology.molecules, ["entity_index"])
        or _needs_columns(topology.entities, ["entity_name", "entity_type"])
    )

    if not any([need_groups, need_components, need_molecules, need_chains, need_entities]):
        return topology

    tmp_topology = topology.copy()

    if need_groups:
        tmp_topology.rebuild_groups(redefine_ids=False, redefine_types=True)
    if need_components:
        tmp_topology.rebuild_components(
            redefine_indices=True,
            redefine_ids=False,
            redefine_types=True,
            redefine_names=True,
            force=True,
        )
    if need_molecules:
        tmp_topology.rebuild_molecules(
            redefine_indices=True,
            redefine_ids=False,
            redefine_names=True,
            redefine_types=True,
            force=True,
        )
    if need_chains:
        tmp_topology.rebuild_chains(
            redefine_indices=True,
            redefine_ids=False,
            redefine_names=True,
            redefine_types=True,
        )
    if need_entities:
        tmp_topology.rebuild_entities(
            redefine_indices=True,
            redefine_ids=False,
            redefine_names=True,
            redefine_types=True,
            force=True,
        )

    return tmp_topology



def project_molecule_index_from_topology(topology, *, element="molecule", redefine_indices=False):
    tmp_topology = prepare_topology_for_molecule_queries(
        topology, element=element, redefine_indices=redefine_indices
    )

    molecule_index_from_group = tmp_topology.groups["molecule_index"].to_numpy(dtype=np.int64, na_value=-1)

    if element == "group":
        return molecule_index_from_group.tolist()
    if element == "molecule":
        return list(range(tmp_topology.n_molecules))
    if element == "atom":
        group_index_from_atom = tmp_topology.atoms["group_index"].to_numpy(dtype=np.int64, na_value=-1)
        return molecule_index_from_group[group_index_from_atom].tolist()
    if element == "component":
        component_index_from_group = tmp_topology.groups["component_index"].to_numpy(dtype=np.int64, na_value=-1)
        output = np.full(tmp_topology.n_components, -1, dtype=np.int64)
        for group_index, component_index in enumerate(component_index_from_group):
            if component_index >= 0 and output[component_index] < 0:
                output[component_index] = molecule_index_from_group[group_index]
        return output.tolist()
    if element == "chain":
        chain_index_from_group = tmp_topology.groups["chain_index"].to_numpy(dtype=np.int64, na_value=-1)
        output = []
        for chain_index in range(tmp_topology.n_chains):
            group_indices = np.where(chain_index_from_group == chain_index)[0]
            chain_molecule_indices = np.unique(molecule_index_from_group[group_indices])
            chain_molecule_indices = chain_molecule_indices[chain_molecule_indices >= 0]
            output.append(chain_molecule_indices.tolist())
        return output
    if element == "entity":
        entity_index_from_molecule = tmp_topology.molecules["entity_index"].to_numpy(dtype=np.int64, na_value=-1)
        return [np.where(entity_index_from_molecule == entity_index)[0].tolist() for entity_index in range(tmp_topology.n_entities)]

    raise NotImplementedError



def project_molecule_name_from_topology(topology, *, element="molecule", redefine_indices=False, redefine_names=False):
    tmp_topology = prepare_topology_for_molecule_queries(
        topology,
        element=element,
        redefine_indices=redefine_indices,
        redefine_names=redefine_names,
    )
    molecule_names = tmp_topology.molecules["molecule_name"].to_numpy(dtype=object)
    if element == "molecule":
        return molecule_names.tolist()
    molecule_index = project_molecule_index_from_topology(tmp_topology, element=element, redefine_indices=False)
    if element in ["chain", "entity"]:
        return [[molecule_names[ii] for ii in aux] for aux in molecule_index]
    return molecule_names[np.asarray(molecule_index, dtype=np.int64)].tolist()



def project_molecule_type_from_topology(topology, *, element="molecule", redefine_indices=False, redefine_types=False):
    tmp_topology = prepare_topology_for_molecule_queries(
        topology,
        element=element,
        redefine_indices=redefine_indices,
        redefine_types=redefine_types,
    )
    molecule_types = tmp_topology.molecules["molecule_type"].to_numpy(dtype=object)
    if element == "molecule":
        return molecule_types.tolist()
    molecule_index = project_molecule_index_from_topology(tmp_topology, element=element, redefine_indices=False)
    if element in ["chain", "entity"]:
        return [[molecule_types[ii] for ii in aux] for aux in molecule_index]
    return molecule_types[np.asarray(molecule_index, dtype=np.int64)].tolist()



def prepare_topology_for_entity_queries(topology, *, redefine_indices=False, redefine_names=False, redefine_types=False):
    return prepare_topology_for_molecule_queries(
        topology,
        element="entity",
        redefine_indices=redefine_indices,
        redefine_names=redefine_names,
        redefine_types=redefine_types,
    )



def project_entity_index_from_topology(topology, *, element="entity", redefine_indices=False):
    tmp_topology = prepare_topology_for_entity_queries(
        topology,
        redefine_indices=redefine_indices,
        redefine_names=False,
        redefine_types=False,
    )

    entity_index_from_molecule = tmp_topology.molecules["entity_index"].to_numpy(dtype=np.int64, na_value=-1)

    if element == "entity":
        return list(range(tmp_topology.n_entities))
    if element == "molecule":
        return entity_index_from_molecule.tolist()
    if element == "atom":
        molecule_index_from_group = tmp_topology.groups["molecule_index"].to_numpy(dtype=np.int64, na_value=-1)
        group_index_from_atom = tmp_topology.atoms["group_index"].to_numpy(dtype=np.int64, na_value=-1)
        molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
        return entity_index_from_molecule[molecule_index_from_atom].tolist()

    raise NotImplementedError



def project_entity_name_from_topology(topology, *, element="entity", redefine_indices=False, redefine_names=False):
    tmp_topology = prepare_topology_for_entity_queries(
        topology,
        redefine_indices=redefine_indices,
        redefine_names=redefine_names,
        redefine_types=False,
    )

    entity_names = tmp_topology.entities["entity_name"].to_numpy(dtype=object)

    if element == "entity":
        return entity_names.tolist()

    entity_index = project_entity_index_from_topology(tmp_topology, element=element, redefine_indices=False)
    return entity_names[np.asarray(entity_index, dtype=np.int64)].tolist()



def project_entity_type_from_topology(topology, *, element="entity", redefine_indices=False, redefine_types=False):
    tmp_topology = prepare_topology_for_entity_queries(
        topology,
        redefine_indices=redefine_indices,
        redefine_names=False,
        redefine_types=redefine_types,
    )

    entity_types = tmp_topology.entities["entity_type"].to_numpy(dtype=object)

    if element == "entity":
        return entity_types.tolist()

    entity_index = project_entity_index_from_topology(tmp_topology, element=element, redefine_indices=False)
    return entity_types[np.asarray(entity_index, dtype=np.int64)].tolist()



def prepare_topology_for_component_queries(topology, *, redefine_indices=False, redefine_names=False, redefine_types=False):
    need_groups = redefine_indices or redefine_names or redefine_types or _needs_columns(topology.groups, ["group_type"])
    need_components = redefine_indices or redefine_names or redefine_types or _needs_columns(
        topology.groups, ["component_index"]
    ) or _needs_columns(topology.components, ["component_type", "component_name"])

    if not any([need_groups, need_components]):
        return topology

    tmp_topology = topology.copy()

    if need_groups:
        tmp_topology.rebuild_groups(redefine_ids=False, redefine_types=True)
    if need_components:
        tmp_topology.rebuild_components(
            redefine_indices=True,
            redefine_ids=False,
            redefine_types=True,
            redefine_names=True,
            force=True,
        )

    return tmp_topology



def project_component_index_from_topology(topology, *, element="component", redefine_indices=False):
    if element == "atom" and redefine_indices:
        atom_component_index, _ = infer_component_indices_from_topology(topology)
        return atom_component_index.tolist()

    tmp_topology = prepare_topology_for_component_queries(topology, redefine_indices=redefine_indices)

    component_index_from_group = tmp_topology.groups["component_index"].to_numpy(dtype=np.int64, na_value=-1)

    if element == "component":
        return list(range(tmp_topology.n_components))
    if element == "group":
        return component_index_from_group.tolist()
    if element == "atom":
        group_index_from_atom = tmp_topology.atoms["group_index"].to_numpy(dtype=np.int64, na_value=-1)
        return component_index_from_group[group_index_from_atom].tolist()

    raise NotImplementedError



def project_component_name_from_topology(topology, *, element="component", redefine_indices=False, redefine_names=False):
    tmp_topology = prepare_topology_for_component_queries(
        topology,
        redefine_indices=redefine_indices,
        redefine_names=redefine_names,
        redefine_types=redefine_indices,
    )

    component_names = tmp_topology.components["component_name"].to_numpy(dtype=object)

    if element == "component":
        return component_names.tolist()

    component_index = project_component_index_from_topology(tmp_topology, element=element, redefine_indices=False)
    return component_names[np.asarray(component_index, dtype=np.int64)].tolist()



def project_component_type_from_topology(topology, *, element="component", redefine_indices=False, redefine_types=False):
    tmp_topology = prepare_topology_for_component_queries(
        topology,
        redefine_indices=redefine_indices,
        redefine_names=False,
        redefine_types=redefine_types,
    )

    component_types = tmp_topology.components["component_type"].to_numpy(dtype=object)

    if element == "component":
        return component_types.tolist()

    component_index = project_component_index_from_topology(tmp_topology, element=element, redefine_indices=False)
    return component_types[np.asarray(component_index, dtype=np.int64)].tolist()



def prepare_topology_for_chain_queries(topology, *, redefine_indices=False, redefine_names=False, redefine_types=False):
    need_groups = redefine_indices or redefine_names or redefine_types or _needs_columns(topology.groups, ["molecule_index", "chain_index"])
    need_components = redefine_types or _needs_columns(topology.groups, ["component_index"]) or _needs_columns(
        topology.components, ["component_type", "component_name"]
    )
    need_molecules = redefine_types or _needs_columns(topology.molecules, ["molecule_name", "molecule_type"])
    need_chains = redefine_indices or redefine_names or redefine_types or _needs_columns(
        topology.chains, ["chain_name", "chain_type"]
    ) or _needs_columns(topology.atoms, ["chain_index"])
    need_entities = False

    if not any([need_groups, need_components, need_molecules, need_chains]):
        return topology

    tmp_topology = topology.copy()

    if need_groups:
        tmp_topology.rebuild_groups(redefine_ids=False, redefine_types=True)
    if need_components:
        tmp_topology.rebuild_components(
            redefine_indices=True,
            redefine_ids=False,
            redefine_types=True,
            redefine_names=True,
            force=True,
        )
    if need_molecules:
        tmp_topology.rebuild_molecules(
            redefine_indices=True,
            redefine_ids=False,
            redefine_names=True,
            redefine_types=True,
            force=True,
        )
    if need_chains:
        tmp_topology.rebuild_chains(
            redefine_indices=True,
            redefine_ids=False,
            redefine_names=True,
            redefine_types=True,
        )

    return tmp_topology



def project_chain_index_from_topology(topology, *, element="atom", redefine_indices=False):
    tmp_topology = prepare_topology_for_chain_queries(topology, redefine_indices=redefine_indices)

    atom_chain_index = tmp_topology.atoms["chain_index"].to_numpy(dtype=np.int64, na_value=-1)
    group_chain_index = tmp_topology.groups["chain_index"].to_numpy(dtype=np.int64, na_value=-1)

    if element == "atom":
        return atom_chain_index.tolist()
    if element == "group":
        return group_chain_index.tolist()
    if element == "chain":
        return list(range(tmp_topology.n_chains))
    if element == "component":
        component_index_from_group = tmp_topology.groups["component_index"].to_numpy(dtype=np.int64, na_value=-1)
        output = np.full(tmp_topology.n_components, -1, dtype=np.int64)
        for group_index, component_index in enumerate(component_index_from_group):
            if component_index >= 0 and output[component_index] < 0:
                output[component_index] = group_chain_index[group_index]
        return output.tolist()
    if element == "molecule":
        molecule_index_from_group = tmp_topology.groups["molecule_index"].to_numpy(dtype=np.int64, na_value=-1)
        output = np.full(tmp_topology.n_molecules, -1, dtype=np.int64)
        for group_index, molecule_index in enumerate(molecule_index_from_group):
            if molecule_index >= 0 and output[molecule_index] < 0:
                output[molecule_index] = group_chain_index[group_index]
        return output.tolist()
    if element == "entity":
        entity_index_from_molecule = tmp_topology.molecules["entity_index"].to_numpy(dtype=np.int64, na_value=-1)
        molecule_chain_index = project_chain_index_from_topology(tmp_topology, element="molecule", redefine_indices=False)
        output = []
        for entity_index in range(tmp_topology.n_entities):
            molecule_indices = np.where(entity_index_from_molecule == entity_index)[0]
            chains = sorted(set(molecule_chain_index[ii] for ii in molecule_indices if molecule_chain_index[ii] >= 0))
            output.append(chains)
        return output

    raise NotImplementedError



def project_chain_name_from_topology(topology, *, element="chain", redefine_indices=False, redefine_names=False):
    tmp_topology = prepare_topology_for_chain_queries(
        topology,
        redefine_indices=redefine_indices,
        redefine_names=redefine_names,
        redefine_types=False,
    )
    chain_names = tmp_topology.chains["chain_name"].to_numpy(dtype=object)
    if element == "chain":
        return chain_names.tolist()
    chain_index = project_chain_index_from_topology(tmp_topology, element=element, redefine_indices=False)
    if element == "entity":
        return [[chain_names[ii] for ii in aux] for aux in chain_index]
    return chain_names[np.asarray(chain_index, dtype=np.int64)].tolist()



def project_chain_type_from_topology(topology, *, element="chain", redefine_indices=False, redefine_types=False):
    tmp_topology = prepare_topology_for_chain_queries(
        topology,
        redefine_indices=redefine_indices,
        redefine_names=False,
        redefine_types=redefine_types,
    )
    chain_types = tmp_topology.chains["chain_type"].to_numpy(dtype=object)
    if element == "chain":
        return chain_types.tolist()
    chain_index = project_chain_index_from_topology(tmp_topology, element=element, redefine_indices=False)
    if element == "entity":
        return [[chain_types[ii] for ii in aux] for aux in chain_index]
    return chain_types[np.asarray(chain_index, dtype=np.int64)].tolist()
