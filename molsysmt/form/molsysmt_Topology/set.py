from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form='molsysmt.Topology'

###### Set

## Atom

@digest(form=form)
def set_atom_index_to_atom(item, indices='all', value=None):

    if is_all(indices):
        item.atoms_dataframe['atom_index']=value
    else:
        item.atoms_dataframe.loc[indices, 'atom_index']=value

    pass

@digest(form=form)
def set_atom_name_to_atom(item, indices='all', value=None):

    if is_all(indices):
        item.atoms_dataframe['atom_name']=value
    else:
        item.atoms_dataframe.loc[indices, 'atom_name']=value

    pass

@digest(form=form)
def set_atom_id_to_atom(item, indices='all', value=None):

    if is_all(indices):
        item.atoms_dataframe['atom_id']=value
    else:
        item.atoms_dataframe.loc[indices, 'atom_id']=value

    pass

@digest(form=form)
def set_atom_type_to_atom(item, indices='all', value=None):

    if is_all(indices):
        item.atoms_dataframe['atom_type']=value
    else:
        item.atoms_dataframe.loc[indices, 'atom_type']=value

    pass

@digest(form=form)
def set_group_index_to_atom(item, indices='all', value=None):

    if is_all(indices):
        item.atoms_dataframe['group_index']=value
    else:
        item.atoms_dataframe.loc[indices, 'group_index']=value

    pass

@digest(form=form)
def set_group_name_to_atom(item, indices='all', value=None):

    if is_all(indices):
        item.atoms_dataframe['group_name']=value
    else:
        item.atoms_dataframe.loc[indices, 'group_name']=value

    pass

@digest(form=form)
def set_group_id_to_atom(item, indices='all', value=None):

    if is_all(indices):
        item.atoms_dataframe['group_id']=value
    else:
        item.atoms_dataframe.loc[indices, 'group_id']=value

    pass

@digest(form=form)
def set_group_type_to_atom(item, indices='all', value=None):

    if is_all(indices):
        item.atoms_dataframe['group_type']=value
    else:
        item.atoms_dataframe.loc[indices, 'group_type']=value

    pass

@digest(form=form)
def set_component_index_to_atom(item, indices='all', value=None):

    if is_all(indices):
        item.atoms_dataframe['component_index']=value
    else:
        item.atoms_dataframe.loc[indices, 'component_index']=value

    pass

@digest(form=form)
def set_component_name_to_atom(item, indices='all', value=None):

    if is_all(indices):
        item.atoms_dataframe['component_name']=value
    else:
        item.atoms_dataframe.loc[indices, 'component_name']=value

    pass

@digest(form=form)
def set_component_id_to_atom(item, indices='all', value=None):

    if is_all(indices):
        item.atoms_dataframe['component_id']=value
    else:
        item.atoms_dataframe.loc[indices, 'component_id']=value

    pass

@digest(form=form)
def set_component_type_to_atom(item, indices='all', value=None):

    if is_all(indices):
        item.atoms_dataframe['component_type']=value
    else:
        item.atoms_dataframe.loc[indices, 'component_type']=value

    pass

@digest(form=form)
def set_molecule_index_to_atom(item, indices='all', value=None):

    if is_all(indices):
        item.atoms_dataframe['molecule_index']=value
    else:
        item.atoms_dataframe.loc[indices, 'molecule_index']=value

    pass

@digest(form=form)
def set_molecule_name_to_atom(item, indices='all', value=None):

    if is_all(indices):
        item.atoms_dataframe['molecule_name']=value
    else:
        item.atoms_dataframe.loc[indices, 'molecule_name']=value

    pass

@digest(form=form)
def set_molecule_id_to_atom(item, indices='all', value=None):

    if is_all(indices):
        item.atoms_dataframe['molecule_id']=value
    else:
        item.atoms_dataframe.loc[indices, 'molecule_id']=value

    pass

@digest(form=form)
def set_molecule_type_to_atom(item, indices='all', value=None):

    if is_all(indices):
        item.atoms_dataframe['molecule_type']=value
    else:
        item.atoms_dataframe.loc[indices, 'molecule_type']=value

    pass

