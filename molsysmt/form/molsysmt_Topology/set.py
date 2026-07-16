from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
import pandas as pd

form='molsysmt.Topology'

_PUBLIC_TO_NATIVE_ATOM_STATE = {
    'formal_charge': 'formal_charge',
    'atom_is_aromatic': 'is_aromatic',
    'n_unpaired_electrons': 'n_unpaired_electrons',
    'n_implicit_hydrogens': 'n_implicit_hydrogens',
    'allows_implicit_hydrogens': 'allows_implicit_hydrogens',
    'atom_stereochemistry': 'stereochemistry',
}

_PUBLIC_TO_NATIVE_BOND_STATE = {
    'bond_id': 'bond_id',
    'bond_order': 'bond_order',
    'fractional_bond_order': 'fractional_bond_order',
    'bond_type': 'bond_type',
    'bond_is_aromatic': 'is_aromatic',
    'bond_is_conjugated': 'is_conjugated',
    'bond_stereochemistry': 'stereochemistry',
    'bond_donor_atom_index': 'donor_atom_index',
    'bond_acceptor_atom_index': 'acceptor_atom_index',
    'bond_joins_components': 'joins_components',
    'bond_evidence': 'evidence',
}


def _set_atom_state_attribute(item, attribute, indices, value):
    if attribute == 'formal_charge' and puw.is_quantity(value):
        value = puw.get_value(value, to_unit='elementary_charge')
    atom_indices = None if is_all(indices) else indices
    item._set_chemical_state_atom_attribute(
        _PUBLIC_TO_NATIVE_ATOM_STATE[attribute], value, atom_indices=atom_indices
    )


@arg_digest(form=form)
def set_formal_charge_to_atom(item, indices='all', value=None, skip_digestion=False):
    """Setting formal charges on the resolved chemical state."""

    _set_atom_state_attribute(item, 'formal_charge', indices, value)


@arg_digest(form=form)
def set_atom_is_aromatic_to_atom(item, indices='all', value=None, skip_digestion=False):
    """Setting atom aromaticity on the resolved chemical state."""

    _set_atom_state_attribute(item, 'atom_is_aromatic', indices, value)


@arg_digest(form=form)
def set_n_unpaired_electrons_to_atom(item, indices='all', value=None, skip_digestion=False):
    """Setting unpaired-electron counts on the resolved chemical state."""

    _set_atom_state_attribute(item, 'n_unpaired_electrons', indices, value)


@arg_digest(form=form)
def set_n_implicit_hydrogens_to_atom(item, indices='all', value=None, skip_digestion=False):
    """Setting implicit-hydrogen counts on the resolved chemical state."""

    _set_atom_state_attribute(item, 'n_implicit_hydrogens', indices, value)


@arg_digest(form=form)
def set_allows_implicit_hydrogens_to_atom(item, indices='all', value=None, skip_digestion=False):
    """Setting implicit-hydrogen permission flags on the resolved chemical state."""

    _set_atom_state_attribute(item, 'allows_implicit_hydrogens', indices, value)


@arg_digest(form=form)
def set_atom_stereochemistry_to_atom(item, indices='all', value=None, skip_digestion=False):
    """Setting atom stereochemistry on the resolved chemical state."""

    _set_atom_state_attribute(item, 'atom_stereochemistry', indices, value)


def _set_bond_state_attribute(item, attribute, indices, value):
    """Set one public bond-state attribute through canonical native storage."""

    item._set_chemical_state_bond_attribute(
        _PUBLIC_TO_NATIVE_BOND_STATE[attribute], value, bond_indices=indices
    )


@arg_digest(form=form)
def set_bond_id_to_bond(item, indices='all', value=None, skip_digestion=False):
    _set_bond_state_attribute(item, 'bond_id', indices, value)


@arg_digest(form=form)
def set_bond_order_to_bond(item, indices='all', value=None, skip_digestion=False):
    _set_bond_state_attribute(item, 'bond_order', indices, value)


@arg_digest(form=form)
def set_fractional_bond_order_to_bond(item, indices='all', value=None, skip_digestion=False):
    _set_bond_state_attribute(item, 'fractional_bond_order', indices, value)


@arg_digest(form=form)
def set_bond_type_to_bond(item, indices='all', value=None, skip_digestion=False):
    _set_bond_state_attribute(item, 'bond_type', indices, value)


@arg_digest(form=form)
def set_bond_is_aromatic_to_bond(item, indices='all', value=None, skip_digestion=False):
    _set_bond_state_attribute(item, 'bond_is_aromatic', indices, value)


@arg_digest(form=form)
def set_bond_is_conjugated_to_bond(item, indices='all', value=None, skip_digestion=False):
    _set_bond_state_attribute(item, 'bond_is_conjugated', indices, value)


@arg_digest(form=form)
def set_bond_stereochemistry_to_bond(item, indices='all', value=None, skip_digestion=False):
    _set_bond_state_attribute(item, 'bond_stereochemistry', indices, value)


@arg_digest(form=form)
def set_bond_stereo_atom_indices_to_bond(item, indices='all', value=None, skip_digestion=False):
    item._set_chemical_state_bond_stereo_atom_indices(value, bond_indices=indices)


@arg_digest(form=form)
def set_bond_donor_atom_index_to_bond(item, indices='all', value=None, skip_digestion=False):
    _set_bond_state_attribute(item, 'bond_donor_atom_index', indices, value)


@arg_digest(form=form)
def set_bond_acceptor_atom_index_to_bond(item, indices='all', value=None, skip_digestion=False):
    _set_bond_state_attribute(item, 'bond_acceptor_atom_index', indices, value)


@arg_digest(form=form)
def set_bond_joins_components_to_bond(item, indices='all', value=None, skip_digestion=False):
    _set_bond_state_attribute(item, 'bond_joins_components', indices, value)


@arg_digest(form=form)
def set_bond_evidence_to_bond(item, indices='all', value=None, skip_digestion=False):
    _set_bond_state_attribute(item, 'bond_evidence', indices, value)


