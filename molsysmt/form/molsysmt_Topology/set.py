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

## System