@digest(form=form)
def set_chain_index_to_atom(item, indices='all', value=None):

    if is_all(indices):
        item.atoms_dataframe['chain_index']=value
    else:
        item.atoms_dataframe.loc[indices, 'chain_index']=value

    pass

@digest(form=form)
def set_chain_name_to_atom(item, indices='all', value=None):

    if is_all(indices):
        item.atoms_dataframe['chain_name']=value
    else:
        item.atoms_dataframe.loc[indices, 'chain_name']=value

    pass

@digest(form=form)
def set_chain_id_to_atom(item, indices='all', value=None):

    if is_all(indices):
        item.atoms_dataframe['chain_id']=value
        item.atoms_dataframe['chain_index']=0
    else:
        item.atoms_dataframe.loc[indices, 'chain_id']=value
        aux_list = item.atoms_dataframe['chain_id'].unique()
        for new_index, id for enumerate(aux_list):
            item[item['chain_id']==id]=new_index

    pass

@digest(form=form)
def set_chain_type_to_atom(item, indices='all', value=None):

    if is_all(indices):
        item.atoms_dataframe['chain_type']=value
    else:
        item.atoms_dataframe.loc[indices, 'chain_type']=value

    pass

@digest(form=form)
def set_entity_index_to_atom(item, indices='all', value=None):

    if is_all(indices):
        item.atoms_dataframe['entity_index']=value
    else:
        item.atoms_dataframe.loc[indices, 'entity_index']=value

    pass

@digest(form=form)
def set_entity_name_to_atom(item, indices='all', value=None):

    if is_all(indices):
        item.atoms_dataframe['entity_name']=value
    else:
        item.atoms_dataframe.loc[indices, 'entity_name']=value

    pass

@digest(form=form)
def set_entity_id_to_atom(item, indices='all', value=None):

    if is_all(indices):
        item.atoms_dataframe['entity_id']=value
    else:
        item.atoms_dataframe.loc[indices, 'entity_id']=value

    pass

@digest(form=form)
def set_entity_type_to_atom(item, indices='all', value=None):

    if is_all(indices):
        item.atoms_dataframe['entity_type']=value
    else:
        item.atoms_dataframe.loc[indices, 'entity_type']=value

    pass


## Group

