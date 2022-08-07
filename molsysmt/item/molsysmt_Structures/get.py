from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import puw

form='molsysmt.Structures'


## atom

@digest(form=form)
def get_atom_id_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_atom_name_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_atom_type_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_group_index_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_component_index_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_chain_index_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_molecule_index_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_entity_index_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_inner_bonded_atoms_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all'):

    tmp_coordinates = item.coordinates

    if not is_all(structure_indices):
        tmp_coordinates = tmp_coordinates[structure_indices,:,:]

    if not is_all(indices):
        tmp_coordinates = tmp_coordinates[:,indices,:]

    return tmp_coordinates


## From group

@digest(form=form)
def get_group_id_from_group(item, indices='all'):

    raise NotImplementedMethodError()

@digest(form=form)
def get_group_name_from_group(item, indices='all'):

    raise NotImplementedMethodError()

@digest(form=form)
def get_group_type_from_group(item, indices='all'):

    raise NotImplementedMethodError()


## From component

@digest(form=form)
def get_component_id_from_group(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_component_name_from_group(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_component_type_from_group(item, indices='all'):

    raise NotWithThisFormError()


## From molecule

@digest(form=form)
def get_molecule_id_from_group(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_molecule_name_from_group(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_molecule_type_from_group(item, indices='all'):

    raise NotWithThisFormError()


## From chain

@digest(form=form)
def get_chain_id_from_group(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_chain_name_from_group(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_chain_type_from_group(item, indices='all'):

    raise NotWithThisFormError()


## From entity

@digest(form=form)
def get_entity_id_from_group(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_entity_name_from_group(item, indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_entity_type_from_group(item, indices='all'):

    raise NotWithThisFormError()


## system

@digest(form=form)
def get_n_atoms_from_system(item):

    output=item.coordinates.shape[1]

    return output

@digest(form=form)
def get_n_groups_from_system(item):

    raise NotWithThisFormError()

@digest(form=form)
def get_n_components_from_system(item):

    raise NotWithThisFormError()

@digest(form=form)
def get_n_chains_from_system(item):

    raise NotWithThisFormError()

@digest(form=form)
def get_n_molecules_from_system(item):

    raise NotWithThisFormError()

@digest(form=form)
def get_n_entities_from_system(item):

    raise NotWithThisFormError()

@digest(form=form)
def get_n_bonds_from_system(item):

    raise NotWithThisFormError()

@digest(form=form)
def get_n_structures_from_system(item):

    output=item.coordinates.shape[0]

    return output

@digest(form=form)
def get_coordinates_from_system(item, structure_indices='all'):

    if is_all(structure_indices):
        output=item.coordinates
    else:
        output=item.coordinates[structure_indices,:,:]
    return output

@digest(form=form)
def get_box_from_system(item, structure_indices='all'):

    output=None
    if item.box is not None:
        if is_all(structure_indices):
            output=item.box
        else:
            output=item.box[structure_indices,:,:]
    return output

@digest(form=form)
def get_box_shape_from_system(item, structure_indices='all'):

    from molsysmt.pbc import box_shape_from_box
    output = None
    box = get_box_from_system(item, structure_indices=structure_indices)
    if box is not None:
        output = box_shape_from_box(box)
    return output

@digest(form=form)
def get_box_lengths_from_system(item, structure_indices='all'):

    tmp_box_lengths = item.get_box_lengths()
    if is_all(structure_indices):
        output = tmp_box_lengths
    else:
        output = tmp_box_lengths[structure_indices,:]
    return output

@digest(form=form)
def get_box_angles_from_system(item, structure_indices='all'):

    tmp_box_angles = item.get_box_angles()
    if is_all(structure_indices):
        output = tmp_box_angles
    else:
        output = tmp_box_angles[structure_indices,:]
    return output

@digest(form=form)
def get_box_volume_from_system(item, structure_indices='all'):

    from molsysmt.pbc import box_volume_from_box
    output = None
    box = get_box_from_system(item, structure_indices=structure_indices)
    if box is not None:
        output = box_volume_from_box(box)
    return output

@digest(form=form)
def get_time_from_system(item, structure_indices='all'):

    if is_all(structure_indices):
        output = item.time
    else:
        output = item.time[structure_indices]
    return output

@digest(form=form)
def get_step_from_system(item, structure_indices='all'):

    if is_all(structure_indices):
        output = item.step
    else:
        output = item.step[structure_indices]
    return output