###### Set

## Atom

@arg_digest(form=form)
def set_atom_id_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.atoms.atom_id=value
    else:
        item.atoms.loc[indices, 'atom_id']=value

    pass

@arg_digest(form=form)
def set_atom_name_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.atoms.atom_name=value
    else:
        item.atoms.loc[indices, 'atom_name']=value

    pass

@arg_digest(form=form)
def set_atom_type_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.atoms.atom_type=value
    else:
        item.atoms.loc[indices, 'atom_type']=value

    pass


@arg_digest(form=form)
def set_isotope_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        if value is None or value is pd.NA or np.isscalar(value):
            value = [value] * item.n_atoms
        item.atoms['isotope'] = pd.array(value, dtype='UInt16')
    else:
        isotope = item.atoms['isotope'].copy()
        isotope.iloc[indices] = value
        item.atoms['isotope'] = pd.array(isotope, dtype='UInt16')

@arg_digest(form=form)
def set_group_index_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.atoms.group_index=value
    else:
        item.atoms.loc[indices, 'group_index']=value

    pass

@arg_digest(form=form)
def set_component_index_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        if len(value)==1:
            item._set_component_indices([value[0]] * item.n_atoms)
            n_components = 1
        else:
            item._set_component_indices(value)
            n_components = np.unique(value).shape[0]
        if n_components!=item.components.shape[0]:
            item.reset_components(n_components=n_components)
            item.rebuild_components(redefine_indices=True, redefine_ids=True,
                                    redefine_types=True, redefine_names=True)
    else:
        item._set_component_indices(value, atom_indices=indices)

    pass

@arg_digest(form=form)
def set_chain_index_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        if len(value)==1:
            item.atoms.chain_index=value[0]
            n_chains = 1
        else:
            item.atoms.chain_index=value
            n_chains = np.unique(value).shape[0]
        if n_chains!=item.chains.shape[0]:
            item.reset_chains(n_chains=n_chains)
            item.rebuild_chains(redefine_indices=True, redefine_ids=True,
                                redefine_types=True, redefine_names=True)
    else:
        item.atoms.loc[indices, 'chain_index']=value

    pass

#@arg_digest(form=form)
#def set_chain_id_to_atom(item, indices='all', value=None, skip_digestion=False):
#
#    if is_all(indices):
#        item.atoms.chain_index=0
#        item.reset_chains(n_chains=1)
#        item.chains.chain_id=value
#        item.chains.chain_name='A'
#        item.rebuild_chains(redefine_ids=False, redefine_types=True)
#    else:
#        raise NotImplementedError
#
#    pass


## Cross-element atom setters — group attributes


def _set_by_bridge(target_df, target_col, bridge_indices, value):
    """Set target_df[target_col] using first value per unique bridge index.

    Uses full column reassignment to avoid dtype enforcement of .at[].
    """
    n_target = len(target_df)
    new_values = [None] * n_target
    for src_i, bi in enumerate(bridge_indices):
        bi_int = int(bi)
        if new_values[bi_int] is None:
            new_values[bi_int] = value[src_i]
    # Only update positions that were touched (keep original for untouched)
    current = target_df[target_col].tolist()
    for i, v in enumerate(new_values):
        if v is not None:
            current[i] = v
    target_df[target_col] = current


@arg_digest(form=form)
def set_group_id_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = item.atoms['group_index'].to_numpy()
        _set_by_bridge(item.groups, 'group_id', bridge, value)
    else:
        for i, ai in enumerate(list(indices)):
            gi = item.atoms.at[ai, 'group_index']
            item.groups.at[int(gi), 'group_id'] = value[i]

    pass


@arg_digest(form=form)
def set_group_name_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = item.atoms['group_index'].to_numpy()
        _set_by_bridge(item.groups, 'group_name', bridge, value)
    else:
        for i, ai in enumerate(list(indices)):
            gi = item.atoms.at[ai, 'group_index']
            item.groups.at[int(gi), 'group_name'] = value[i]

    pass


@arg_digest(form=form)
def set_group_type_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = item.atoms['group_index'].to_numpy()
        _set_by_bridge(item.groups, 'group_type', bridge, value)
    else:
        for i, ai in enumerate(list(indices)):
            gi = item.atoms.at[ai, 'group_index']
            item.groups.at[int(gi), 'group_type'] = value[i]

    pass


@arg_digest(form=form)
def set_component_id_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = item._get_component_indices().to_numpy()
        _set_by_bridge(item.components, 'component_id', bridge, value)
    else:
        component_indices = item._get_component_indices()
        for i, ai in enumerate(list(indices)):
            ci = component_indices.loc[ai]
            item.components.at[int(ci), 'component_id'] = value[i]

    pass


@arg_digest(form=form)
def set_component_name_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = item._get_component_indices().to_numpy()
        _set_by_bridge(item.components, 'component_name', bridge, value)
    else:
        component_indices = item._get_component_indices()
        for i, ai in enumerate(list(indices)):
            ci = component_indices.loc[ai]
            item.components.at[int(ci), 'component_name'] = value[i]

    pass


@arg_digest(form=form)
def set_component_type_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = item._get_component_indices().to_numpy()
        _set_by_bridge(item.components, 'component_type', bridge, value)
    else:
        component_indices = item._get_component_indices()
        for i, ai in enumerate(list(indices)):
            ci = component_indices.loc[ai]
            item.components.at[int(ci), 'component_type'] = value[i]

    pass


@arg_digest(form=form)
def set_molecule_index_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = item.atoms['group_index'].to_numpy()
        _set_by_bridge(item.groups, 'molecule_index', bridge, value)
    else:
        for i, ai in enumerate(list(indices)):
            gi = item.atoms.at[ai, 'group_index']
            item.groups.at[int(gi), 'molecule_index'] = value[i]

    pass


