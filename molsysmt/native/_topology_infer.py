import numpy as np
import pandas as pd


def fallback_ids(n_items):
    return np.arange(n_items, dtype=int).astype(str)


def molecule_indices_from_atoms(topology):
    """Project stored stable membership without consulting chemical states."""
    from ._atom_molecules import resolve

    return resolve(topology)


def _group_atom_names(topology):
    atom_group_indices = topology.atoms["group_index"].to_numpy(
        dtype=np.int64, na_value=-1
    )
    atom_names = topology.atoms["atom_name"].to_numpy(dtype=object)
    names_by_group = {}
    for atom_name, group_index in zip(atom_names, atom_group_indices):
        if group_index < 0:
            continue
        names_by_group.setdefault(int(group_index), set()).add(atom_name)
    return names_by_group


def infer_group_types_from_topology(topology):
    from molsysmt.element.group import get_group_type_from_group_name
    from molsysmt.element.group.small_molecule.group_names import (
        group_names as reserved_small_molecule_names,
    )

    group_names = topology.groups["group_name"].to_numpy(dtype=object)
    atom_names_by_group = _group_atom_names(topology)

    output = []
    for group_index, group_name in enumerate(group_names):
        group_type = get_group_type_from_group_name(group_name)
        if (
            group_type == "small molecule"
            and group_name in reserved_small_molecule_names
        ):
            atom_names = atom_names_by_group.get(group_index, set())
            if {"N", "CA", "C", "O", "CB"}.issubset(atom_names):
                group_type = "amino acid"
        output.append(group_type)

    return np.array(output, dtype=object)


def project_group_type_from_topology(
    topology, *, element="group", redefine_types=False
):
    if redefine_types or _needs_columns(topology.groups, ["group_type"]):
        tmp_topology = topology.copy()
        tmp_topology.rebuild_groups(redefine_ids=False, redefine_types=True)
    else:
        tmp_topology = topology

    group_types = tmp_topology.groups["group_type"].to_numpy(dtype=object)

    if element == "group":
        return group_types.tolist()

    if element == "atom":
        group_index_from_atom = tmp_topology.atoms["group_index"].to_numpy(
            dtype=np.int64, na_value=-1
        )
        return group_types[group_index_from_atom].tolist()

    raise NotImplementedError


def infer_component_indices_from_topology(topology):
    """
    Return per-atom component_index array.

    Architecture invariant: component_index is atom-aligned state data.
    Groups do NOT have a component_index column.

    Parameters
    ----------
    topology : object
        Argument topology.
    """
    return _component_indices_from_bonds(
        topology.n_atoms, topology._get_chemical_state_bonds()
    )


def _component_indices_from_bonds(n_atoms, bonds):
    """Delegate graph partitioning to its chemical-state owner during migration."""
    from ._chemical_components import indices_from_bonds

    return indices_from_bonds(n_atoms, bonds)


def _unchanged_component_rows(old_indices, new_indices, n_old, n_new):
    """Delegate exact atom-set matching to its chemical-state owner."""
    from ._chemical_components import unchanged_rows

    return unchanged_rows(old_indices, new_indices, n_old, n_new)


def _component_index_per_group(topology):
    from ._chemical_components import group_components

    return group_components(topology, topology._get_component_indices())


def infer_component_types_from_topology(topology):
    from ._chemical_components import infer_types

    return infer_types(
        topology.groups["group_name"].to_numpy(dtype=object),
        topology.groups["group_type"].to_numpy(dtype=object),
        _component_index_per_group(topology),
        topology.n_components,
    )


def infer_component_names_from_topology(topology):
    from ._chemical_components import infer_names

    return infer_names(
        topology.groups["group_name"].to_numpy(dtype=object),
        _component_index_per_group(topology),
        topology.components["component_type"].to_numpy(dtype=object),
    )


