from molsysmt._private.arg_digestion import arg_digest
import numpy as np
import types

form = "molsysmt.MolSysBuilder"


def _normalize_sequence(values):
    output = []
    for value in values:
        if value is np.nan:
            output.append(None)
        elif value is None:
            output.append(None)
        else:
            try:
                if np.isnan(value):
                    output.append(None)
                    continue
            except Exception:
                pass
            if getattr(value, "__class__", None).__name__ == "NAType":
                output.append(None)
            else:
                output.append(value)
    return output


def _take(values, indices):
    if indices == "all":
        return values.tolist()
    return values[indices].tolist()


def _project(indices, target_values):
    output = []
    for index in indices:
        if index is None:
            output.append(None)
        else:
            output.append(target_values[int(index)])
    return output


@arg_digest(form=form)
def get_atom_index_from_atom(item, indices="all", skip_digestion=False):
    if indices == "all":
        return list(range(item.topology.n_atoms))
    return indices


@arg_digest(form=form)
def get_atom_id_from_atom(item, indices="all", skip_digestion=False):
    values = item.topology.atoms["atom_id"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_atom_name_from_atom(item, indices="all", skip_digestion=False):
    values = item.topology.atoms["atom_name"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_atom_type_from_atom(item, indices="all", skip_digestion=False):
    values = item.topology.atoms["atom_type"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_group_index_from_atom(item, indices="all", skip_digestion=False):
    values = item.topology.atoms["group_index"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_group_index_from_group(item, indices="all", skip_digestion=False):
    if indices == "all":
        return list(range(item.topology.n_groups))
    return indices


@arg_digest(form=form)
def get_group_id_from_group(item, indices="all", skip_digestion=False):
    values = item.topology.groups["group_id"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_group_name_from_group(item, indices="all", skip_digestion=False):
    values = item.topology.groups["group_name"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_group_type_from_group(item, indices="all", skip_digestion=False):
    values = item.topology.groups["group_type"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_chain_index_from_atom(item, indices="all", skip_digestion=False):
    values = item.topology.atoms["chain_index"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_chain_index_from_group(item, indices="all", skip_digestion=False):
    if "chain_index" not in item.topology.groups.columns:
        values = [None] * item.topology.n_groups
    else:
        values = item.topology.groups["chain_index"].to_numpy(dtype=object)
    return _normalize_sequence(_take(np.asarray(values, dtype=object), indices))


@arg_digest(form=form)
def get_chain_index_from_chain(item, indices="all", skip_digestion=False):
    if indices == "all":
        return list(range(item.topology.n_chains))
    return indices


@arg_digest(form=form)
def get_chain_id_from_chain(item, indices="all", skip_digestion=False):
    values = item.topology.chains["chain_id"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_chain_name_from_chain(item, indices="all", skip_digestion=False):
    values = item.topology.chains["chain_name"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_chain_type_from_chain(item, indices="all", skip_digestion=False):
    values = item.topology.chains["chain_type"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_molecule_index_from_group(item, indices="all", skip_digestion=False):
    values = item.topology.groups["molecule_index"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_molecule_index_from_atom(item, indices="all", skip_digestion=False):
    group_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    molecule_values = item.topology.groups["molecule_index"].to_numpy(dtype=object)
    return _normalize_sequence(_project(group_indices, molecule_values))


@arg_digest(form=form)
def get_molecule_index_from_molecule(item, indices="all", skip_digestion=False):
    if indices == "all":
        return list(range(item.topology.n_molecules))
    return indices


@arg_digest(form=form)
def get_molecule_id_from_molecule(item, indices="all", skip_digestion=False):
    values = item.topology.molecules["molecule_id"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_molecule_name_from_molecule(item, indices="all", skip_digestion=False):
    values = item.topology.molecules["molecule_name"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_molecule_type_from_molecule(item, indices="all", skip_digestion=False):
    values = item.topology.molecules["molecule_type"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_entity_index_from_molecule(item, indices="all", skip_digestion=False):
    values = item.topology.molecules["entity_index"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_entity_index_from_atom(item, indices="all", skip_digestion=False):
    molecule_indices = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
    entity_values = item.topology.molecules["entity_index"].to_numpy(dtype=object)
    return _normalize_sequence(_project(molecule_indices, entity_values))


@arg_digest(form=form)
def get_entity_index_from_entity(item, indices="all", skip_digestion=False):
    if indices == "all":
        return list(range(item.topology.n_entities))
    return indices


@arg_digest(form=form)
def get_entity_id_from_entity(item, indices="all", skip_digestion=False):
    values = item.topology.entities["entity_id"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_entity_name_from_entity(item, indices="all", skip_digestion=False):
    values = item.topology.entities["entity_name"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_entity_type_from_entity(item, indices="all", skip_digestion=False):
    values = item.topology.entities["entity_type"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    return item.topology.n_atoms


@arg_digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):
    return item.topology.n_groups


@arg_digest(form=form)
def get_n_bonds_from_system(item, skip_digestion=False):
    return item.topology.n_bonds


@arg_digest(form=form)
def get_n_molecules_from_system(item, skip_digestion=False):
    return item.topology.n_molecules


@arg_digest(form=form)
def get_n_chains_from_system(item, skip_digestion=False):
    return item.topology.n_chains


@arg_digest(form=form)
def get_n_entities_from_system(item, skip_digestion=False):
    return item.topology.n_entities


@arg_digest(form=form)
def get_bonded_atom_pairs_from_system(item, skip_digestion=False):
    if item.topology.n_bonds == 0:
        return []
    return item.topology.bonds[["atom1_index", "atom2_index"]].to_numpy(dtype=int).tolist()


@arg_digest(form=form)
def get_n_atoms_from_group(item, indices="all", skip_digestion=False):
    import pandas as pd
    group_index_from_atom = item.topology.atoms["group_index"].to_numpy(dtype=object)
    valid_mask = pd.notna(group_index_from_atom)
    valid_indices = group_index_from_atom[valid_mask]
    if indices == "all":
        indices = list(range(item.topology.n_groups))
    output = []
    for group_index in indices:
        output.append(int(np.sum(valid_indices == group_index)))
    return output


@arg_digest(form=form)
def get_n_groups_from_chain(item, indices="all", skip_digestion=False):
    group_chain_index = get_chain_index_from_group(item, indices="all", skip_digestion=True)
    if indices == "all":
        indices = list(range(item.topology.n_chains))
    output = []
    for chain_index in indices:
        output.append(sum(ii == chain_index for ii in group_chain_index))
    return output


@arg_digest(form=form)
def get_n_groups_from_molecule(item, indices="all", skip_digestion=False):
    group_molecule_index = get_molecule_index_from_group(item, indices="all", skip_digestion=True)
    if indices == "all":
        indices = list(range(item.topology.n_molecules))
    output = []
    for molecule_index in indices:
        output.append(sum(ii == molecule_index for ii in group_molecule_index))
    return output


@arg_digest(form=form)
def get_n_molecules_from_entity(item, indices="all", skip_digestion=False):
    molecule_entity_index = get_entity_index_from_molecule(item, indices="all", skip_digestion=True)
    if indices == "all":
        indices = list(range(item.topology.n_entities))
    output = []
    for entity_index in indices:
        output.append(sum(ii == entity_index for ii in molecule_entity_index))
    return output


@arg_digest(form=form)
def get_n_atoms_from_chain(item, indices="all", skip_digestion=False):
    atom_chain_index = get_chain_index_from_atom(item, indices="all", skip_digestion=True)
    if indices == "all":
        indices = list(range(item.topology.n_chains))
    output = []
    for chain_index in indices:
        output.append(sum(ii == chain_index for ii in atom_chain_index))
    return output


@arg_digest(form=form)
def get_n_atoms_from_molecule(item, indices="all", skip_digestion=False):
    group_molecule_index = get_molecule_index_from_group(item, indices="all", skip_digestion=True)
    atom_group_index = get_group_index_from_atom(item, indices="all", skip_digestion=True)
    if indices == "all":
        indices = list(range(item.topology.n_molecules))
    output = []
    for molecule_index in indices:
        output.append(sum(group_molecule_index[group_index] == molecule_index for group_index in atom_group_index if group_index is not None))
    return output


@arg_digest(form=form)
def get_n_atoms_from_entity(item, indices="all", skip_digestion=False):
    molecule_entity_index = get_entity_index_from_molecule(item, indices="all", skip_digestion=True)
    group_molecule_index = get_molecule_index_from_group(item, indices="all", skip_digestion=True)
    atom_group_index = get_group_index_from_atom(item, indices="all", skip_digestion=True)
    if indices == "all":
        indices = list(range(item.topology.n_entities))
    output = []
    for entity_index in indices:
        count = 0
        for group_index in atom_group_index:
            if group_index is None:
                continue
            molecule_index = group_molecule_index[group_index]
            if molecule_index is not None and molecule_entity_index[molecule_index] == entity_index:
                count += 1
        output.append(count)
    return output


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith("get_")]
