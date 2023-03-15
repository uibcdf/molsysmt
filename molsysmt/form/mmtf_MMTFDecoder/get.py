#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################
from molsysmt._private.execfile import execfile
from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form='mmtf.MMTFDecoder'


## From atom

@digest(form=form)
def get_atom_id_from_atom(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_id_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_atom_name_from_atom(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_name_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_atom_type_from_atom(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_type_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_group_index_from_atom(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_index_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_component_index_from_atom(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_index_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_chain_index_from_atom(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_index_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_molecule_index_from_atom(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_index_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_entity_index_from_atom(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_index_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_inner_bonded_atoms_from_atom(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_inner_bonded_atoms_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_inner_bonds_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all'):

    xyz = np.column_stack([item.x_coord_list, item.y_coord_list, item.z_coord_list])
    xyz = xyz.reshape([-1, item.num_atoms, 3])
    xyz = puw.quantity(xyz, 'angstroms')
    xyz = puw.standardize(xyz)

    if not is_all(structure_indices):
        xyz = xyz[structure_indices,:,:]

    if not is_all(indices):
        xyz = xyz[:,indices,:]

    return xyz

@digest(form=form)
def get_occupancy_from_atom (item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_occupancy_from_atom as aux_get
 
    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_alternate_location_from_atom (item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_alternate_location_from_atom as aux_get
 
    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_b_factor_from_atom (item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_b_factor_from_atom as aux_get
 
    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_formal_charge_from_atom (item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_formal_charge_from_atom as aux_get
 
    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_partial_charge_from_atom (item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_partial_charge_from_atom as aux_get
 
    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output


## From group

@digest(form=form)
def get_group_id_from_group(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_id_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_group_name_from_group(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_name_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_group_type_from_group(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_group_type_from_group as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output


## From component

@digest(form=form)
def get_component_id_from_component(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_id_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_component_name_from_component(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_name_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_component_type_from_component(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_component_type_from_component as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output


## From molecule

@digest(form=form)
def get_molecule_id_from_molecule(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_id_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_molecule_name_from_molecule(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_name_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_molecule_type_from_molecule(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_molecule_type_from_molecule as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output


## From chain

@digest(form=form)
def get_chain_id_from_chain(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_id_from_chain as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_chain_name_from_chain(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_name_from_chain as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_chain_type_from_chain(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_chain_type_from_chain as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output


## From entity

@digest(form=form)
def get_entity_id_from_entity(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_id_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_entity_name_from_entity(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_name_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_entity_type_from_entity(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_entity_type_from_entity as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output


## From system

@digest(form=form)
def get_n_atoms_from_system(item):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_atoms_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item)

    return output

@digest(form=form)
def get_n_groups_from_system(item):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_groups_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item)

    return output

@digest(form=form)
def get_n_components_from_system(item):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_components_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item)

    return output

@digest(form=form)
def get_n_chains_from_system(item):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_chains_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item)

    return output

@digest(form=form)
def get_n_molecules_from_system(item):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_molecules_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item)

    return output

@digest(form=form)
def get_n_entities_from_system(item):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_entities_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item)

    return output

@digest(form=form)
def get_n_bonds_from_system(item):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_n_bonds_from_system as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item)

    return output

@digest(form=form)
def get_n_structures_from_system(item, structure_indices='all'):

    if is_all(structure_indices):
        return item.num_models
    else:
        return len(structure_indices)

@digest(form=form)
def get_box_from_system(item, structure_indices='all'):

    from molsysmt.pbc import get_box_from_lengths_and_angles

    n_structures = get_n_structures_from_system(item)

    if item.unit_cell is not None:

        cell_lengths = np.empty([n_structures,3], dtype='float64')
        cell_angles = np.empty([n_structures,3], dtype='float64')
        for ii in range(3):
            cell_lengths[:,ii] = item.unit_cell[ii]
            cell_angles[:,ii] = item.unit_cell[ii+3]

        cell_lengths = puw.quantity(cell_lengths, 'angstroms')
        cell_angles = puw.quantity(cell_angles, 'degrees')

        box = get_box_from_lengths_and_angles(cell_lengths, cell_angles)
        box = puw.standardize(box)

    else:

        box = None

    if not is_all(structure_indices):
        if box is not None:
            box = box[structure_indices,:,:]

    return box

@digest(form=form)
def get_time_from_system(item, structure_indices='all'):

    return None

@digest(form=form)
def get_structure_id_from_system(item, structure_indices='all'):

    return None


@digest(form=form)
def get_bioassemblies_from_system(item):

    output = {}

    for bio_assembly in item.bio_assembly:

        aux = {'chains': [], 'rotations': [], 'translations': []}

        for transformation in bio_assembly['transformList']:

            matrix_transformation = np.array(transformation['matrix']).reshape(-1,4)

            aux['chains'].append(transformation['chainIndexList'])
            aux['rotations'].append(matrix_transformation[:3,:3])
            aux['translations'].append(puw.quantity(matrix_transformation[:3,3], unit='angstroms', standardized=True))

        output[bio_assembly['name']] = aux

    return output

@digest(form=form)
def get_n_bioassemblies_from_system(item):

    return len(item.bio_assembly)

## From bond

@digest(form=form)
def get_bond_order_from_bond(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_order_from_bond as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_bond_type_from_bond(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_bond_type_from_bond as aux_get

    tmp_item = to_molsysmt_Topology(item)
    output = aux_get(tmp_item, indices=indices)

    return output

@digest(form=form)
def get_atom_index_from_bond(item, indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_Topology import get_atom_index_from_bond as aux_get

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