def infer_molecule_indices_from_topology(topology):
    """
    Partition groups into molecules, decoupled from connected components.

    A new molecule begins whenever:
    - the chain changes, or
    - the group_type transitions out of or into the chain-polymer category
      {'amino acid', 'terminal capping', 'unknown', 'nucleotide',
       'saccharide', 'lipid'}, or
    - the group_type is standalone {'ion', 'water', 'small molecule'}
      (each group = its own molecule).

    This decouples molecule identity from bond connectivity, so that a
    covalently or coordinatively bonded complex (e.g. MnATP bound to a
    protein, or a covalent drug) becomes one component but several
    molecules of different types.

    Parameters
    ----------
    topology : object
        Argument topology.
    """
    _CHAIN_POLYMER = frozenset(
        {
            "amino acid",
            "terminal capping",
            "unknown",
            "nucleotide",
            "saccharide",
            "lipid",
        }
    )
    _STANDALONE = frozenset({"ion", "water", "small molecule"})

    n_groups = topology.n_groups
    if n_groups == 0:
        return np.empty(0, dtype=np.int64)

    # Architecture invariant: chain_index is an ATOM-level attribute only.
    # Groups do NOT have a chain_index column. Derive per-group chain from atoms.
    from ._chain_groups import by_group, uses_declared_hierarchy

    chain_indices = np.full(n_groups, -1, dtype=np.int64)
    if uses_declared_hierarchy(topology):
        for group, chains in enumerate(by_group(topology)):
            if len(chains) > 1 and pd.isna(
                topology.groups.loc[group, "molecule_index"]
            ):
                from molsysmt._private.smonitor import StructuralInconsistencyError

                raise StructuralInconsistencyError(
                    reason="Declare molecule ownership for groups shared by multiple chains."
                )
            if chains:
                chain_indices[group] = chains[0]
    else:
        atom_df = topology.atoms[["group_index", "chain_index"]].dropna()
        grp_chain = atom_df.groupby("group_index", sort=False)["chain_index"].first()
        chain_indices[grp_chain.index.to_numpy(dtype=np.int64)] = grp_chain.to_numpy(
            dtype=np.int64
        )
    group_types = topology.groups["group_type"].to_numpy(dtype=object)

    molecule_index_of_groups = np.empty(n_groups, dtype=np.int64)
    current_mol = 0
    prev_chain = -2  # sentinel: guaranteed ≠ any real chain
    prev_gtype = None

    for g in range(n_groups):
        gtype = "unknown" if pd.isna(group_types[g]) else group_types[g]
        chain = chain_indices[g]

        if gtype in _STANDALONE:
            # Each standalone group is its own molecule; always bump counter.
            if g > 0:
                current_mol += 1
        else:
            # Chain-polymer (or completely unknown) type.
            new_chain = chain != prev_chain
            leaving_standalone = prev_gtype in _STANDALONE
            if g == 0 or new_chain or leaving_standalone:
                if g > 0:
                    current_mol += 1

        molecule_index_of_groups[g] = current_mol
        prev_chain = chain
        prev_gtype = gtype

    return molecule_index_of_groups


def complete_missing_molecule_membership(topology):
    """Fill missing group owners while retaining declared occurrence slots."""
    missing = topology.groups["molecule_index"].isna()
    if not missing.any():
        return
    inferred = infer_molecule_indices_from_topology(topology)
    mapping = {}
    for group in topology.groups.index[missing]:
        key = int(inferred[group])
        if key not in mapping:
            molecule = topology.n_molecules
            topology.molecules.loc[molecule, "molecule_id"] = str(molecule)
            topology.molecules.loc[molecule, "molecule_name"] = pd.NA
            topology.molecules.loc[molecule, "molecule_type"] = pd.NA
            topology.molecules.loc[molecule, "entity_index"] = pd.NA
            mapping[key] = molecule
        topology.groups.loc[group, "molecule_index"] = mapping[key]


