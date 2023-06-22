from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw

###### Set

## Atom

@digest(form='molsysmt.Topology')
def set_atom_name_to_atom(item, indices='all', value=None):

    item.atoms_dataframe.loc[indices, 'atom_name']=value

    pass

@digest(form='molsysmt.Topology')
def set_atom_id_to_atom(item, indices='all', value=None):

    item.atoms_dataframe.loc[indices, 'atom_id']=value

    pass

## Group

@digest(form='molsysmt.Topology')
def set_group_name_to_group(item, indices='all', value=None):

    from . import get_atom_index_from_group

    atom_indices_in_groups = get_atom_index_from_group(item, indices=indices)
    for atom_indices in atom_indices_in_groups:
        item.atoms_dataframe.loc[atom_indices, 'group_name']=value

    pass


## System


