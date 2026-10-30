import importlib
import types

import numpy as np

from molsysmt._private.argdigest import arg_digest

from ._delegated_getter import make_delegated_getter

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
    """
    Getting atom index from atom in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        return list(range(item.topology.n_atoms))
    return indices


@arg_digest(form=form)
def get_atom_id_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting atom id from atom in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    values = item.topology.atoms["atom_id"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_atom_name_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting atom name from atom in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    values = item.topology.atoms["atom_name"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_atom_type_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting atom type from atom in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    values = item.topology.atoms["atom_type"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_group_index_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting group index from atom in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    values = item.topology.atoms["group_index"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_group_index_from_group(item, indices="all", skip_digestion=False):
    """
    Getting group index from group in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        return list(range(item.topology.n_groups))
    return indices


@arg_digest(form=form)
def get_group_id_from_group(item, indices="all", skip_digestion=False):
    """
    Getting group id from group in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    values = item.topology.groups["group_id"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_group_name_from_group(item, indices="all", skip_digestion=False):
    """
    Getting group name from group in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    values = item.topology.groups["group_name"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_group_type_from_group(item, indices="all", skip_digestion=False):
    """
    Getting group type from group in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    values = item.topology.groups["group_type"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_chain_index_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting chain index from atom in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    values = item.topology.atoms["chain_index"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_chain_index_from_group(item, indices="all", skip_digestion=False):
    # chain_index is atom-level only; derive per-group from atoms
    """
    Getting chain index from group in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if "chain_index" not in item.topology.atoms.columns:
        values = [None] * item.topology.n_groups
    else:
        _adf = item.topology.atoms[["group_index", "chain_index"]].dropna()
        _gc = _adf.groupby("group_index", sort=False)["chain_index"].first()
        values = np.full(item.topology.n_groups, None, dtype=object)
        values[_gc.index.to_numpy(dtype=np.int64)] = _gc.to_numpy()
    return _normalize_sequence(_take(np.asarray(values, dtype=object), indices))


@arg_digest(form=form)
def get_chain_index_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting chain index from chain in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        return list(range(item.topology.n_chains))
    return indices


@arg_digest(form=form)
def get_chain_id_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting chain id from chain in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    values = item.topology.chains["chain_id"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_chain_name_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting chain name from chain in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    values = item.topology.chains["chain_name"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_chain_type_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting chain type from chain in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    values = item.topology.chains["chain_type"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_molecule_index_from_group(item, indices="all", skip_digestion=False):
    """
    Getting molecule index from group in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    values = item.topology.groups["molecule_index"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_molecule_index_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting molecule index from atom in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_indices = get_group_index_from_atom(
        item, indices=indices, skip_digestion=True
    )
    molecule_values = item.topology.groups["molecule_index"].to_numpy(dtype=object)
    return _normalize_sequence(_project(group_indices, molecule_values))


@arg_digest(form=form)
def get_molecule_index_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting molecule index from molecule in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        return list(range(item.topology.n_molecules))
    return indices


@arg_digest(form=form)
def get_molecule_id_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting molecule id from molecule in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    values = item.topology.molecules["molecule_id"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_molecule_name_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting molecule name from molecule in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    values = item.topology.molecules["molecule_name"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_molecule_type_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting molecule type from molecule in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    values = item.topology.molecules["molecule_type"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_entity_index_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting entity index from molecule in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    values = item.topology.molecules["entity_index"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_entity_index_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting entity index from atom in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    molecule_indices = get_molecule_index_from_atom(
        item, indices=indices, skip_digestion=True
    )
    entity_values = item.topology.molecules["entity_index"].to_numpy(dtype=object)
    return _normalize_sequence(_project(molecule_indices, entity_values))


@arg_digest(form=form)
def get_entity_index_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting entity index from entity in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        return list(range(item.topology.n_entities))
    return indices


@arg_digest(form=form)
def get_entity_id_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting entity id from entity in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    values = item.topology.entities["entity_id"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_entity_name_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting entity name from entity in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    values = item.topology.entities["entity_name"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_entity_type_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting entity type from entity in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    values = item.topology.entities["entity_type"].to_numpy(dtype=object)
    return _normalize_sequence(_take(values, indices))


@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    """
    Getting n atoms from system in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return item.topology.n_atoms


@arg_digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):
    """
    Getting n groups from system in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return item.topology.n_groups


@arg_digest(form=form)
def get_n_bonds_from_system(item, skip_digestion=False):
    """
    Getting n bonds from system in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_n_bonds_from_system(
        item._query_view(), skip_digestion=True
    )


@arg_digest(form=form)
def get_n_molecules_from_system(item, skip_digestion=False):
    """
    Getting n molecules from system in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return item.topology.n_molecules


@arg_digest(form=form)
def get_n_chains_from_system(item, skip_digestion=False):
    """
    Getting n chains from system in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return item.topology.n_chains


@arg_digest(form=form)
def get_n_entities_from_system(item, skip_digestion=False):
    """
    Getting n entities from system in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return item.topology.n_entities


@arg_digest(form=form)
def get_bonded_atom_pairs_from_system(item, skip_digestion=False):
    """
    Getting bonded atom pairs from system in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_bonded_atom_pairs_from_system(
        item._query_view(), skip_digestion=True
    )


@arg_digest(form=form)
def get_n_atoms_from_group(item, indices="all", skip_digestion=False):
    """
    Getting n atoms from group in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
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
    """
    Getting n groups from chain in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_chain_index = get_chain_index_from_group(
        item, indices="all", skip_digestion=True
    )
    if indices == "all":
        indices = list(range(item.topology.n_chains))
    output = []
    for chain_index in indices:
        output.append(sum(ii == chain_index for ii in group_chain_index))
    return output


@arg_digest(form=form)
def get_n_groups_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting n groups from molecule in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_molecule_index = get_molecule_index_from_group(
        item, indices="all", skip_digestion=True
    )
    if indices == "all":
        indices = list(range(item.topology.n_molecules))
    output = []
    for molecule_index in indices:
        output.append(sum(ii == molecule_index for ii in group_molecule_index))
    return output


@arg_digest(form=form)
def get_n_molecules_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting n molecules from entity in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    molecule_entity_index = get_entity_index_from_molecule(
        item, indices="all", skip_digestion=True
    )
    if indices == "all":
        indices = list(range(item.topology.n_entities))
    output = []
    for entity_index in indices:
        output.append(sum(ii == entity_index for ii in molecule_entity_index))
    return output


@arg_digest(form=form)
def get_n_atoms_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting n atoms from chain in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    atom_chain_index = get_chain_index_from_atom(
        item, indices="all", skip_digestion=True
    )
    if indices == "all":
        indices = list(range(item.topology.n_chains))
    output = []
    for chain_index in indices:
        output.append(sum(ii == chain_index for ii in atom_chain_index))
    return output


@arg_digest(form=form)
def get_n_atoms_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting n atoms from molecule in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_molecule_index = get_molecule_index_from_group(
        item, indices="all", skip_digestion=True
    )
    atom_group_index = get_group_index_from_atom(
        item, indices="all", skip_digestion=True
    )
    if indices == "all":
        indices = list(range(item.topology.n_molecules))
    output = []
    for molecule_index in indices:
        output.append(
            sum(
                group_molecule_index[group_index] == molecule_index
                for group_index in atom_group_index
                if group_index is not None
            )
        )
    return output


@arg_digest(form=form)
def get_n_atoms_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting n atoms from entity in form molsysmt.MolSysBuilder.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    molecule_entity_index = get_entity_index_from_molecule(
        item, indices="all", skip_digestion=True
    )
    group_molecule_index = get_molecule_index_from_group(
        item, indices="all", skip_digestion=True
    )
    atom_group_index = get_group_index_from_atom(
        item, indices="all", skip_digestion=True
    )
    if indices == "all":
        indices = list(range(item.topology.n_entities))
    output = []
    for entity_index in indices:
        count = 0
        for group_index in atom_group_index:
            if group_index is None:
                continue
            molecule_index = group_molecule_index[group_index]
            if (
                molecule_index is not None
                and molecule_entity_index[molecule_index] == entity_index
            ):
                count += 1
        output.append(count)
    return output


_target_module = importlib.import_module(
    "molsysmt.form.molsysmt_Topology.get_topological_attributes"
)
for _name in _target_module.__all__:
    if _name not in globals():
        globals()[_name] = make_delegated_getter(
            _name,
            getattr(_target_module, _name),
            "topology",
        )

__all__ = [
    name
    for name, obj in globals().items()
    if isinstance(obj, types.FunctionType) and name.startswith("get_")
]

del _name, _target_module


@arg_digest(form=form)
def get_formal_charge_from_atom(item, indices="all", skip_digestion=False):
    """Reading stored integer formal charges in elementary-charge units.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's atom axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None, or None
        Formal charge per atom, in integer multiples of the elementary charge;
        not a partial charge or a summed system charge.
        An absent atom-property column returns None; a materialized column retains
        one nullable value per selected atom, including an empty list for no atoms.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_formal_charge_from_atom(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_atom_is_aromatic_from_atom(item, indices="all", skip_digestion=False):
    """Reading stored atom aromaticity assignments.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's atom axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of bool or None, or None
        Declared aromaticity per atom; no ring perception or aromaticity model
        is executed.
        An absent atom-property column returns None; a materialized column retains
        one nullable value per selected atom, including an empty list for no atoms.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_atom_is_aromatic_from_atom(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_n_unpaired_electrons_from_atom(item, indices="all", skip_digestion=False):
    """Reading stored unpaired-electron counts.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's atom axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None, or None
        Assigned unpaired-electron count per atom; unknown radical state remains
        missing.
        An absent atom-property column returns None; a materialized column retains
        one nullable value per selected atom, including an empty list for no atoms.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_n_unpaired_electrons_from_atom(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_n_implicit_hydrogens_from_atom(item, indices="all", skip_digestion=False):
    """Reading stored implicit-hydrogen counts.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's atom axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None, or None
        Assigned implicit-hydrogen count per atom; no valence completion is performed.
        An absent atom-property column returns None; a materialized column retains
        one nullable value per selected atom, including an empty list for no atoms.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_n_implicit_hydrogens_from_atom(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_n_explicit_hydrogens_from_atom(item, indices="all", skip_digestion=False):
    """Reading stored explicit-hydrogen counts.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's atom axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None, or None
        Assigned explicit-hydrogen count per atom; bonds and atom inventory are
        not recounted.
        An absent atom-property column returns None; a materialized column retains
        one nullable value per selected atom, including an empty list for no atoms.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_n_explicit_hydrogens_from_atom(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_allows_implicit_hydrogens_from_atom(item, indices="all", skip_digestion=False):
    """Reading stored permission for implicit hydrogens.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's atom axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of bool or None, or None
        Declared permission per atom; false is an available assignment, not a
        missing value.
        An absent atom-property column returns None; a materialized column retains
        one nullable value per selected atom, including an empty list for no atoms.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_allows_implicit_hydrogens_from_atom(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_atom_stereochemistry_from_atom(item, indices="all", skip_digestion=False):
    """Reading stored atom stereochemistry labels.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's atom axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of str or None, or None
        Assigned stereochemistry per atom; labels are not derived from
        coordinates or connectivity.
        An absent atom-property column returns None; a materialized column retains
        one nullable value per selected atom, including an empty list for no atoms.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_atom_stereochemistry_from_atom(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_formal_charge_from_system(item, skip_digestion=False):
    """Reading stored integer formal charges in elementary-charge units.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference chemical state.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None, or None
        Formal charge per atom, in integer multiples of the elementary charge;
        not a partial charge or a summed system charge.
        An absent atom-property column returns None; a materialized column retains
        one nullable value per selected atom, including an empty list for no atoms.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_formal_charge_from_system(
        item._query_view(), skip_digestion=True
    )


@arg_digest(form=form)
def get_bond_id_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored bond labels without interpreting them as positions.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's bond axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of str or None
        String labels in bond-row order; labels need not be unique and are not
        bond indices. Missing fields return one None per selected edge, or []
        for no edges.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_bond_id_from_bond(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bond_order_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored integer bond orders.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's bond axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None
        Declared integer order per edge; unknown order is not replaced with a
        single bond. Missing fields return one None per selected edge, or [] for
        no edges.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_bond_order_from_bond(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_fractional_bond_order_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored fractional bond orders.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's bond axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of float or None
        Declared dimensionless fractional order per edge; no electronic
        calculation is performed. Missing fields return one None per selected
        edge, or [] for no edges.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_fractional_bond_order_from_bond(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bond_type_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored chemical bond types.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's bond axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of str or None
        Declared covalent, dative or unknown type per edge; geometric proximity
        is not interpreted. Missing fields return one None per selected edge, or
        [] for no edges.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_bond_type_from_bond(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bond_is_aromatic_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored bond aromaticity assignments.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's bond axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of bool or None
        Declared aromaticity per edge; false remains distinct from an unknown
        assignment. Missing fields return one None per selected edge, or [] for
        no edges.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_bond_is_aromatic_from_bond(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bond_is_conjugated_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored bond conjugation assignments.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's bond axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of bool or None
        Declared conjugation per edge; no aromaticity or conjugation perception
        is performed. Missing fields return one None per selected edge, or []
        for no edges.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_bond_is_conjugated_from_bond(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bond_stereochemistry_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored bond stereochemistry labels.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's bond axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of str or None
        Assigned stereochemistry per edge; no coordinate-based stereochemistry
        is inferred. Missing fields return one None per selected edge, or [] for
        no edges.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_bond_stereochemistry_from_bond(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bond_stereo_atom_indices_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored atom references for bond stereochemistry.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's bond axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of list of int or None
        Two independently nullable atom indices per edge, in stored reference
        order; these are not atom IDs. Missing references retain two nullable
        positions per edge; no edges returns [].

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_bond_stereo_atom_indices_from_bond(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bond_donor_atom_index_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored donor atom indices of directed bonds.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's bond axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None
        Declared donor atom position per edge; undirected or unassigned edges
        remain missing. Missing fields return one None per selected edge, or []
        for no edges.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_bond_donor_atom_index_from_bond(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bond_acceptor_atom_index_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored acceptor atom indices of directed bonds.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's bond axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None
        Declared acceptor atom position per edge; no direction is inferred from
        endpoint order. Missing fields return one None per selected edge, or []
        for no edges.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_bond_acceptor_atom_index_from_bond(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bond_joins_components_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored bond participation in component connectivity.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's bond axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of bool or None
        Declared participation flag per edge; no components are rebuilt or flags
        synthesized during reading. Missing fields return one None per selected
        edge, or [] for no edges.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_bond_joins_components_from_bond(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bond_evidence_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored evidence labels for chemical bonds.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's bond axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of str or None
        Original evidence declaration per edge; reading a value does not certify
        its scientific provenance. Missing fields return one None per selected
        edge, or [] for no edges.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_bond_evidence_from_bond(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_component_id_from_component(item, indices="all", skip_digestion=False):
    """Reading stored state-local component labels.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's component axis, retaining order and
        repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of str or None
        String component labels; they are not component indices and are not
        regenerated. Missing labels retain None.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_component_id_from_component(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_component_id_from_atom(item, indices="all", skip_digestion=False):
    """Reading stored state-local component labels.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's atom axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of str or None
        String component labels; they are not component indices and are not
        regenerated. Each atom receives its component label; unknown membership
        returns None.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_component_id_from_atom(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_component_name_from_component(item, indices="all", skip_digestion=False):
    """Reading stored state-local component names.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's component axis, retaining order and
        repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of str or None
        Assigned component names; no molecular identity or chemical name is
        inferred. Missing labels retain None.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_component_name_from_component(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_component_name_from_atom(item, indices="all", skip_digestion=False):
    """Reading stored state-local component names.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's atom axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of str or None
        Assigned component names; no molecular identity or chemical name is
        inferred. Each atom receives its component label; unknown membership
        returns None.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_component_name_from_atom(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_component_type_from_component(item, indices="all", skip_digestion=False):
    """Reading stored state-local component types.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's component axis, retaining order and
        repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of str or None
        Assigned component types; no chemical classification or component
        rebuilding is performed. Missing labels retain None.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_component_type_from_component(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_component_type_from_atom(item, indices="all", skip_digestion=False):
    """Reading stored state-local component types.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference chemical state.
    indices : 'all' or array-like of int, default='all'
        Positions on the selected state's atom axis, retaining order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of str or None
        Assigned component types; no chemical classification or component
        rebuilding is performed. Each atom receives its component label; unknown
        membership returns None.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_component_type_from_atom(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form="molsysmt.MolSysBuilder")
def get_n_chemical_states_from_system(item, skip_digestion=False):
    """Getting the number of chemical states."""
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_n_chemical_states_from_system(
        item._query_view(), skip_digestion=True
    )


@arg_digest(form="molsysmt.MolSysBuilder")
def get_reference_chemical_state_index_from_system(item, skip_digestion=False):
    """Getting the reference chemical-state index."""
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_reference_chemical_state_index_from_system(
        item._query_view(), skip_digestion=True
    )


@arg_digest(form=form)
def get_n_components_from_system(item, skip_digestion=False):
    """Counting component rows in the selected chemical state.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection supplying state-local component inventory.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    int
        Stored component count, including declared components without atoms.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_n_components_from_system(
        item._query_view(), skip_digestion=True
    )


@arg_digest(form=form)
def get_chemical_state_index_from_system(item, skip_digestion=False):
    """Listing every chemical-state position without changing the reference.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Ordered collection whose complete inventory is requested.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int
        All state indices, even when another attribute selects one state.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_chemical_state_index_from_system(
        item._query_view(), skip_digestion=True
    )


@arg_digest(form=form)
def get_chemical_state_id_from_system(item, skip_digestion=False):
    """Listing stored string labels for the complete chemical-state inventory.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Ordered collection whose labels are requested.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of str or None
        One label per state, retaining missing labels and collection order.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_chemical_state_id_from_system(
        item._query_view(), skip_digestion=True
    )


@arg_digest(form=form)
def get_connectivity_completeness_from_system(item, skip_digestion=False):
    """Reading the selected state's connectivity declaration without inference.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with a resolvable chemical state.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    str
        'unavailable', 'partial' or 'complete' for that state, not all states.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_connectivity_completeness_from_system(
        item._query_view(), skip_digestion=True
    )


@arg_digest(form=form)
def get_component_completeness_from_system(item, skip_digestion=False):
    """Reading the selected state's component-completeness declaration.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with a resolvable chemical state.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    str
        'unavailable', 'partial' or 'complete', independently of connectivity.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_component_completeness_from_system(
        item._query_view(), skip_digestion=True
    )


@arg_digest(form=form)
def get_component_evidence_from_system(item, skip_digestion=False):
    """Reading the selected state's recorded component evidence.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection retaining the original component assignment evidence.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    str
        Stored evidence label, without classifying or rebuilding components.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_component_evidence_from_system(
        item._query_view(), skip_digestion=True
    )


@arg_digest(form=form)
def get_n_atoms_from_atom(item, indices="all", skip_digestion=False):
    """Counting positions in an atom selection without requiring a state.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection declaring the shared atom-domain size.
    indices : str or list of int, default='all'
        Atom positions; repetitions contribute to the selected length.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    int or None
        Selection length, or the complete atom-domain size for 'all'.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_n_atoms_from_atom(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bond_index_from_bond(item, indices="all", skip_digestion=False):
    """Returning validated positions in the selected state's bond table.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection supplying the active chemical-state axis.
    indices : str or list of int, default='all'
        Bond positions in that state, not bond IDs or another state's positions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None
        Ordered selected positions, including repetitions or an empty list.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_bond_index_from_bond(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bond_index_from_system(item, skip_digestion=False):
    """Listing all stored bond positions in the selected chemical state.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection with an unambiguous active or reference state.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int
        Contiguous state-local positions; an edge-free table returns [].

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_bond_index_from_system(
        item._query_view(), skip_digestion=True
    )


@arg_digest(form=form)
def get_component_index_from_component(item, indices="all", skip_digestion=False):
    """Returning validated positions in the selected component inventory.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection supplying the active state's component rows.
    indices : str or list of int, default='all'
        Component positions, preserving order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None
        State-local positions, independent of Topology's stable molecules.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_component_index_from_component(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_component_index_from_atom(item, indices="all", skip_digestion=False):
    """Projecting stored component membership onto selected atom positions.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection supplying the selected state's atom-aligned declarations.
    indices : str or list of int, default='all'
        Atom positions, preserving order and repetitions.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None
        One component index or missing value per atom; no graph inference runs.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_component_index_from_atom(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_n_components_from_atom(item, indices="all", skip_digestion=False):
    """Counting distinct declared components represented by selected atoms.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection supplying state-local membership and component inventory.
    indices : str or list of int, default='all'
        Atom positions. 'all' counts the full declared component inventory.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    int or None
        Distinct known memberships for an explicit selection; missing links do
        not create components. A count does not certify completeness.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_n_components_from_atom(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_n_components_from_component(item, indices="all", skip_digestion=False):
    """Counting selected component positions without rebuilding their graph.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection supplying the active component inventory.
    indices : str or list of int, default='all'
        Component positions; repeated positions retain their multiplicity.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    int or None
        Selected length, including zero for an empty selection.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_n_components_from_component(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_n_bonds_from_atom(item, indices="all", skip_digestion=False):
    """Counting stored incident edges separately for each selected atom.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection supplying the active state's stored edges.
    indices : str or list of int, default='all'
        Atom positions, including repetitions and atoms without bonds.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None
        One incident-edge count per atom, including edges to unselected atoms.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_n_bonds_from_atom(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bond_index_from_atom(item, indices="all", skip_digestion=False):
    """Listing stored incident bond positions for each selected atom.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection supplying the active state's stored edges.
    indices : str or list of int, default='all'
        Atom positions; external endpoints are retained in incident lists.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of list of int or None
        One ordered state-local bond list per atom; isolated atoms give [].

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_bond_index_from_atom(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_n_atoms_from_component(item, indices="all", skip_digestion=False):
    """Counting atoms with declared membership in each selected component.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection supplying atom-aligned membership in the active state.
    indices : str or list of int, default='all'
        Component positions, including empty declared components.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None
        Atom count per component; atoms with unknown membership are excluded.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_n_atoms_from_component(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_atom_index_from_component(item, indices="all", skip_digestion=False):
    """Listing declared atom members of each selected component.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection supplying atom-aligned membership in the active state.
    indices : str or list of int, default='all'
        Component positions, preserving repeated and empty components.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of list of int or None
        Ascending source atom positions per component, without topology context.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_atom_index_from_component(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_n_bonds_from_component(item, indices="all", skip_digestion=False):
    """Counting distinct stored edges incident on each selected component.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Collection supplying stored edges and declared component memberships.
    indices : str or list of int, default='all'
        Component positions. An internal edge contributes once, not twice.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list of int or None
        Incident counts, including cross-component edges at both known ends.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_n_bonds_from_component(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bonded_atom_pairs_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored bond participants from the selected chemical state.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Declared chemical-state provider; no stable hierarchy is required.
    indices : str or list of int, default='all'
        Ordered source positions. Atom selections restrict incident edges or,
        for inner relationships, edges with both endpoints selected.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list
        Source atom-index pairs, or sorted unique atoms for bonded_atoms.
        Empty stored connectivity returns an empty list without inference.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_bonded_atom_pairs_from_bond(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bonded_atoms_from_bond(item, indices="all", skip_digestion=False):
    """Reading stored bond participants from the selected chemical state.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Declared chemical-state provider; no stable hierarchy is required.
    indices : str or list of int, default='all'
        Ordered source positions. Atom selections restrict incident edges or,
        for inner relationships, edges with both endpoints selected.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list
        Source atom-index pairs, or sorted unique atoms for bonded_atoms.
        Empty stored connectivity returns an empty list without inference.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_bonded_atoms_from_bond(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bonded_atom_pairs_from_atom(item, indices="all", skip_digestion=False):
    """Reading stored bond participants from the selected chemical state.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Declared chemical-state provider; no stable hierarchy is required.
    indices : str or list of int, default='all'
        Ordered source positions. Atom selections restrict incident edges or,
        for inner relationships, edges with both endpoints selected.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list
        Source atom-index pairs, or sorted unique atoms for bonded_atoms.
        Empty stored connectivity returns an empty list without inference.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_bonded_atom_pairs_from_atom(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_atom(item, indices="all", skip_digestion=False):
    """Reading stored bond participants from the selected chemical state.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Declared chemical-state provider; no stable hierarchy is required.
    indices : str or list of int, default='all'
        Ordered source positions. Atom selections restrict incident edges or,
        for inner relationships, edges with both endpoints selected.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list
        Source atom-index pairs, or sorted unique atoms for bonded_atoms.
        Empty stored connectivity returns an empty list without inference.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_inner_bonded_atom_pairs_from_atom(
        item._query_view(), indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_system(item, skip_digestion=False):
    """Reading stored bond participants from the selected chemical state.

    Parameters
    ----------
    item : molsysmt.MolSysBuilder
        Declared chemical-state provider; no stable hierarchy is required.
    skip_digestion : bool, default=False
        Skip digestion only for already validated arguments.

    Returns
    -------
    list
        Source atom-index pairs, or sorted unique atoms for bonded_atoms.
        Empty stored connectivity returns an empty list without inference.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_MolSys

    return molsysmt_MolSys.get_inner_bonded_atom_pairs_from_system(
        item._query_view(), skip_digestion=True
    )


_mixed_module = importlib.import_module(
    "molsysmt.form.molsysmt_MolSys.get_topological_attributes"
)
for _name, _target in vars(_mixed_module).items():
    if _name.startswith(
        ("get_inner_bond_index_", "get_inner_bonded_atoms_", "get_n_inner_bonds_")
    ) and callable(_target):
        globals()[_name] = make_delegated_getter(_name, _target, "_query_view")


__all__ = [name for name in globals() if name.startswith("get_")]