def infer_molecule_types_from_topology(topology):
    """
    Infer molecule_type from the group_types within each molecule.

    Derives type directly from the groups belonging to the molecule,
    not from the component the molecule happens to be bonded into.

    Parameters
    ----------
    topology : object
        Argument topology.
    """
    from molsysmt.element.component.get_component_type import (
        _get_component_type_from_group_names_and_types,
    )

    if topology.n_groups == 0 and topology.n_atoms == 0:
        return np.array(["unknown"] * topology.n_molecules, dtype=object)
    if topology.n_groups == 0:
        return (
            topology.molecules["molecule_type"]
            .fillna("unknown")
            .to_numpy(dtype=object, copy=True)
        )
    molecule_index_of_groups = topology.groups["molecule_index"].to_numpy(
        dtype=np.int64, na_value=-1
    )
    group_names = topology.groups["group_name"].to_numpy(dtype=object)
    group_types = topology.groups["group_type"].to_numpy(dtype=object)

    output = np.empty(topology.n_molecules, dtype=object)
    for molecule_index in range(topology.n_molecules):
        mask = molecule_index_of_groups == molecule_index
        if not np.any(mask):
            output[molecule_index] = "unknown"
            continue
        output[molecule_index] = _get_component_type_from_group_names_and_types(
            group_names[mask], group_types[mask]
        )
    return output


def infer_molecule_names_from_topology(topology):
    """
    Infer molecule_name from the group_names/types within each molecule.

    Parameters
    ----------
    topology : object
        Argument topology.
    """
    if topology.n_groups == 0 and topology.n_atoms == 0:
        return np.array(
            [f"unknown {i}" for i in range(topology.n_molecules)], dtype=object
        )
    if topology.n_groups == 0:
        values = topology.molecules["molecule_name"].to_numpy(dtype=object, copy=True)
        for index, value in enumerate(values):
            if pd.isna(value):
                values[index] = f"unknown {index}"
        return values
    molecule_index_of_groups = topology.groups["molecule_index"].to_numpy(
        dtype=np.int64, na_value=-1
    )
    molecule_types = topology.molecules["molecule_type"].to_numpy(dtype=object)
    group_names = topology.groups["group_name"].to_numpy(dtype=object)

    counters = {"peptide": 0, "protein": 0, "small molecule": 0, "unknown": 0}
    peptides = {}
    output = np.empty(topology.n_molecules, dtype=object)

    for molecule_index in range(topology.n_molecules):
        mask = molecule_index_of_groups == molecule_index
        if not np.any(mask):
            output[molecule_index] = f"unknown {counters['unknown']}"
            counters["unknown"] += 1
            continue
        mol_type = molecule_types[molecule_index]
        if mol_type is pd.NA or mol_type is None:
            mol_type = "unknown"
        names_in_mol = group_names[mask].tolist()

        if mol_type == "peptide":
            peptide_key = ",".join(names_in_mol)
            if peptide_key in peptides:
                name = peptides[peptide_key]
            else:
                name = f"peptide {counters['peptide']}"
                peptides[peptide_key] = name
                counters["peptide"] += 1
        elif mol_type in ("protein", "small molecule"):
            name = f"{mol_type} {counters[mol_type]}"
            counters[mol_type] += 1
        elif mol_type in ("ion", "lipid"):
            name = names_in_mol[0] if names_in_mol else f"unknown {counters['unknown']}"
        elif mol_type == "water":
            name = "water"
        else:
            name = f"unknown {counters['unknown']}"
            counters["unknown"] += 1

        output[molecule_index] = name
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
    entity_index_of_molecules = topology.molecules["entity_index"].to_numpy(
        dtype=np.int64, na_value=-1
    )
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
    entity_index_of_molecules = topology.molecules["entity_index"].to_numpy(
        dtype=np.int64, na_value=-1
    )
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
    """
    Return per-atom chain_index array.

    Architecture invariant: chain_index is defined at the ATOM level only.
    Groups do NOT have a chain_index column.

    Parameters
    ----------
    topology : object
        Argument topology.
    """
    n_atoms = topology.n_atoms

    if n_atoms == 0:
        return np.empty(0, dtype=np.int64)

    atom_chain_index = topology.atoms["chain_index"].to_numpy(
        dtype=np.int64, na_value=-1
    )
    if np.all(atom_chain_index < 0):
        atom_chain_index = np.zeros(n_atoms, dtype=np.int64)
    else:
        atom_chain_index = atom_chain_index.copy()
        atom_chain_index[atom_chain_index < 0] = 0

    return atom_chain_index