@arg_digest(form=form)
def set_molecule_id_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        group_idx = item.atoms['group_index'].to_numpy()
        mol_idx = item.groups['molecule_index'].to_numpy()
        bridge = mol_idx[group_idx]
        _set_by_bridge(item.molecules, 'molecule_id', bridge, value)
    else:
        for i, ai in enumerate(list(indices)):
            gi = item.atoms.at[ai, 'group_index']
            mi = item.groups.at[int(gi), 'molecule_index']
            item.molecules.at[int(mi), 'molecule_id'] = value[i]

    pass


@arg_digest(form=form)
def set_molecule_name_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        group_idx = item.atoms['group_index'].to_numpy()
        mol_idx = item.groups['molecule_index'].to_numpy()
        bridge = mol_idx[group_idx]
        _set_by_bridge(item.molecules, 'molecule_name', bridge, value)
    else:
        for i, ai in enumerate(list(indices)):
            gi = item.atoms.at[ai, 'group_index']
            mi = item.groups.at[int(gi), 'molecule_index']
            item.molecules.at[int(mi), 'molecule_name'] = value[i]

    pass


@arg_digest(form=form)
def set_molecule_type_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        group_idx = item.atoms['group_index'].to_numpy()
        mol_idx = item.groups['molecule_index'].to_numpy()
        bridge = mol_idx[group_idx]
        _set_by_bridge(item.molecules, 'molecule_type', bridge, value)
    else:
        for i, ai in enumerate(list(indices)):
            gi = item.atoms.at[ai, 'group_index']
            mi = item.groups.at[int(gi), 'molecule_index']
            item.molecules.at[int(mi), 'molecule_type'] = value[i]

    pass


@arg_digest(form=form)
def set_chain_id_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = item.atoms['chain_index'].to_numpy()
        _set_by_bridge(item.chains, 'chain_id', bridge, value)
    else:
        for i, ai in enumerate(list(indices)):
            ci = item.atoms.at[ai, 'chain_index']
            item.chains.at[int(ci), 'chain_id'] = value[i]

    pass


@arg_digest(form=form)
def set_chain_name_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = item.atoms['chain_index'].to_numpy()
        _set_by_bridge(item.chains, 'chain_name', bridge, value)
    else:
        for i, ai in enumerate(list(indices)):
            ci = item.atoms.at[ai, 'chain_index']
            item.chains.at[int(ci), 'chain_name'] = value[i]

    pass


@arg_digest(form=form)
def set_chain_type_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = item.atoms['chain_index'].to_numpy()
        _set_by_bridge(item.chains, 'chain_type', bridge, value)
    else:
        for i, ai in enumerate(list(indices)):
            ci = item.atoms.at[ai, 'chain_index']
            item.chains.at[int(ci), 'chain_type'] = value[i]

    pass


@arg_digest(form=form)
def set_entity_index_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        group_idx = item.atoms['group_index'].to_numpy()
        mol_idx = item.groups['molecule_index'].to_numpy()
        bridge = mol_idx[group_idx]
        _set_by_bridge(item.molecules, 'entity_index', bridge, value)
    else:
        for i, ai in enumerate(list(indices)):
            gi = item.atoms.at[ai, 'group_index']
            mi = item.groups.at[int(gi), 'molecule_index']
            item.molecules.at[int(mi), 'entity_index'] = value[i]

    pass


@arg_digest(form=form)
def set_entity_id_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        group_idx = item.atoms['group_index'].to_numpy()
        mol_idx = item.groups['molecule_index'].to_numpy()
        ent_idx = item.molecules['entity_index'].to_numpy()
        bridge = ent_idx[mol_idx[group_idx]]
        _set_by_bridge(item.entities, 'entity_id', bridge, value)
    else:
        for i, ai in enumerate(list(indices)):
            gi = item.atoms.at[ai, 'group_index']
            mi = item.groups.at[int(gi), 'molecule_index']
            ei = item.molecules.at[int(mi), 'entity_index']
            item.entities.at[int(ei), 'entity_id'] = value[i]

    pass


@arg_digest(form=form)
def set_entity_name_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        group_idx = item.atoms['group_index'].to_numpy()
        mol_idx = item.groups['molecule_index'].to_numpy()
        ent_idx = item.molecules['entity_index'].to_numpy()
        bridge = ent_idx[mol_idx[group_idx]]
        _set_by_bridge(item.entities, 'entity_name', bridge, value)
    else:
        for i, ai in enumerate(list(indices)):
            gi = item.atoms.at[ai, 'group_index']
            mi = item.groups.at[int(gi), 'molecule_index']
            ei = item.molecules.at[int(mi), 'entity_index']
            item.entities.at[int(ei), 'entity_name'] = value[i]

    pass


@arg_digest(form=form)
def set_entity_type_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        group_idx = item.atoms['group_index'].to_numpy()
        mol_idx = item.groups['molecule_index'].to_numpy()
        ent_idx = item.molecules['entity_index'].to_numpy()
        bridge = ent_idx[mol_idx[group_idx]]
        _set_by_bridge(item.entities, 'entity_type', bridge, value)
    else:
        for i, ai in enumerate(list(indices)):
            gi = item.atoms.at[ai, 'group_index']
            mi = item.groups.at[int(gi), 'molecule_index']
            ei = item.molecules.at[int(mi), 'entity_index']
            item.entities.at[int(ei), 'entity_type'] = value[i]

    pass


## Group

