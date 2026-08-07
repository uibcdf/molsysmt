from molsysmt._private.smonitor import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
from copy import copy
import numpy as np
import types

form='molsysmt.Structures'


## atom

@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    if (indices is None) or (structure_indices is None):
        return None

    tmp_coordinates = copy(item.coordinates)

    if not is_all(structure_indices):
        if not is_all(indices):
            tmp_coordinates = tmp_coordinates[np.ix_(structure_indices, indices)]
        else:
            tmp_coordinates = tmp_coordinates[structure_indices,:,:]
    else:
        if not is_all(indices):
            tmp_coordinates = tmp_coordinates[:,indices,:]

    return tmp_coordinates

@arg_digest(form=form)
def get_velocities_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    if (indices is None) or (structure_indices is None):
        return None

    tmp_velocities = copy(item.velocities)

    if tmp_velocities is None:
        return None

    if not is_all(structure_indices):
        if not is_all(indices):
            tmp_velocities = tmp_velocities[np.ix_(structure_indices, indices)]
        else:
            tmp_velocities = tmp_velocities[structure_indices,:,:]
    else:
        if not is_all(indices):
            tmp_velocities = tmp_velocities[:,indices,:]

    return tmp_velocities

@arg_digest(form=form)
def get_occupancy_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    if (indices is None) or (structure_indices is None):
        return None

    if getattr(item, '_occupancy', None) is None:
        return None

    tmp_occupancy = copy(item.occupancy)

    if tmp_occupancy is not None:

        if not is_all(structure_indices):
            tmp_occupancy = tmp_occupancy[structure_indices,:]

        if not is_all(indices):
            tmp_occupancy = tmp_occupancy[:,indices]

    return tmp_occupancy


@arg_digest(form=form)
def get_b_factor_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    if (indices is None) or (structure_indices is None):
        return None

    tmp_b_factor = copy(item.b_factor)

    if tmp_b_factor is not None:

        if not is_all(structure_indices):
            tmp_b_factor = tmp_b_factor[structure_indices,:]

        if not is_all(indices):
            tmp_b_factor = tmp_b_factor[:,indices]

    return tmp_b_factor

@arg_digest(form=form)
def get_alternate_location_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    if (indices is None) or (structure_indices is None):
        return None

    if item.alternate_location is None:
        return None

    if is_all(indices):
        tmp_output = copy(item.alternate_location)
    else:
        tmp_output = []
        for aux_dict in item.alternate_location:
            tmp_dict = {}
            for aux_atom_index in aux_dict:
                if aux_atom_index in indices:
                    tmp_dict[aux_atom_index] = aux_dict[aux_atom_index]
            tmp_output.append(tmp_dict)

    if not is_all(structure_indices):
        aux_tmp_output = []
        for ii in structure_indices:
            aux_tmp_output.append(tmp_output[ii])
        tmp_output = aux_tmp_output

    return tmp_output

## system

@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):

    output=item.coordinates.shape[1]

    return output

@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    if is_all(structure_indices):
        return int(item.n_structures)
    else:
        return len(structure_indices)


@arg_digest(form=form)
def get_structure_index_from_system(item, structure_indices='all', skip_digestion=False):

    if structure_indices is None:
        return None
    if is_all(structure_indices):
        return list(range(item.n_structures))
    return list(structure_indices)


@arg_digest(form=form)
def get_coordinates_from_system(item, structure_indices='all', skip_digestion=False):

    if structure_indices is None:
        return None

    if is_all(structure_indices):
        output=copy(item.coordinates)
    else:
        output=item.coordinates[structure_indices,:,:]
    return output

@arg_digest(form=form)
def get_velocities_from_system(item, structure_indices='all', skip_digestion=False):

    if structure_indices is None:
        return None

    if item.velocities is None:
        return None

    if is_all(structure_indices):
        output=copy(item.velocities)
    else:
        output=item.velocities[structure_indices,:,:]
    return output

@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    if structure_indices is None:
        return None

    output=None
    if item.box is not None:
        if is_all(structure_indices):
            output=copy(item.box)
        else:
            output=item.box[structure_indices,:,:]
    return output