def infer_chain_ids_from_topology(topology):
    from molsysmt.element.chain.chain_names import _alphabetic_chain_id

    return np.array(
        [_alphabetic_chain_id(i) for i in range(topology.n_chains)], dtype=object
    )


def infer_chain_names_from_topology(topology):
    return infer_chain_ids_from_topology(topology)


def infer_chain_types_from_topology(topology):
    from molsysmt.element.molecule import _singular_molecule_type_to_plural

    atom_chain_index = infer_chain_indices_from_topology(topology)
    molecule_index_from_group = topology.groups["molecule_index"].to_numpy(
        dtype=np.int64, na_value=-1
    )
    group_index_from_atom = topology.atoms["group_index"].to_numpy(
        dtype=np.int64, na_value=-1
    )
    molecule_types = topology.molecules["molecule_type"].to_numpy(dtype=object)

    if topology.n_atoms and topology.n_chains == 1 and topology.n_molecules > 0:
        if np.all(atom_chain_index == atom_chain_index[0]):
            return np.array(["system"], dtype=object)

    from ._chain_groups import by_chain, uses_declared_hierarchy

    declared = by_chain(topology) if uses_declared_hierarchy(topology) else None
    output = []
    for chain_index in range(topology.n_chains):
        atom_indices = np.where(atom_chain_index == chain_index)[0]
        chain_group_indices = (
            declared[chain_index]
            if declared is not None
            else np.unique(group_index_from_atom[atom_indices])
        )
        chain_group_indices = chain_group_indices[chain_group_indices >= 0]
        if len(chain_group_indices) == 0:
            output.append("unknown")
            continue
        chain_molecule_indices = np.unique(
            molecule_index_from_group[chain_group_indices]
        )
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
    for column in columns:
        if column not in table.columns:
            return True
        if table[column].isnull().any():
            return True
    return False


def prepare_topology_for_molecule_queries(
    topology,
    *,
    element="molecule",
    redefine_indices=False,
    redefine_names=False,
    redefine_types=False,
):
    need_groups = (
        redefine_indices
        or redefine_names
        or redefine_types
        or _needs_columns(topology.groups, ["molecule_index"])
    )
    need_components = (
        redefine_indices
        or redefine_names
        or redefine_types
        or topology._component_indices_are_missing()
        or _needs_columns(topology.components, ["component_type", "component_name"])
    )
    need_molecules = (
        redefine_indices
        or redefine_names
        or redefine_types
        or (
            topology.n_atoms > 0
            and topology.n_groups == 0
            and topology.n_molecules == 0
        )
        or _needs_columns(topology.molecules, ["molecule_name", "molecule_type"])
    )
    need_chains = element == "chain" and (
        _needs_columns(topology.atoms, ["chain_index"])
        or _needs_columns(topology.groups, ["chain_index"])
    )
    need_entities = element == "entity" and (
        _needs_columns(topology.molecules, ["entity_index"])
        or _needs_columns(topology.entities, ["entity_name", "entity_type"])
    )

    if not any(
        [need_groups, need_components, need_molecules, need_chains, need_entities]
    ):
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


