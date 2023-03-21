#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.execfile import execfile
from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form='nglview.NGLWidget'

## From atom

@digest(form=form)
def get_atom_id_from_atom(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_id_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_atom_name_from_atom(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_name_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_atom_type_from_atom(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_type_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_group_index_from_atom(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_index_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_component_index_from_atom(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_index_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_chain_index_from_atom(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_index_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_molecule_index_from_atom(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_index_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_entity_index_from_atom(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_index_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_inner_bonded_atoms_from_atom(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_inner_bonded_atoms_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_inner_bonds_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all'):

    if is_all(structure_indices):
        n_structures = get_n_structures_from_system(item)
        structure_indices = np.arange(n_structures)

    coordinates = []

    for ii in structure_indices:
        if is_all(indices):
            coordinates.append(item.component_0.get_coordinates(ii))
        else:
            coordinates.append(item.component_0.get_coordinates(ii)[indices,:])

    coordinates = np.array(coordinates)
    coordinates = puw.quantity(coordinates, unit='angstroms')
    coordinates = puw.standardize(coordinates)

    return coordinates

## From group

@digest(form=form)
def get_group_id_from_group(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_id_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_group_name_from_group(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_name_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_group_type_from_group(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_type_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

## From component

@digest(form=form)
def get_component_id_from_component(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_id_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_component_name_from_component(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_name_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_component_type_from_component(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_type_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

## From molecule

@digest(form=form)
def get_molecule_id_from_molecule(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_id_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_molecule_name_from_molecule(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_name_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_molecule_type_from_molecule(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_type_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

## From chain

@digest(form=form)
def get_chain_id_from_chain(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_id_from_chain as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_chain_name_from_chain(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_name_from_chain as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_chain_type_from_chain(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_type_from_chain as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

## From entity

@digest(form=form)
def get_entity_id_from_entity(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_id_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_entity_name_from_entity(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_name_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_entity_type_from_entity(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output


## From system

@digest(form=form)
def get_n_atoms_from_system(item):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_atoms_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item)

    return output

@digest(form=form)
def get_n_groups_from_system(item):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_groups_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item)

    return output

@digest(form=form)
def get_n_components_from_system(item):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_components_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item)

    return output

@digest(form=form)
def get_n_chains_from_system(item):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_chains_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item)

    return output

@digest(form=form)
def get_n_molecules_from_system(item):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_molecules_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item)

    return output

@digest(form=form)
def get_n_entities_from_system(item):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_entities_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item)

    return output

@digest(form=form)
def get_n_bonds_from_system(item):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_bonds_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item)

    return output

@digest(form=form)
def get_n_structures_from_system(item, structure_indices='all'):

    if is_all(structure_indices):
        n_structures = item.component_0.n_frames
    else:
        n_structures = len(structure_indices)

    return n_structures

@digest(form=form)
def get_box_from_system(item, structure_indices='all'):

    from . import to_string_pdb_text
    from ..string_pdb_text import get_box_from_system as aux_get

    tmp_item = to_string_pdb_text(item)
    output = aux_get(tmp_item)

    return output

@digest(form=form)
def get_time_from_system(item, structure_indices='all'):

    from . import to_string_pdb_text
    from ..string_pdb_text import get_time_from_system as aux_get

    tmp_item = to_string_pdb_text(item)
    output = aux_get(tmp_item)

    return output

@digest(form=form)
def get_structure_id_from_system(item, structure_indices='all'):

    from . import to_string_pdb_text
    from ..string_pdb_text import get_structure_id_from_system as aux_get

    tmp_item = to_string_pdb_text(item)
    output = aux_get(tmp_item)

    return output


## From bond

@digest(form=form)
def get_bond_order_from_bond(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_order_from_bond as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_bond_type_from_bond(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_type_from_bond as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_bonded_atoms_from_bond(item, indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bonded_atoms_from_bond as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output


#######################################################################################
######### DO NOT TOUCH THE FOLLOWING LINES, JUST INCLUDE THEM AS THEY ARE #############
#######################################################################################

from os import path
this_folder = path.dirname(path.abspath(__file__))
common_get = path.join(this_folder, '../../_private/common_get.py')
execfile(common_get, globals(), locals())
del(path, this_folder, common_get)

