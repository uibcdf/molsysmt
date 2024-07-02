from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form='molsysmt.Topology'


###### Set

## Atom

@digest(form=form)
def set_atom_id_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.atoms.atom_id=value
    else:
        item.atoms.iloc[indices, 0]=value

    pass

@digest(form=form)
def set_atom_name_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.atoms.atom_name=value
    else:
        item.atoms.iloc[indices, 1]=value

    pass

@digest(form=form)
def set_atom_type_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.atoms.atom_type=value
    else:
        item.atoms.iloc[indices, 2]=value

    pass

@digest(form=form)
def set_group_index_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.atoms.group_index=value
    else:
        item.atoms.iloc[indices, 3]=value

    pass

@digest(form=form)
def set_chain_index_to_atom(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        if len(value)==1:
            item.atoms.chain_index=value[0]
        else:
            item.atoms.chain_index=value
    else:
        item.atoms.iloc[indices, 4]=value

    pass

#@digest(form=form)
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


## Group

@digest(form=form)
def set_group_id_to_group(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.groups.group_id=value
    else:
        item.groups.iloc[indices, 0]=value

    pass

@digest(form=form)
def set_group_name_to_group(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.groups.group_name=value
    else:
        item.groups.iloc[indices, 1]=value

    pass

@digest(form=form)
def set_group_type_to_group(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.groups.group_type=value
    else:
        item.groups.iloc[indices, 2]=value

    pass

@digest(form=form)
def set_component_index_to_group(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.groups.component_index=value
    else:
        item.groups.iloc[indices, 3]=value

    pass


## Component

@digest(form=form)
def set_component_id_to_component(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.components.component_id=value
    else:
        item.components.iloc[indices, 0]=value

    pass

@digest(form=form)
def set_component_name_to_component(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.components.component_name=value
    else:
        item.components.iloc[indices, 1]=value

    pass

@digest(form=form)
def set_component_type_to_component(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.components.component_type=value
    else:
        item.components.iloc[indices, 2]=value

    pass


## Molecule

@digest(form=form)
def set_molecule_id_to_molecule(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.molecules.molecule_id=value
    else:
        item.molecules.iloc[indices, 0]=value

    pass

@digest(form=form)
def set_molecule_name_to_molecule(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.molecules.molecule_name=value
    else:
        item.molecules.iloc[indices, 1]=value

    pass

@digest(form=form)
def set_molecule_type_to_molecule(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.molecules.molecule_type=value
    else:
        item.molecules.iloc[indices, 2]=value

    pass


## Chain

@digest(form=form)
def set_chain_id_to_chain(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.chains.chain_id=value
    else:
        item.chains.iloc[indices, 0]=value

    pass

@digest(form=form)
def set_chain_name_to_chain(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.chains.chain_name=value
    else:
        item.chains.iloc[indices, 1]=value

    pass

@digest(form=form)
def set_chain_type_to_chain(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.chains.chain_type=value
    else:
        item.chains.iloc[indices, 2]=value

    pass


## Entity

@digest(form=form)
def set_entity_id_to_entity(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.entities.entity_id=value
    else:
        item.entities.iloc[indices, 0]=value

    pass

@digest(form=form)
def set_entity_name_to_entity(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.entities.entity_name=value
    else:
        item.entities.iloc[indices, 1]=value

    pass

@digest(form=form)
def set_entity_type_to_entity(item, indices='all', value=None, skip_digestion=False):

    if is_all(indices):
        item.entities.entity_type=value
    else:
        item.entities.iloc[indices, 2]=value

    pass