def project_molecule_index_from_topology(
    topology, *, element="molecule", redefine_indices=False
):
    tmp_topology = prepare_topology_for_molecule_queries(
        topology, element=element, redefine_indices=redefine_indices
    )

    molecule_index_from_group = tmp_topology.groups["molecule_index"].to_numpy(
        dtype=np.int64, na_value=-1
    )

    if element == "group":
        return molecule_index_from_group.tolist()
    if element == "molecule":
        return list(range(tmp_topology.n_molecules))
    if element == "atom":
        return molecule_indices_from_atoms(tmp_topology).tolist()
    if element == "component":
        if tmp_topology.n_groups == 0:
            return list(range(tmp_topology.n_molecules))
        component_index_from_group = _component_index_per_group(tmp_topology)
        output = np.full(tmp_topology.n_components, -1, dtype=np.int64)
        for group_index, component_index in enumerate(component_index_from_group):
            if component_index >= 0 and output[component_index] < 0:
                output[component_index] = molecule_index_from_group[group_index]
        return output.tolist()
    if element == "chain":
        # chain_index is atom-level; derive per-group from atoms
        _adf = tmp_topology.atoms[["group_index", "chain_index"]].dropna()
        _gc = _adf.groupby("group_index", sort=False)["chain_index"].first()
        chain_index_from_group = np.full(tmp_topology.n_groups, -1, dtype=np.int64)
        chain_index_from_group[_gc.index.to_numpy(dtype=np.int64)] = _gc.to_numpy(
            dtype=np.int64
        )
        output = []
        for chain_index in range(tmp_topology.n_chains):
            group_indices = np.where(chain_index_from_group == chain_index)[0]
            chain_molecule_indices = np.unique(molecule_index_from_group[group_indices])
            chain_molecule_indices = chain_molecule_indices[chain_molecule_indices >= 0]
            output.append(chain_molecule_indices.tolist())
        return output
    if element == "entity":
        entity_index_from_molecule = tmp_topology.molecules["entity_index"].to_numpy(
            dtype=np.int64, na_value=-1
        )
        return [
            np.where(entity_index_from_molecule == entity_index)[0].tolist()
            for entity_index in range(tmp_topology.n_entities)
        ]

    raise NotImplementedError


def project_molecule_name_from_topology(
    topology, *, element="molecule", redefine_indices=False, redefine_names=False
):
    tmp_topology = prepare_topology_for_molecule_queries(
        topology,
        element=element,
        redefine_indices=redefine_indices,
        redefine_names=redefine_names,
    )
    molecule_names = tmp_topology.molecules["molecule_name"].to_numpy(dtype=object)
    if element == "molecule":
        return molecule_names.tolist()
    molecule_index = project_molecule_index_from_topology(
        tmp_topology, element=element, redefine_indices=False
    )
    if element in ["chain", "entity"]:
        return [[molecule_names[ii] for ii in aux] for aux in molecule_index]
    return molecule_names[np.asarray(molecule_index, dtype=np.int64)].tolist()


def project_molecule_type_from_topology(
    topology, *, element="molecule", redefine_indices=False, redefine_types=False
):
    tmp_topology = prepare_topology_for_molecule_queries(
        topology,
        element=element,
        redefine_indices=redefine_indices,
        redefine_types=redefine_types,
    )
    molecule_types = tmp_topology.molecules["molecule_type"].to_numpy(dtype=object)
    if element == "molecule":
        return molecule_types.tolist()
    molecule_index = project_molecule_index_from_topology(
        tmp_topology, element=element, redefine_indices=False
    )
    if element in ["chain", "entity"]:
        return [[molecule_types[ii] for ii in aux] for aux in molecule_index]
    return molecule_types[np.asarray(molecule_index, dtype=np.int64)].tolist()


def prepare_topology_for_entity_queries(
    topology, *, redefine_indices=False, redefine_names=False, redefine_types=False
):
    return prepare_topology_for_molecule_queries(
        topology,
        element="entity",
        redefine_indices=redefine_indices,
        redefine_names=redefine_names,
        redefine_types=redefine_types,
    )


def project_entity_index_from_topology(
    topology, *, element="entity", redefine_indices=False
):
    tmp_topology = prepare_topology_for_entity_queries(
        topology,
        redefine_indices=redefine_indices,
        redefine_names=False,
        redefine_types=False,
    )

    entity_index_from_molecule = tmp_topology.molecules["entity_index"].to_numpy(
        dtype=np.int64, na_value=-1
    )

    if element == "entity":
        return list(range(tmp_topology.n_entities))
    if element == "molecule":
        return entity_index_from_molecule.tolist()
    if element == "atom":
        molecule_index_from_atom = molecule_indices_from_atoms(tmp_topology)
        return entity_index_from_molecule[molecule_index_from_atom].tolist()

    raise NotImplementedError


def project_entity_name_from_topology(
    topology, *, element="entity", redefine_indices=False, redefine_names=False
):
    tmp_topology = prepare_topology_for_entity_queries(
        topology,
        redefine_indices=redefine_indices,
        redefine_names=redefine_names,
        redefine_types=False,
    )

    entity_names = tmp_topology.entities["entity_name"].to_numpy(dtype=object)

    if element == "entity":
        return entity_names.tolist()

    entity_index = project_entity_index_from_topology(
        tmp_topology, element=element, redefine_indices=False
    )
    return entity_names[np.asarray(entity_index, dtype=np.int64)].tolist()