@digest(form=form)
def set_group_index_to_group(item, indices='all', value=None):

    from . import get_atom_index_from_group

    atom_indices_in_groups = get_atom_index_from_group(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_groups)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_groups, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_groups)
        del(temp_value)

    set_group_index_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_group_name_to_group(item, indices='all', value=None):

    from . import get_atom_index_from_group

    atom_indices_in_groups = get_atom_index_from_group(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_groups)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_groups, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_groups)
        del(temp_value)

    set_group_name_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_group_id_to_group(item, indices='all', value=None):

    from . import get_atom_index_from_group

    atom_indices_in_groups = get_atom_index_from_group(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_groups)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_groups, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_groups)
        del(temp_value)

    set_group_id_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_group_type_to_group(item, indices='all', value=None):

    from . import get_atom_index_from_group

    atom_indices_in_groups = get_atom_index_from_group(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_groups)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_groups, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_groups)
        del(temp_value)

    set_group_type_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_component_index_to_group(item, indices='all', value=None):

    from . import get_atom_index_from_group

    atom_indices_in_groups = get_atom_index_from_group(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_groups)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_groups, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_groups)
        del(temp_value)

    set_component_index_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_component_id_to_group(item, indices='all', value=None):

    from . import get_atom_index_from_group

    atom_indices_in_groups = get_atom_index_from_group(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_groups)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_groups, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_groups)
        del(temp_value)

    set_component_id_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_component_name_to_group(item, indices='all', value=None):

    from . import get_atom_index_from_group

    atom_indices_in_groups = get_atom_index_from_group(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_groups)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_groups, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_groups)
        del(temp_value)

    set_component_name_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_component_type_to_group(item, indices='all', value=None):

    from . import get_atom_index_from_group

    atom_indices_in_groups = get_atom_index_from_group(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_groups)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_groups, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_groups)
        del(temp_value)

    set_component_type_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_molecule_index_to_group(item, indices='all', value=None):

    from . import get_atom_index_from_group

    atom_indices_in_groups = get_atom_index_from_group(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_groups)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_groups, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_groups)
        del(temp_value)

    set_molecule_index_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_molecule_id_to_group(item, indices='all', value=None):

    from . import get_atom_index_from_group

    atom_indices_in_groups = get_atom_index_from_group(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_groups)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_groups, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_groups)
        del(temp_value)

    set_molecule_id_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_molecule_name_to_group(item, indices='all', value=None):

    from . import get_atom_index_from_group

    atom_indices_in_groups = get_atom_index_from_group(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_groups)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_groups, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_groups)
        del(temp_value)

    set_molecule_name_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_molecule_type_to_group(item, indices='all', value=None):

    from . import get_atom_index_from_group

    atom_indices_in_groups = get_atom_index_from_group(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_groups)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_groups, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_groups)
        del(temp_value)

    set_molecule_type_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_chain_index_to_group(item, indices='all', value=None):

    from . import get_atom_index_from_group

    atom_indices_in_groups = get_atom_index_from_group(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_groups)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_groups, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_groups)
        del(temp_value)

    set_chain_index_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_chain_id_to_group(item, indices='all', value=None):

    from . import get_atom_index_from_group

    atom_indices_in_groups = get_atom_index_from_group(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_groups)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_groups, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_groups)
        del(temp_value)

    set_chain_id_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_chain_name_to_group(item, indices='all', value=None):

    from . import get_atom_index_from_group

    atom_indices_in_groups = get_atom_index_from_group(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_groups)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_groups, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_groups)
        del(temp_value)

    set_chain_name_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_chain_type_to_group(item, indices='all', value=None):

    from . import get_atom_index_from_group

    atom_indices_in_groups = get_atom_index_from_group(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_groups)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_groups, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_groups)
        del(temp_value)

    set_chain_type_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_entity_index_to_group(item, indices='all', value=None):

    from . import get_atom_index_from_group

    atom_indices_in_groups = get_atom_index_from_group(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_groups)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_groups, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_groups)
        del(temp_value)

    set_entity_index_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_entity_id_to_group(item, indices='all', value=None):

    from . import get_atom_index_from_group

    atom_indices_in_groups = get_atom_index_from_group(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_groups)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_groups, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_groups)
        del(temp_value)

    set_entity_id_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_entity_name_to_group(item, indices='all', value=None):

    from . import get_atom_index_from_group

    atom_indices_in_groups = get_atom_index_from_group(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_groups)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_groups, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_groups)
        del(temp_value)

    set_entity_name_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_entity_type_to_group(item, indices='all', value=None):

    from . import get_atom_index_from_group

    atom_indices_in_groups = get_atom_index_from_group(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_groups)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_groups, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_groups)
        del(temp_value)

    set_entity_type_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

## Component

