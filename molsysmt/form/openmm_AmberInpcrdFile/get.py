#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.execfile import execfile
from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form='openmm.AmberInpcrdFile'

## From atom

@digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False):

    raise NotWithThisFormError()

@digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False):

    raise NotWithThisFormError()

@digest(form=form)
def get_atom_type_from_atom(item, indices='all', skip_digestion=False):

    raise NotWithThisFormError()

@digest(form=form)
def get_group_index_from_atom(item, indices='all', skip_digestion=False):

    raise NotWithThisFormError()

@digest(form=form)
def get_component_index_from_atom(item, indices='all', skip_digestion=False):

    raise NotWithThisFormError()

@digest(form=form)
def get_chain_index_from_atom(item, indices='all', skip_digestion=False):

    raise NotWithThisFormError()

@digest(form=form)
def get_molecule_index_from_atom(item, indices='all', skip_digestion=False):

    raise NotWithThisFormError()

@digest(form=form)
def get_entity_index_from_atom(item, indices='all', skip_digestion=False):

    raise NotWithThisFormError()

@digest(form=form)
def get_inner_bonded_atoms_from_atom(item, indices='all', skip_digestion=False):

    raise NotWithThisFormError()

@digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all', skip_digestion=False):

    raise NotWithThisFormError()

@digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    xyz = item.getPositions(asNumpy=True)

    if xyz is not None:

        unit = puw.get_unit(xyz)

        xyz = np.expand_dims(xyz, axis=0)

        if not is_all(structure_indices):
            xyz = xyz[structure_indices, :, :]
        if not is_all(indices):
            xyz = xyz[:, indices, :]


        xyz = puw.standardize(xyz*unit)

    return xyz

@digest(form=form)
def get_velocities_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    try:

        xyz = item.getVelocities(asNumpy=True)

    except:

        xyz = None

    if xyz is not None:

        unit = puw.get_unit(xyz)

        xyz = np.expand_dims(xyz, axis=0)

        if not is_all(structure_indices):
            xyz = xyz[structure_indices, :, :]
        if not is_all(indices):
            xyz = xyz[:, indices, :]


        xyz = puw.standardize(xyz*unit)

    return xyz

## From group

@digest(form=form)
def get_group_id_from_group(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_group_name_from_group(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_group_type_from_group(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


## From component

@digest(form=form)
def get_component_id_from_group(item, indices='all', skip_digestion=False):

    raise NotWithThisFormError()

@digest(form=form)
def get_component_name_from_group(item, indices='all', skip_digestion=False):

    raise NotWithThisFormError()

@digest(form=form)
def get_component_type_from_group(item, indices='all', skip_digestion=False):

    raise NotWithThisFormError()


## From molecule

@digest(form=form)
def get_molecule_id_from_group(item, indices='all', skip_digestion=False):

    raise NotWithThisFormError()

@digest(form=form)
def get_molecule_name_from_group(item, indices='all', skip_digestion=False):

    raise NotWithThisFormError()

@digest(form=form)
def get_molecule_type_from_group(item, indices='all', skip_digestion=False):

    raise NotWithThisFormError()


## From chain

@digest(form=form)
def get_chain_id_from_group(item, indices='all', skip_digestion=False):

    raise NotWithThisFormError()

@digest(form=form)
def get_chain_name_from_group(item, indices='all', skip_digestion=False):

    raise NotWithThisFormError()

@digest(form=form)
def get_chain_type_from_group(item, indices='all', skip_digestion=False):

    raise NotWithThisFormError()


## From entity

@digest(form=form)
def get_entity_id_from_group(item, indices='all', skip_digestion=False):

    raise NotWithThisFormError()

@digest(form=form)
def get_entity_name_from_group(item, indices='all', skip_digestion=False):

    raise NotWithThisFormError()

@digest(form=form)
def get_entity_type_from_group(item, indices='all', skip_digestion=False):

    raise NotWithThisFormError()



## From system

@digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):

    n_atoms = item.getPositions(asNumpy=True).shape[0]

    return n_atoms

@digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):

    raise NotWithThisFormError()

@digest(form=form)
def get_n_components_from_system(item, skip_digestion=False):

    raise NotWithThisFormError()

@digest(form=form)
def get_n_chains_from_system(item, skip_digestion=False):

    raise NotWithThisFormError()

@digest(form=form)
def get_n_molecules_from_system(item, skip_digestion=False):

    raise NotWithThisFormError()

@digest(form=form)
def get_n_entities_from_system(item, skip_digestion=False):

    raise NotWithThisFormError()

@digest(form=form)
def get_n_bonds_from_system(item, skip_digestion=False):

    raise NotWithThisFormError()

@digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    if is_all(structure_indices):
        return 1
    else:
        return len(structure_indices)

@digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    try:
        box = item.getBoxVectors(asNumpy=True)
        unit = puw.get_unit(box[0])
        box = np.expand_dims(box, axis=0)
        box = puw.standardize(box*unit)
    except:
        box = None

    return box

@digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):

    raise None

@digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    return None


#######################################################################################
######### DO NOT TOUCH THE FOLLOWING LINES, JUST INCLUDE THEM AS THEY ARE #############
#######################################################################################

from os import path
this_folder = path.dirname(path.abspath(__file__))
common_get = path.join(this_folder, '../../_private/common_get.py')
execfile(common_get, globals(), locals())
del(path, this_folder, common_get)