def project_entity_type_from_topology(
    topology, *, element="entity", redefine_indices=False, redefine_types=False
):
    tmp_topology = prepare_topology_for_entity_queries(
        topology,
        redefine_indices=redefine_indices,
        redefine_names=False,
        redefine_types=redefine_types,
    )

    entity_types = tmp_topology.entities["entity_type"].to_numpy(dtype=object)

    if element == "entity":
        return entity_types.tolist()

    entity_index = project_entity_index_from_topology(
        tmp_topology, element=element, redefine_indices=False
    )
    return entity_types[np.asarray(entity_index, dtype=np.int64)].tolist()


def prepare_topology_for_component_queries(
    topology, *, redefine_indices=False, redefine_names=False, redefine_types=False
):
    need_groups = (
        redefine_indices
        or redefine_names
        or redefine_types
        or _needs_columns(topology.groups, ["group_type"])
    )
    # Component membership is atom-aligned state data, never group storage.
    need_components = (
        redefine_indices
        or redefine_names
        or redefine_types
        or topology._component_indices_are_missing()
        or _needs_columns(topology.components, ["component_type", "component_name"])
    )

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


def project_component_index_from_topology(
    topology, *, element="component", redefine_indices=False
):
    if element == "atom" and redefine_indices:
        atom_component_index = infer_component_indices_from_topology(topology)
        return atom_component_index.tolist()

    tmp_topology = prepare_topology_for_component_queries(
        topology, redefine_indices=redefine_indices
    )

    # Derive group membership from atom-aligned state data.
    component_index_from_group = _component_index_per_group(tmp_topology)

    if element == "component":
        return list(range(tmp_topology.n_components))
    if element == "group":
        return component_index_from_group.tolist()
    if element == "atom":
        group_index_from_atom = tmp_topology.atoms["group_index"].to_numpy(
            dtype=np.int64, na_value=-1
        )
        return component_index_from_group[group_index_from_atom].tolist()

    raise NotImplementedError


def project_component_name_from_topology(
    topology, *, element="component", redefine_indices=False, redefine_names=False
):
    tmp_topology = prepare_topology_for_component_queries(
        topology,
        redefine_indices=redefine_indices,
        redefine_names=redefine_names,
        redefine_types=redefine_indices,
    )

    component_names = tmp_topology.components["component_name"].to_numpy(dtype=object)

    if element == "component":
        return component_names.tolist()

    component_index = project_component_index_from_topology(
        tmp_topology, element=element, redefine_indices=False
    )
    return component_names[np.asarray(component_index, dtype=np.int64)].tolist()


def project_component_type_from_topology(
    topology, *, element="component", redefine_indices=False, redefine_types=False
):
    tmp_topology = prepare_topology_for_component_queries(
        topology,
        redefine_indices=redefine_indices,
        redefine_names=False,
        redefine_types=redefine_types,
    )

    component_types = tmp_topology.components["component_type"].to_numpy(dtype=object)

    if element == "component":
        return component_types.tolist()

    component_index = project_component_index_from_topology(
        tmp_topology, element=element, redefine_indices=False
    )
    return component_types[np.asarray(component_index, dtype=np.int64)].tolist()


def prepare_topology_for_chain_queries(
    topology, *, redefine_indices=False, redefine_names=False, redefine_types=False
):
    # chain_index is stable atom data; component_index is atom-aligned state data.
    need_groups = (
        redefine_indices
        or redefine_names
        or redefine_types
        or _needs_columns(topology.groups, ["molecule_index"])
    )
    need_components = (
        redefine_types
        or topology._component_indices_are_missing()
        or _needs_columns(topology.components, ["component_type", "component_name"])
    )
    need_molecules = redefine_types or _needs_columns(
        topology.molecules, ["molecule_name", "molecule_type"]
    )
    need_chains = (
        redefine_indices
        or redefine_names
        or redefine_types
        or _needs_columns(topology.chains, ["chain_name", "chain_type"])
        or _needs_columns(topology.atoms, ["chain_index"])
    )

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