@digest(form=form)
def set_component_index_to_component(item, indices='all', value=None):

    from . import get_atom_index_from_component

    atom_indices_in_components = get_atom_index_from_component(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_components)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_components, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_components)
        del(temp_value)

    set_component_index_to_component(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_component_id_to_component(item, indices='all', value=None):

    from . import get_atom_index_from_component

    atom_indices_in_components = get_atom_index_from_component(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_components)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_components, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_components)
        del(temp_value)

    set_component_id_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_component_name_to_component(item, indices='all', value=None):

    from . import get_atom_index_from_component

    atom_indices_in_components = get_atom_index_from_component(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_components)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_components, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_components)
        del(temp_value)

    set_component_name_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_component_type_to_component(item, indices='all', value=None):

    from . import get_atom_index_from_component

    atom_indices_in_components = get_atom_index_from_component(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_components)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_components, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_components)
        del(temp_value)

    set_component_type_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_molecule_index_to_component(item, indices='all', value=None):

    from . import get_atom_index_from_component

    atom_indices_in_components = get_atom_index_from_component(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_components)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_components, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_components)
        del(temp_value)

    set_molecule_index_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_molecule_id_to_component(item, indices='all', value=None):

    from . import get_atom_index_from_component

    atom_indices_in_components = get_atom_index_from_component(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_components)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_components, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_components)
        del(temp_value)

    set_molecule_id_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_molecule_name_to_component(item, indices='all', value=None):

    from . import get_atom_index_from_component

    atom_indices_in_components = get_atom_index_from_component(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_components)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_components, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_components)
        del(temp_value)

    set_molecule_name_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_molecule_type_to_component(item, indices='all', value=None):

    from . import get_atom_index_from_component

    atom_indices_in_components = get_atom_index_from_component(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_components)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_components, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_components)
        del(temp_value)

    set_molecule_type_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_chain_index_to_component(item, indices='all', value=None):

    from . import get_atom_index_from_component

    atom_indices_in_components = get_atom_index_from_component(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_components)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_components, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_components)
        del(temp_value)

    set_chain_index_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_chain_id_to_component(item, indices='all', value=None):

    from . import get_atom_index_from_component

    atom_indices_in_components = get_atom_index_from_component(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_components)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_components, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_components)
        del(temp_value)

    set_chain_id_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_chain_name_to_component(item, indices='all', value=None):

    from . import get_atom_index_from_component

    atom_indices_in_components = get_atom_index_from_component(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_components)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_components, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_components)
        del(temp_value)

    set_chain_name_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_chain_type_to_component(item, indices='all', value=None):

    from . import get_atom_index_from_component

    atom_indices_in_components = get_atom_index_from_component(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_components)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_components, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_components)
        del(temp_value)

    set_chain_type_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_entity_index_to_component(item, indices='all', value=None):

    from . import get_atom_index_from_component

    atom_indices_in_components = get_atom_index_from_component(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_components)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_components, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_components)
        del(temp_value)

    set_entity_index_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_entity_id_to_component(item, indices='all', value=None):

    from . import get_atom_index_from_component

    atom_indices_in_components = get_atom_index_from_component(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_components)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_components, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_components)
        del(temp_value)

    set_entity_id_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_entity_type_to_component(item, indices='all', value=None):

    from . import get_atom_index_from_component

    atom_indices_in_components = get_atom_index_from_component(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_components)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_components, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_components)
        del(temp_value)

    set_entity_type_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

## Molecule

@digest(form=form)
def set_molecule_index_to_molecule(item, indices='all', value=None):

    from . import get_atom_index_from_molecule

    atom_indices_in_molecules = get_atom_index_from_molecule(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_molecules)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_molecules, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_molecules)
        del(temp_value)

    set_molecule_index_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_molecule_id_to_molecule(item, indices='all', value=None):

    from . import get_atom_index_from_molecule

    atom_indices_in_molecules = get_atom_index_from_molecule(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_molecules)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_molecules, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_molecules)
        del(temp_value)

    set_molecule_id_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_molecule_name_to_molecule(item, indices='all', value=None):

    from . import get_atom_index_from_molecule

    atom_indices_in_molecules = get_atom_index_from_molecule(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_molecules)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_molecules, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_molecules)
        del(temp_value)

    set_molecule_name_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_molecule_type_to_molecule(item, indices='all', value=None):

    from . import get_atom_index_from_molecule

    atom_indices_in_molecules = get_atom_index_from_molecule(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_molecules)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_molecules, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_molecules)
        del(temp_value)

    set_molecule_type_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_chain_index_to_molecule(item, indices='all', value=None):

    from . import get_atom_index_from_molecule

    atom_indices_in_molecules = get_atom_index_from_molecule(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_molecules)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_molecules, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_molecules)
        del(temp_value)

    set_chain_index_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_chain_id_to_molecule(item, indices='all', value=None):

    from . import get_atom_index_from_molecule

    atom_indices_in_molecules = get_atom_index_from_molecule(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_molecules)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_molecules, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_molecules)
        del(temp_value)

    set_chain_id_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_chain_name_to_molecule(item, indices='all', value=None):

    from . import get_atom_index_from_molecule

    atom_indices_in_molecules = get_atom_index_from_molecule(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_molecules)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_molecules, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_molecules)
        del(temp_value)

    set_chain_name_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_chain_type_to_molecule(item, indices='all', value=None):

    from . import get_atom_index_from_molecule

    atom_indices_in_molecules = get_atom_index_from_molecule(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_molecules)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_molecules, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_molecules)
        del(temp_value)

    set_chain_type_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_entity_index_to_molecule(item, indices='all', value=None):

    from . import get_atom_index_from_molecule

    atom_indices_in_molecules = get_atom_index_from_molecule(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_molecules)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_molecules, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_molecules)
        del(temp_value)

    set_entity_index_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_entity_id_to_molecule(item, indices='all', value=None):

    from . import get_atom_index_from_molecule

    atom_indices_in_molecules = get_atom_index_from_molecule(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_molecules)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_molecules, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_molecules)
        del(temp_value)

    set_entity_id_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_entity_type_to_molecule(item, indices='all', value=None):

    from . import get_atom_index_from_molecule

    atom_indices_in_molecules = get_atom_index_from_molecule(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_molecules)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_molecules, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_molecules)
        del(temp_value)

    set_entity_type_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