@arg_digest(form=form)
def set_group_id_to_group(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.groups.group_id=value
    else:
        item.groups.iloc[indices, 0]=value

    pass

@arg_digest(form=form)
def set_group_name_to_group(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.groups.group_name=value
    else:
        item.groups.iloc[indices, 1]=value

    pass

@arg_digest(form=form)
def set_group_type_to_group(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.groups.group_type=value
    else:
        item.groups.iloc[indices, 2]=value

    pass


## Cross-element group setters — molecule / chain / entity attributes


@arg_digest(form=form)
def set_molecule_id_to_group(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = item.groups['molecule_index'].to_numpy()
        _set_by_bridge(item.molecules, 'molecule_id', bridge, value)
    else:
        for i, gi in enumerate(list(indices)):
            mi = item.groups.at[gi, 'molecule_index']
            item.molecules.at[int(mi), 'molecule_id'] = value[i]

    pass


@arg_digest(form=form)
def set_molecule_name_to_group(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = item.groups['molecule_index'].to_numpy()
        _set_by_bridge(item.molecules, 'molecule_name', bridge, value)
    else:
        for i, gi in enumerate(list(indices)):
            mi = item.groups.at[gi, 'molecule_index']
            item.molecules.at[int(mi), 'molecule_name'] = value[i]

    pass


@arg_digest(form=form)
def set_molecule_type_to_group(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = item.groups['molecule_index'].to_numpy()
        _set_by_bridge(item.molecules, 'molecule_type', bridge, value)
    else:
        for i, gi in enumerate(list(indices)):
            mi = item.groups.at[gi, 'molecule_index']
            item.molecules.at[int(mi), 'molecule_type'] = value[i]

    pass


def _chain_index_per_group(item):
    """Derive per-group chain_index from atoms (chain_index is atom-level only)."""
    import numpy as np
    _adf = item.atoms[["group_index", "chain_index"]].dropna()
    _gc = _adf.groupby("group_index", sort=False)["chain_index"].first()
    bridge = np.full(item.n_groups, -1, dtype=np.int64)
    bridge[_gc.index.to_numpy(dtype=np.int64)] = _gc.to_numpy(dtype=np.int64)
    return bridge


@arg_digest(form=form)
def set_chain_id_to_group(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = _chain_index_per_group(item)
        _set_by_bridge(item.chains, 'chain_id', bridge, value)
    else:
        for i, gi in enumerate(list(indices)):
            atom_mask = item.atoms["group_index"] == gi
            ci = int(item.atoms.loc[atom_mask, "chain_index"].iloc[0])
            item.chains.at[ci, 'chain_id'] = value[i]

    pass


@arg_digest(form=form)
def set_chain_name_to_group(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = _chain_index_per_group(item)
        _set_by_bridge(item.chains, 'chain_name', bridge, value)
    else:
        for i, gi in enumerate(list(indices)):
            atom_mask = item.atoms["group_index"] == gi
            ci = int(item.atoms.loc[atom_mask, "chain_index"].iloc[0])
            item.chains.at[ci, 'chain_name'] = value[i]

    pass


@arg_digest(form=form)
def set_chain_type_to_group(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = _chain_index_per_group(item)
        _set_by_bridge(item.chains, 'chain_type', bridge, value)
    else:
        for i, gi in enumerate(list(indices)):
            atom_mask = item.atoms["group_index"] == gi
            ci = int(item.atoms.loc[atom_mask, "chain_index"].iloc[0])
            item.chains.at[ci, 'chain_type'] = value[i]

    pass


@arg_digest(form=form)
def set_entity_id_to_group(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        mol_idx = item.groups['molecule_index'].to_numpy()
        ent_idx = item.molecules['entity_index'].to_numpy()
        bridge = ent_idx[mol_idx]
        _set_by_bridge(item.entities, 'entity_id', bridge, value)
    else:
        for i, gi in enumerate(list(indices)):
            mi = item.groups.at[gi, 'molecule_index']
            ei = item.molecules.at[int(mi), 'entity_index']
            item.entities.at[int(ei), 'entity_id'] = value[i]

    pass


@arg_digest(form=form)
def set_entity_name_to_group(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        mol_idx = item.groups['molecule_index'].to_numpy()
        ent_idx = item.molecules['entity_index'].to_numpy()
        bridge = ent_idx[mol_idx]
        _set_by_bridge(item.entities, 'entity_name', bridge, value)
    else:
        for i, gi in enumerate(list(indices)):
            mi = item.groups.at[gi, 'molecule_index']
            ei = item.molecules.at[int(mi), 'entity_index']
            item.entities.at[int(ei), 'entity_name'] = value[i]

    pass


@arg_digest(form=form)
def set_entity_type_to_group(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        mol_idx = item.groups['molecule_index'].to_numpy()
        ent_idx = item.molecules['entity_index'].to_numpy()
        bridge = ent_idx[mol_idx]
        _set_by_bridge(item.entities, 'entity_type', bridge, value)
    else:
        for i, gi in enumerate(list(indices)):
            mi = item.groups.at[gi, 'molecule_index']
            ei = item.molecules.at[int(mi), 'entity_index']
            item.entities.at[int(ei), 'entity_type'] = value[i]

    pass


## Component

@arg_digest(form=form)
def set_component_id_to_component(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.components.component_id=value
    else:
        item.components.iloc[indices, 0]=value

    pass

@arg_digest(form=form)
def set_component_name_to_component(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.components.component_name=value
    else:
        item.components.iloc[indices, 1]=value

    pass

@arg_digest(form=form)
def set_component_type_to_component(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.components.component_type=value
    else:
        item.components.iloc[indices, 2]=value

    pass


## Molecule

@arg_digest(form=form)
def set_molecule_id_to_molecule(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.molecules.molecule_id=value
    else:
        item.molecules.iloc[indices, 0]=value

    pass

@arg_digest(form=form)
def set_molecule_name_to_molecule(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.molecules.molecule_name=value
    else:
        item.molecules.iloc[indices, 1]=value

    pass

@arg_digest(form=form)
def set_molecule_type_to_molecule(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.molecules.molecule_type=value
    else:
        item.molecules.iloc[indices, 2]=value

    pass


## Chain

@arg_digest(form=form)
def set_chain_id_to_chain(item, indices='all', value=None, skip_digestion=False):

    value_is_string = False

    if isinstance(value, str):
        value_is_string = True
    elif isinstance(value, list):
        if isinstance(value[0], str):
            value_is_string = True

    if value_is_string:
        if item.chains.chain_id.dtype.kind == 'i':
            item.chains.chain_id = item.chains.chain_id.astype('string')

    if is_all(indices):
        item.chains.chain_id=value
    else:
        if len(value)==1:
            value=value[0]
        item.chains.iloc[indices, 0]=value

    pass

@arg_digest(form=form)
def set_chain_name_to_chain(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.chains.chain_name=value
    else:
        item.chains.iloc[indices, 1]=value


    pass

@arg_digest(form=form)
def set_chain_type_to_chain(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.chains.chain_type=value
    else:
        if len(value)==1:
            value=value[0]
        item.chains.iloc[indices, 2]=value

    pass


## Entity

@arg_digest(form=form)
def set_entity_id_to_entity(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.entities.entity_id=value
    else:
        item.entities.iloc[indices, 0]=value

    pass

@arg_digest(form=form)
def set_entity_name_to_entity(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.entities.entity_name=value
    else:
        item.entities.iloc[indices, 1]=value

    pass

@arg_digest(form=form)
def set_entity_type_to_entity(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.entities.entity_type=value
    else:
        item.entities.iloc[indices, 2]=value

    pass


## ---------------------------------------------------------------------------
## Bridge helper functions
## ---------------------------------------------------------------------------

def _get_chain_index_for_molecule(item):
    """Array of chain_index, one per molecule (first atom found)."""
    n_molecules = len(item.molecules)
    bridge = np.zeros(n_molecules, dtype=int)
    seen = np.zeros(n_molecules, dtype=bool)
    group_idx = item.atoms['group_index'].to_numpy()
    chain_idx = item.atoms['chain_index'].to_numpy()
    mol_idx_arr = item.groups['molecule_index'].to_numpy()
    for ai in range(len(group_idx)):
        mi = int(mol_idx_arr[int(group_idx[ai])])
        if not seen[mi]:
            bridge[mi] = int(chain_idx[ai])
            seen[mi] = True
    return bridge


def _get_chain_index_for_component(item):
    """Array of chain_index, one per component (first atom found)."""
    n_components = len(item.components)
    bridge = np.zeros(n_components, dtype=int)
    seen = np.zeros(n_components, dtype=bool)
    comp_idx = item._get_component_indices().to_numpy()
    chain_idx = item.atoms['chain_index'].to_numpy()
    for ai in range(len(comp_idx)):
        ci = int(comp_idx[ai])
        if not seen[ci]:
            bridge[ci] = int(chain_idx[ai])
            seen[ci] = True
    return bridge


def _get_molecule_index_for_chain(item):
    """Array of molecule_index, one per chain (first group found)."""
    n_chains = len(item.chains)
    bridge = np.zeros(n_chains, dtype=int)
    seen = np.zeros(n_chains, dtype=bool)
    group_idx = item.atoms['group_index'].to_numpy()
    chain_idx = item.atoms['chain_index'].to_numpy()
    mol_idx_arr = item.groups['molecule_index'].to_numpy()
    for ai in range(len(group_idx)):
        ci = int(chain_idx[ai])
        if not seen[ci]:
            bridge[ci] = int(mol_idx_arr[int(group_idx[ai])])
            seen[ci] = True
    return bridge


def _get_molecule_index_for_component(item):
    """Array of molecule_index, one per component (first atom found)."""
    n_components = len(item.components)
    bridge = np.zeros(n_components, dtype=int)
    seen = np.zeros(n_components, dtype=bool)
    comp_idx = item._get_component_indices().to_numpy()
    group_idx = item.atoms['group_index'].to_numpy()
    mol_idx_arr = item.groups['molecule_index'].to_numpy()
    for ai in range(len(comp_idx)):
        ci = int(comp_idx[ai])
        if not seen[ci]:
            bridge[ci] = int(mol_idx_arr[int(group_idx[ai])])
            seen[ci] = True
    return bridge


def _get_component_index_for_group(item):
    """Array of component_index, one per group (first atom found)."""
    n_groups = len(item.groups)
    bridge = np.zeros(n_groups, dtype=int)
    seen = np.zeros(n_groups, dtype=bool)
    group_idx = item.atoms['group_index'].to_numpy()
    comp_idx = item._get_component_indices().to_numpy()
    for ai in range(len(group_idx)):
        gi = int(group_idx[ai])
        if not seen[gi]:
            bridge[gi] = int(comp_idx[ai])
            seen[gi] = True
    return bridge


## ---------------------------------------------------------------------------
## Self-index setters — indices are row positions; no-op
## ---------------------------------------------------------------------------

@arg_digest(form=form)
def set_atom_index_to_atom(item, indices='all', value=None, skip_digestion=False):
    pass


@arg_digest(form=form)
def set_group_index_to_group(item, indices='all', value=None, skip_digestion=False):
    pass


@arg_digest(form=form)
def set_component_index_to_component(item, indices='all', value=None, skip_digestion=False):
    pass


@arg_digest(form=form)
def set_molecule_index_to_molecule(item, indices='all', value=None, skip_digestion=False):
    pass


@arg_digest(form=form)
def set_chain_index_to_chain(item, indices='all', value=None, skip_digestion=False):
    pass


@arg_digest(form=form)
def set_entity_index_to_entity(item, indices='all', value=None, skip_digestion=False):
    pass


## ---------------------------------------------------------------------------
## FK column setters on groups table
## ---------------------------------------------------------------------------

@arg_digest(form=form)
def set_molecule_index_to_group(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.groups['molecule_index'] = value
    else:
        for i, gi in enumerate(list(indices)):
            item.groups.at[gi, 'molecule_index'] = value[i]

    pass


@arg_digest(form=form)
def set_chain_index_to_group(item, indices='all', value=None, skip_digestion=False):
    # chain_index is an atom-level attribute only; groups do not have this column.
    # Setting chain_index via groups is architecturally invalid — no-op.
    pass


@arg_digest(form=form)
def set_component_index_to_group(item, indices='all', value=None, skip_digestion=False):
    # component_index is an atom-level attribute only; groups do not have this column.
    # Setting component_index via groups is architecturally invalid — no-op.
    pass


@arg_digest(form=form)
def set_entity_index_to_group(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = item.groups['molecule_index'].to_numpy()
        _set_by_bridge(item.molecules, 'entity_index', bridge, value)
    else:
        for i, gi in enumerate(list(indices)):
            mi = item.groups.at[gi, 'molecule_index']
            item.molecules.at[int(mi), 'entity_index'] = value[i]

    pass


## ---------------------------------------------------------------------------
## Component attribute setters from group (group→atom→component bridge)
## ---------------------------------------------------------------------------

@arg_digest(form=form)
def set_component_id_to_group(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = _get_component_index_for_group(item)
        _set_by_bridge(item.components, 'component_id', bridge, value)
    else:
        component_indices = item._get_component_indices()
        for i, gi in enumerate(list(indices)):
            ci = component_indices.loc[item.atoms['group_index'] == gi].iloc[0]
            item.components.at[int(ci), 'component_id'] = value[i]

    pass


@arg_digest(form=form)
def set_component_name_to_group(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = _get_component_index_for_group(item)
        _set_by_bridge(item.components, 'component_name', bridge, value)
    else:
        component_indices = item._get_component_indices()
        for i, gi in enumerate(list(indices)):
            ci = component_indices.loc[item.atoms['group_index'] == gi].iloc[0]
            item.components.at[int(ci), 'component_name'] = value[i]

    pass


@arg_digest(form=form)
def set_component_type_to_group(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = _get_component_index_for_group(item)
        _set_by_bridge(item.components, 'component_type', bridge, value)
    else:
        component_indices = item._get_component_indices()
        for i, gi in enumerate(list(indices)):
            ci = component_indices.loc[item.atoms['group_index'] == gi].iloc[0]
            item.components.at[int(ci), 'component_type'] = value[i]

    pass


## ---------------------------------------------------------------------------
## Entity setters from molecule (molecule→entity bridge)
## ---------------------------------------------------------------------------

@arg_digest(form=form)
def set_entity_index_to_molecule(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.molecules['entity_index'] = value
    else:
        for i, mi in enumerate(list(indices)):
            item.molecules.at[mi, 'entity_index'] = value[i]

    pass


@arg_digest(form=form)
def set_entity_id_to_molecule(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = item.molecules['entity_index'].to_numpy()
        _set_by_bridge(item.entities, 'entity_id', bridge, value)
    else:
        for i, mi in enumerate(list(indices)):
            ei = item.molecules.at[mi, 'entity_index']
            item.entities.at[int(ei), 'entity_id'] = value[i]

    pass


@arg_digest(form=form)
def set_entity_name_to_molecule(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = item.molecules['entity_index'].to_numpy()
        _set_by_bridge(item.entities, 'entity_name', bridge, value)
    else:
        for i, mi in enumerate(list(indices)):
            ei = item.molecules.at[mi, 'entity_index']
            item.entities.at[int(ei), 'entity_name'] = value[i]

    pass


@arg_digest(form=form)
def set_entity_type_to_molecule(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = item.molecules['entity_index'].to_numpy()
        _set_by_bridge(item.entities, 'entity_type', bridge, value)
    else:
        for i, mi in enumerate(list(indices)):
            ei = item.molecules.at[mi, 'entity_index']
            item.entities.at[int(ei), 'entity_type'] = value[i]

    pass


## ---------------------------------------------------------------------------
## Chain attribute setters from molecule (molecule→atom→chain bridge)
## ---------------------------------------------------------------------------

@arg_digest(form=form)
def set_chain_id_to_molecule(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = _get_chain_index_for_molecule(item)
        _set_by_bridge(item.chains, 'chain_id', bridge, value)
    else:
        bridge = _get_chain_index_for_molecule(item)
        for i, mi in enumerate(list(indices)):
            ci = bridge[mi]
            item.chains.at[ci, 'chain_id'] = value[i]

    pass


@arg_digest(form=form)
def set_chain_name_to_molecule(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = _get_chain_index_for_molecule(item)
        _set_by_bridge(item.chains, 'chain_name', bridge, value)
    else:
        bridge = _get_chain_index_for_molecule(item)
        for i, mi in enumerate(list(indices)):
            ci = bridge[mi]
            item.chains.at[ci, 'chain_name'] = value[i]

    pass


@arg_digest(form=form)
def set_chain_type_to_molecule(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = _get_chain_index_for_molecule(item)
        _set_by_bridge(item.chains, 'chain_type', bridge, value)
    else:
        bridge = _get_chain_index_for_molecule(item)
        for i, mi in enumerate(list(indices)):
            ci = bridge[mi]
            item.chains.at[ci, 'chain_type'] = value[i]

    pass


@arg_digest(form=form)
def set_chain_index_to_molecule(item, indices='all', value=None, skip_digestion=False):
    """Reassign atoms' chain_index using a per-molecule mapping."""

    group_idx = item.atoms['group_index'].to_numpy()
    mol_idx_arr = item.groups['molecule_index'].to_numpy()
    new_chain = item.atoms['chain_index'].copy().to_numpy()

    if is_all(indices):
        for ai in range(len(group_idx)):
            mi = int(mol_idx_arr[int(group_idx[ai])])
            new_chain[ai] = value[mi]
    else:
        idx_set = set(int(i) for i in indices)
        for ai in range(len(group_idx)):
            mi = int(mol_idx_arr[int(group_idx[ai])])
            if mi in idx_set:
                new_chain[ai] = value[list(indices).index(mi)]

    item.atoms['chain_index'] = new_chain
    n_chains = len(np.unique(new_chain))
    if n_chains != item.chains.shape[0]:
        item.reset_chains(n_chains=n_chains)
        item.rebuild_chains(redefine_indices=True, redefine_ids=True,
                            redefine_types=True, redefine_names=True)

    pass


## ---------------------------------------------------------------------------
## Chain attribute setters from component (component→atom→chain bridge)
## ---------------------------------------------------------------------------

@arg_digest(form=form)
def set_chain_id_to_component(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = _get_chain_index_for_component(item)
        _set_by_bridge(item.chains, 'chain_id', bridge, value)
    else:
        bridge = _get_chain_index_for_component(item)
        for i, ci in enumerate(list(indices)):
            item.chains.at[int(bridge[ci]), 'chain_id'] = value[i]

    pass


@arg_digest(form=form)
def set_chain_name_to_component(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = _get_chain_index_for_component(item)
        _set_by_bridge(item.chains, 'chain_name', bridge, value)
    else:
        bridge = _get_chain_index_for_component(item)
        for i, ci in enumerate(list(indices)):
            item.chains.at[int(bridge[ci]), 'chain_name'] = value[i]

    pass


@arg_digest(form=form)
def set_chain_type_to_component(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = _get_chain_index_for_component(item)
        _set_by_bridge(item.chains, 'chain_type', bridge, value)
    else:
        bridge = _get_chain_index_for_component(item)
        for i, ci in enumerate(list(indices)):
            item.chains.at[int(bridge[ci]), 'chain_type'] = value[i]

    pass


@arg_digest(form=form)
def set_chain_index_to_component(item, indices='all', value=None, skip_digestion=False):
    """Reassign atoms' chain_index using a per-component mapping."""

    comp_idx = item._get_component_indices().to_numpy()
    new_chain = item.atoms['chain_index'].copy().to_numpy()

    if is_all(indices):
        for ai in range(len(comp_idx)):
            ci = int(comp_idx[ai])
            new_chain[ai] = value[ci]
    else:
        idx_set = {int(i): pos for pos, i in enumerate(indices)}
        for ai in range(len(comp_idx)):
            ci = int(comp_idx[ai])
            if ci in idx_set:
                new_chain[ai] = value[idx_set[ci]]

    item.atoms['chain_index'] = new_chain
    n_chains = len(np.unique(new_chain))
    if n_chains != item.chains.shape[0]:
        item.reset_chains(n_chains=n_chains)
        item.rebuild_chains(redefine_indices=True, redefine_ids=True,
                            redefine_types=True, redefine_names=True)

    pass


## ---------------------------------------------------------------------------
## Molecule attribute setters from chain (chain→atom→group→molecule bridge)
## ---------------------------------------------------------------------------

@arg_digest(form=form)
def set_molecule_id_to_chain(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = _get_molecule_index_for_chain(item)
        _set_by_bridge(item.molecules, 'molecule_id', bridge, value)
    else:
        bridge = _get_molecule_index_for_chain(item)
        for i, ci in enumerate(list(indices)):
            item.molecules.at[int(bridge[ci]), 'molecule_id'] = value[i]

    pass


@arg_digest(form=form)
def set_molecule_name_to_chain(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = _get_molecule_index_for_chain(item)
        _set_by_bridge(item.molecules, 'molecule_name', bridge, value)
    else:
        bridge = _get_molecule_index_for_chain(item)
        for i, ci in enumerate(list(indices)):
            item.molecules.at[int(bridge[ci]), 'molecule_name'] = value[i]

    pass


@arg_digest(form=form)
def set_molecule_type_to_chain(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = _get_molecule_index_for_chain(item)
        _set_by_bridge(item.molecules, 'molecule_type', bridge, value)
    else:
        bridge = _get_molecule_index_for_chain(item)
        for i, ci in enumerate(list(indices)):
            item.molecules.at[int(bridge[ci]), 'molecule_type'] = value[i]

    pass


@arg_digest(form=form)
def set_molecule_index_to_chain(item, indices='all', value=None, skip_digestion=False):
    """Reassign groups' molecule_index using a per-chain mapping."""

    group_idx = item.atoms['group_index'].to_numpy()
    chain_idx = item.atoms['chain_index'].to_numpy()
    mol_idx_arr = item.groups['molecule_index'].copy().to_numpy()

    if is_all(indices):
        for ai in range(len(group_idx)):
            ci = int(chain_idx[ai])
            gi = int(group_idx[ai])
            mol_idx_arr[gi] = value[ci]
    else:
        idx_set = {int(i): pos for pos, i in enumerate(indices)}
        for ai in range(len(group_idx)):
            ci = int(chain_idx[ai])
            if ci in idx_set:
                mol_idx_arr[int(group_idx[ai])] = value[idx_set[ci]]

    item.groups['molecule_index'] = mol_idx_arr

    pass


## ---------------------------------------------------------------------------
## Molecule attribute setters from component (component→atom→group→molecule)
## ---------------------------------------------------------------------------

@arg_digest(form=form)
def set_molecule_id_to_component(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = _get_molecule_index_for_component(item)
        _set_by_bridge(item.molecules, 'molecule_id', bridge, value)
    else:
        bridge = _get_molecule_index_for_component(item)
        for i, ci in enumerate(list(indices)):
            item.molecules.at[int(bridge[ci]), 'molecule_id'] = value[i]

    pass


@arg_digest(form=form)
def set_molecule_name_to_component(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = _get_molecule_index_for_component(item)
        _set_by_bridge(item.molecules, 'molecule_name', bridge, value)
    else:
        bridge = _get_molecule_index_for_component(item)
        for i, ci in enumerate(list(indices)):
            item.molecules.at[int(bridge[ci]), 'molecule_name'] = value[i]

    pass


@arg_digest(form=form)
def set_molecule_type_to_component(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = _get_molecule_index_for_component(item)
        _set_by_bridge(item.molecules, 'molecule_type', bridge, value)
    else:
        bridge = _get_molecule_index_for_component(item)
        for i, ci in enumerate(list(indices)):
            item.molecules.at[int(bridge[ci]), 'molecule_type'] = value[i]

    pass


@arg_digest(form=form)
def set_molecule_index_to_component(item, indices='all', value=None, skip_digestion=False):
    """Reassign groups' molecule_index using a per-component mapping."""

    comp_idx = item._get_component_indices().to_numpy()
    group_idx = item.atoms['group_index'].to_numpy()
    mol_idx_arr = item.groups['molecule_index'].copy().to_numpy()

    if is_all(indices):
        for ai in range(len(comp_idx)):
            ci = int(comp_idx[ai])
            gi = int(group_idx[ai])
            mol_idx_arr[gi] = value[ci]
    else:
        idx_set = {int(i): pos for pos, i in enumerate(indices)}
        for ai in range(len(comp_idx)):
            ci = int(comp_idx[ai])
            if ci in idx_set:
                mol_idx_arr[int(group_idx[ai])] = value[idx_set[ci]]

    item.groups['molecule_index'] = mol_idx_arr

    pass


## ---------------------------------------------------------------------------
## Entity attribute setters from chain (chain→mol→entity bridge)
## ---------------------------------------------------------------------------

@arg_digest(form=form)
def set_entity_index_to_chain(item, indices='all', value=None, skip_digestion=False):
    """Set entity_index in molecules table using a per-chain mapping."""

    mol_for_chain = _get_molecule_index_for_chain(item)

    if is_all(indices):
        for ci, mi in enumerate(mol_for_chain):
            item.molecules.at[int(mi), 'entity_index'] = value[ci]
    else:
        for i, ci in enumerate(list(indices)):
            item.molecules.at[int(mol_for_chain[ci]), 'entity_index'] = value[i]

    pass


@arg_digest(form=form)
def set_entity_id_to_chain(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        mol_for_chain = _get_molecule_index_for_chain(item)
        ent_idx = item.molecules['entity_index'].to_numpy()
        bridge = ent_idx[mol_for_chain]
        _set_by_bridge(item.entities, 'entity_id', bridge, value)
    else:
        mol_for_chain = _get_molecule_index_for_chain(item)
        for i, ci in enumerate(list(indices)):
            mi = int(mol_for_chain[ci])
            ei = item.molecules.at[mi, 'entity_index']
            item.entities.at[int(ei), 'entity_id'] = value[i]

    pass


@arg_digest(form=form)
def set_entity_name_to_chain(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        mol_for_chain = _get_molecule_index_for_chain(item)
        ent_idx = item.molecules['entity_index'].to_numpy()
        bridge = ent_idx[mol_for_chain]
        _set_by_bridge(item.entities, 'entity_name', bridge, value)
    else:
        mol_for_chain = _get_molecule_index_for_chain(item)
        for i, ci in enumerate(list(indices)):
            mi = int(mol_for_chain[ci])
            ei = item.molecules.at[mi, 'entity_index']
            item.entities.at[int(ei), 'entity_name'] = value[i]

    pass


@arg_digest(form=form)
def set_entity_type_to_chain(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        mol_for_chain = _get_molecule_index_for_chain(item)
        ent_idx = item.molecules['entity_index'].to_numpy()
        bridge = ent_idx[mol_for_chain]
        _set_by_bridge(item.entities, 'entity_type', bridge, value)
    else:
        mol_for_chain = _get_molecule_index_for_chain(item)
        for i, ci in enumerate(list(indices)):
            mi = int(mol_for_chain[ci])
            ei = item.molecules.at[mi, 'entity_index']
            item.entities.at[int(ei), 'entity_type'] = value[i]

    pass


## ---------------------------------------------------------------------------
## Entity attribute setters from component (comp→mol→entity bridge)
## ---------------------------------------------------------------------------

@arg_digest(form=form)
def set_entity_index_to_component(item, indices='all', value=None, skip_digestion=False):
    """Set entity_index in molecules table using a per-component mapping."""

    mol_for_comp = _get_molecule_index_for_component(item)

    if is_all(indices):
        for ci, mi in enumerate(mol_for_comp):
            item.molecules.at[int(mi), 'entity_index'] = value[ci]
    else:
        for i, ci in enumerate(list(indices)):
            item.molecules.at[int(mol_for_comp[ci]), 'entity_index'] = value[i]

    pass


@arg_digest(form=form)
def set_entity_id_to_component(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        mol_for_comp = _get_molecule_index_for_component(item)
        ent_idx = item.molecules['entity_index'].to_numpy()
        bridge = ent_idx[mol_for_comp]
        _set_by_bridge(item.entities, 'entity_id', bridge, value)
    else:
        mol_for_comp = _get_molecule_index_for_component(item)
        for i, ci in enumerate(list(indices)):
            mi = int(mol_for_comp[ci])
            ei = item.molecules.at[mi, 'entity_index']
            item.entities.at[int(ei), 'entity_id'] = value[i]

    pass


@arg_digest(form=form)
def set_entity_name_to_component(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        mol_for_comp = _get_molecule_index_for_component(item)
        ent_idx = item.molecules['entity_index'].to_numpy()
        bridge = ent_idx[mol_for_comp]
        _set_by_bridge(item.entities, 'entity_name', bridge, value)
    else:
        mol_for_comp = _get_molecule_index_for_component(item)
        for i, ci in enumerate(list(indices)):
            mi = int(mol_for_comp[ci])
            ei = item.molecules.at[mi, 'entity_index']
            item.entities.at[int(ei), 'entity_name'] = value[i]

    pass


@arg_digest(form=form)
def set_entity_type_to_component(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        mol_for_comp = _get_molecule_index_for_component(item)
        ent_idx = item.molecules['entity_index'].to_numpy()
        bridge = ent_idx[mol_for_comp]
        _set_by_bridge(item.entities, 'entity_type', bridge, value)
    else:
        mol_for_comp = _get_molecule_index_for_component(item)
        for i, ci in enumerate(list(indices)):
            mi = int(mol_for_comp[ci])
            ei = item.molecules.at[mi, 'entity_index']
            item.entities.at[int(ei), 'entity_type'] = value[i]

    pass