def project_chain_index_from_topology(
    topology, *, element="atom", redefine_indices=False
):
    tmp_topology = prepare_topology_for_chain_queries(
        topology, redefine_indices=redefine_indices
    )

    atom_chain_index = tmp_topology.atoms["chain_index"].to_numpy(
        dtype=np.int64, na_value=-1
    )
    # chain_index is atom-level; derive per-group from atoms (groups have no chain_index column)
    _adf = tmp_topology.atoms[["group_index", "chain_index"]].dropna()
    _gc = _adf.groupby("group_index", sort=False)["chain_index"].first()
    group_chain_index = np.full(tmp_topology.n_groups, -1, dtype=np.int64)
    group_chain_index[_gc.index.to_numpy(dtype=np.int64)] = _gc.to_numpy(dtype=np.int64)

    if element == "atom":
        return atom_chain_index.tolist()
    if element == "group":
        return group_chain_index.tolist()
    if element == "chain":
        return list(range(tmp_topology.n_chains))
    if element == "component":
        component_index_from_group = _component_index_per_group(tmp_topology)
        output = np.full(tmp_topology.n_components, -1, dtype=np.int64)
        for group_index, component_index in enumerate(component_index_from_group):
            if component_index >= 0 and output[component_index] < 0:
                output[component_index] = group_chain_index[group_index]
        return output.tolist()
    if element == "molecule":
        molecule_index_from_group = tmp_topology.groups["molecule_index"].to_numpy(
            dtype=np.int64, na_value=-1
        )
        output = np.full(tmp_topology.n_molecules, -1, dtype=np.int64)
        for group_index, molecule_index in enumerate(molecule_index_from_group):
            if molecule_index >= 0 and output[molecule_index] < 0:
                output[molecule_index] = group_chain_index[group_index]
        return output.tolist()
    if element == "entity":
        entity_index_from_molecule = tmp_topology.molecules["entity_index"].to_numpy(
            dtype=np.int64, na_value=-1
        )
        molecule_chain_index = project_chain_index_from_topology(
            tmp_topology, element="molecule", redefine_indices=False
        )
        output = []
        for entity_index in range(tmp_topology.n_entities):
            molecule_indices = np.where(entity_index_from_molecule == entity_index)[0]
            chains = sorted(
                set(
                    molecule_chain_index[ii]
                    for ii in molecule_indices
                    if molecule_chain_index[ii] >= 0
                )
            )
            output.append(chains)
        return output

    raise NotImplementedError


def project_chain_name_from_topology(
    topology, *, element="chain", redefine_indices=False, redefine_names=False
):
    tmp_topology = prepare_topology_for_chain_queries(
        topology,
        redefine_indices=redefine_indices,
        redefine_names=redefine_names,
        redefine_types=False,
    )
    chain_names = tmp_topology.chains["chain_name"].to_numpy(dtype=object)
    if element == "chain":
        return chain_names.tolist()
    chain_index = project_chain_index_from_topology(
        tmp_topology, element=element, redefine_indices=False
    )
    if element == "entity":
        return [[chain_names[ii] for ii in aux] for aux in chain_index]
    return chain_names[np.asarray(chain_index, dtype=np.int64)].tolist()


def project_chain_type_from_topology(
    topology, *, element="chain", redefine_indices=False, redefine_types=False
):
    tmp_topology = prepare_topology_for_chain_queries(
        topology,
        redefine_indices=redefine_indices,
        redefine_names=False,
        redefine_types=redefine_types,
    )
    chain_types = tmp_topology.chains["chain_type"].to_numpy(dtype=object)
    if element == "chain":
        return chain_types.tolist()
    chain_index = project_chain_index_from_topology(
        tmp_topology, element=element, redefine_indices=False
    )
    if element == "entity":
        return [[chain_types[ii] for ii in aux] for aux in chain_index]
    return chain_types[np.asarray(chain_index, dtype=np.int64)].tolist()
