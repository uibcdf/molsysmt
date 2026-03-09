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