@arg_digest(form=form)
def get_box_shape_from_system(item, structure_indices='all', skip_digestion=False):

    if structure_indices is None:
        return None

    from molsysmt.pbc import get_shape_from_box
    output = None
    box = get_box_from_system(item, structure_indices=structure_indices, skip_digestion=True)
    if box is not None:
        output = get_shape_from_box(box, skip_digestion=False)
    return output

@arg_digest(form=form)
def get_box_lengths_from_system(item, structure_indices='all', skip_digestion=False):

    from molsysmt.pbc import get_lengths_and_angles_from_box

    if structure_indices is None:
        return None

    if item.box is not None:
        tmp_box_lengths, _ = get_lengths_and_angles_from_box(item.box, skip_digestion=True)
    else:
        tmp_box_lengths = None

    if is_all(structure_indices):
        output = tmp_box_lengths
    else:
        output = tmp_box_lengths[structure_indices,:]
    return output

@arg_digest(form=form)
def get_box_angles_from_system(item, structure_indices='all', skip_digestion=False):

    from molsysmt.pbc import get_lengths_and_angles_from_box

    if structure_indices is None:
        return None

    if item.box is not None:
        _, tmp_box_angles = get_lengths_and_angles_from_box(item.box, skip_digestion=True)
    else:
        tmp_box_angles = None

    if is_all(structure_indices):
        output = tmp_box_angles
    else:
        output = tmp_box_angles[structure_indices,:]
    return output

@arg_digest(form=form)
def get_box_volume_from_system(item, structure_indices='all', skip_digestion=False):

    if structure_indices is None:
        return None

    from molsysmt.pbc import get_volume_from_box
    output = None
    box = get_box_from_system(item, structure_indices=structure_indices, skip_digestion=True)
    if box is not None:
        output = get_volume_from_box(box)
    return output

@arg_digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):

    if structure_indices is None:
        return None

    if item.time is None:
        return None

    if is_all(structure_indices):
        output = copy(item.time)
    else:
        output = item.time[structure_indices]
    return output


def _get_structure_series(value, structure_indices):
    if structure_indices is None or value is None:
        return None
    if is_all(structure_indices):
        return copy(value)
    return value[structure_indices]


@arg_digest(form=form)
def get_temperature_from_system(item, structure_indices='all', skip_digestion=False):
    return _get_structure_series(item.temperature, structure_indices)


@arg_digest(form=form)
def get_potential_energy_from_system(item, structure_indices='all', skip_digestion=False):
    return _get_structure_series(item.potential_energy, structure_indices)


@arg_digest(form=form)
def get_kinetic_energy_from_system(item, structure_indices='all', skip_digestion=False):
    return _get_structure_series(item.kinetic_energy, structure_indices)


@arg_digest(form=form)
def get_total_energy_from_system(item, structure_indices='all', skip_digestion=False):
    potential_energy = get_potential_energy_from_system(
        item,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    kinetic_energy = get_kinetic_energy_from_system(
        item,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    if potential_energy is None or kinetic_energy is None:
        return None
    return potential_energy + kinetic_energy

@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    if structure_indices is None:
        return None

    if item.structure_id is None:
        return None

    if is_all(structure_indices):
        output = copy(item.structure_id)
    else:
        output = item.structure_id[structure_indices]
    return output

@arg_digest(form=form)
def get_occupancy_from_system(item, structure_indices='all', skip_digestion=False):

    return get_occupancy_from_atom(item, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_b_factor_from_system(item, structure_indices='all', skip_digestion=False):

    return get_b_factor_from_atom(item, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_alternate_location_from_system(item, structure_indices='all', skip_digestion=False):

    return get_alternate_location_from_atom(item, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_bioassembly_from_system(item, skip_digestion=False):

    tmp_output = copy(item.bioassembly)

    return tmp_output

@arg_digest(form=form)
def get_n_bioassemblies_from_system(item, skip_digestion=False):

    if item.bioassembly is None:
        return 0
    return len(item.bioassembly)

# List of functions to be imported

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