## Chain

@digest(form=form)
def set_chain_index_to_chain(item, indices='all', value=None):

    from . import get_atom_index_from_chain

    atom_indices_in_chains = get_atom_index_from_chain(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_chains)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_chains, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_chains)
        del(temp_value)

    set_chain_index_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_chain_id_to_chain(item, indices='all', value=None):

    from . import get_atom_index_from_chain

    atom_indices_in_chains = get_atom_index_from_chain(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_chains)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_chains, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_chains)
        del(temp_value)

    set_chain_id_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_chain_name_to_chain(item, indices='all', value=None):

    from . import get_atom_index_from_chain

    atom_indices_in_chains = get_atom_index_from_chain(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_chains)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_chains, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_chains)
        del(temp_value)

    set_chain_name_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_chain_type_to_chain(item, indices='all', value=None):

    from . import get_atom_index_from_chain

    atom_indices_in_chains = get_atom_index_from_chain(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_chains)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_chains, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_chains)
        del(temp_value)

    set_chain_type_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_entity_index_to_chain(item, indices='all', value=None):

    from . import get_atom_index_from_chain

    atom_indices_in_chains = get_atom_index_from_chain(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_chains)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_chains, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_chains)
        del(temp_value)

    set_entity_index_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_entity_id_to_chain(item, indices='all', value=None):

    from . import get_atom_index_from_chain

    atom_indices_in_chains = get_atom_index_from_chain(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_chains)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_chains, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_chains)
        del(temp_value)

    set_entity_id_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_entity_type_to_chain(item, indices='all', value=None):

    from . import get_atom_index_from_chain

    atom_indices_in_chains = get_atom_index_from_chain(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_chains)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_chains, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_chains)
        del(temp_value)

    set_entity_type_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

## Entity

@digest(form=form)
def set_entity_index_to_entity(item, indices='all', value=None):

    from . import get_atom_index_from_entity

    atom_indices_in_entities = get_atom_index_from_entity(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_entities)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_entities, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_entities)
        del(temp_value)

    set_entity_index_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_entity_id_to_entity(item, indices='all', value=None):

    from . import get_atom_index_from_entity

    atom_indices_in_entities = get_atom_index_from_entity(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_entities)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_entities, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_entities)
        del(temp_value)

    set_entity_id_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

@digest(form=form)
def set_entity_type_to_entity(item, indices='all', value=None):

    from . import get_atom_index_from_entity

    atom_indices_in_entities = get_atom_index_from_entity(item, indices=indices)

    if isinstance(value, (int, str)):
        atom_indices = np.concatenate(atom_indices_in_entities)
        value = np.full((len(atom_indices)), value)
    else:
        temp_value=[]
        for atom_indices, aux_value in zip(atom_indices_in_entities, value):
            temp_value+=[aux_value for ii in atom_indices]
        value = np.array(temp_value)
        atom_indices = np.concatenate(atom_indices_in_entities)
        del(temp_value)

    set_entity_type_to_atom(item, indices=atom_indices, value=value)

    del(indices, atom_indices, value)

    pass

## System


