from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form='molsysmt.Topology'


###### Set

## Atom

@arg_digest(form=form)
def set_atom_id_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.atoms.atom_id=value
    else:
        item.atoms.iloc[indices, 0]=value

    pass

@arg_digest(form=form)
def set_atom_name_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.atoms.atom_name=value
    else:
        item.atoms.iloc[indices, 1]=value

    pass

@arg_digest(form=form)
def set_atom_type_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.atoms.atom_type=value
    else:
        item.atoms.iloc[indices, 2]=value

    pass

@arg_digest(form=form)
def set_group_index_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.atoms.group_index=value
    else:
        item.atoms.iloc[indices, 3]=value

    pass

@arg_digest(form=form)
def set_component_index_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        if len(value)==1:
            item.atoms.component_index=value[0]
            n_components = 1
        else:
            item.atoms.component_index=value
            n_components = np.unique(value).shape[0]
        if n_components!=item.components.shape[0]:
            item.reset_components(n_components=n_components)
            item.rebuild_components(redefine_indices=True, redefine_ids=True,
                                    redefine_types=True, redefine_names=True)
    else:
        item.atoms.iloc[indices, 4]=value

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
        item.atoms.iloc[indices, 5]=value

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
        bridge = item.atoms['component_index'].to_numpy()
        _set_by_bridge(item.components, 'component_id', bridge, value)
    else:
        for i, ai in enumerate(list(indices)):
            ci = item.atoms.at[ai, 'component_index']
            item.components.at[int(ci), 'component_id'] = value[i]

    pass


@arg_digest(form=form)
def set_component_name_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = item.atoms['component_index'].to_numpy()
        _set_by_bridge(item.components, 'component_name', bridge, value)
    else:
        for i, ai in enumerate(list(indices)):
            ci = item.atoms.at[ai, 'component_index']
            item.components.at[int(ci), 'component_name'] = value[i]

    pass


@arg_digest(form=form)
def set_component_type_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = item.atoms['component_index'].to_numpy()
        _set_by_bridge(item.components, 'component_type', bridge, value)
    else:
        for i, ai in enumerate(list(indices)):
            ci = item.atoms.at[ai, 'component_index']
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


@arg_digest(form=form)
def set_chain_id_to_group(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = item.groups['chain_index'].to_numpy()
        _set_by_bridge(item.chains, 'chain_id', bridge, value)
    else:
        for i, gi in enumerate(list(indices)):
            ci = item.groups.at[gi, 'chain_index']
            item.chains.at[int(ci), 'chain_id'] = value[i]

    pass


@arg_digest(form=form)
def set_chain_name_to_group(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = item.groups['chain_index'].to_numpy()
        _set_by_bridge(item.chains, 'chain_name', bridge, value)
    else:
        for i, gi in enumerate(list(indices)):
            ci = item.groups.at[gi, 'chain_index']
            item.chains.at[int(ci), 'chain_name'] = value[i]

    pass


@arg_digest(form=form)
def set_chain_type_to_group(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        bridge = item.groups['chain_index'].to_numpy()
        _set_by_bridge(item.chains, 'chain_type', bridge, value)
    else:
        for i, gi in enumerate(list(indices)):
            ci = item.groups.at[gi, 'chain_index']
            item.chains.at[int(ci), 'chain_type'] = value[i]

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

