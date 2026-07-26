#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.execfile import execfile
from molsysmt._private.smonitor import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form='molsysmt.H5MSMFileHandler'


def _read_structure_rows(dataset, structure_indices):
    """Reading structure rows while preserving order and repeated indices."""

    if is_all(structure_indices):
        return dataset[:]
    return np.asarray([dataset[int(index)] for index in structure_indices])


def _h5py_atom_indices(indices):
    """Returning sorted unique indices and an inverse map for h5py reads."""

    requested = np.asarray(indices, dtype=np.int64)
    unique, inverse = np.unique(requested, return_inverse=True)
    return unique, inverse


## From atom


@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    if not is_all(indices):
        read_indices, restore_order = _h5py_atom_indices(indices)

    if is_all(structure_indices):
        if is_all(indices):
            output = item.file['structures']['coordinates'][:,:,:].astype('float')
        else:
            output = item.file['structures']['coordinates'][:,read_indices,:].astype('float')
            output = output[:,restore_order,:]
    else:
        output = []
        for ii in structure_indices:
            if is_all(indices):
                output.append(item.file['structures']['coordinates'][ii,:,:].astype('float'))
            else:
                frame = item.file['structures']['coordinates'][ii,read_indices,:].astype('float')
                output.append(frame[restore_order,:])
        output = np.array(output)

    output = puw.quantity(output, item.file.attrs['length_unit'], standardized=True)

    return output

@arg_digest(form=form)
def get_velocities_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    if item.file['structures']['velocities'].shape[0] == 0:
        return None

    if not is_all(indices):
        read_indices, restore_order = _h5py_atom_indices(indices)

    if is_all(structure_indices):
        if is_all(indices):
            output = item.file['structures']['velocities'][:,:,:].astype('float')
        else:
            output = item.file['structures']['velocities'][:,read_indices,:].astype('float')
            output = output[:,restore_order,:]
    else:
        output = []
        for ii in structure_indices:
            if is_all(indices):
                output.append(item.file['structures']['velocities'][ii,:,:].astype('float'))
            else:
                frame = item.file['structures']['velocities'][ii,read_indices,:].astype('float')
                output.append(frame[restore_order,:])
        output = np.array(output)

    output = puw.quantity(output, item.file.attrs['length_unit']+'/'+item.file.attrs['time_unit'], standardized=True)

    return output

@arg_digest(form=form)
def get_b_factor_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    if 'b_factor' not in item.file['structures']:
        return None

    if item.file['structures']['b_factor'].shape[0] == 0:
        return None

    if not is_all(indices):
        read_indices, restore_order = _h5py_atom_indices(indices)

    if is_all(structure_indices):
        if is_all(indices):
            output = item.file['structures']['b_factor'][:, :].astype('float')
        else:
            output = item.file['structures']['b_factor'][:, read_indices].astype('float')
            output = output[:, restore_order]
    else:
        output = []
        for ii in structure_indices:
            if is_all(indices):
                output.append(item.file['structures']['b_factor'][ii, :].astype('float'))
            else:
                frame = item.file['structures']['b_factor'][ii, read_indices].astype('float')
                output.append(frame[restore_order])
        output = np.array(output)

    unit = item.file['structures'].attrs.get('b_factor_unit', 'nanometer**2')
    output = puw.quantity(output, unit, standardized=True)

    return output


## From system


@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    output = item.file['structures'].attrs['n_structures_written']

    return output

@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    if item.file['structures'].attrs['constant_box']:
        if is_all(structure_indices):
            n_structures = item.file['structures'].attrs['n_structures_written']
            output = item.file['structures']['box'][0,:,:]
            output = np.repeat(output[np.newaxis,:,:], n_structures, axis=0)
        else:
            n_structures = len(structure_indices)
            output = item.file['structures']['box'][0,:,:]
            output = np.repeat(output[np.newaxis,:,:], n_structures, axis=0)
    else:
        if is_all(structure_indices):
            output = item.file['structures']['box'][:,:,:]
        else:
            output = item.file['structures']['box'][structure_indices,:,:]

    output = puw.quantity(output, item.file.attrs['length_unit'], standardized=True)

    return output

@arg_digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):

    if item.file['structures']['time'].shape[0] == 0:
        return None

    if item.file['structures'].attrs['constant_time_step']:
        init_time = item.file['structures']['time'][0]
        time_step = item.file['structures'].attrs['time_step']
        if is_all(structure_indices):
            n_structures = item.file['structures'].attrs['n_structures_written']
            output = init_time + time_step*np.arange(n_structures)
        else:
            output = init_time + time_step*np.asarray(structure_indices)
    else:
        output = _read_structure_rows(
            item.file['structures']['time'], structure_indices
        )

    output = puw.quantity(output, item.file.attrs['time_unit'], standardized=True)

    return output

@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    if item.file['structures']['id'].shape[0] == 0:
        return None

    if item.file['structures'].attrs['constant_id_step']:
        init_id = item.file['structures']['id'][0]
        id_step = item.file['structures'].attrs['id_step']
        if is_all(structure_indices):
            n_structures = item.file['structures'].attrs['n_structures_written']
            output = init_id + id_step*np.arange(n_structures)
        else:
            output = init_id + id_step*np.asarray(structure_indices)
    else:
        output = _read_structure_rows(
            item.file['structures']['id'], structure_indices
        )

    return output


@arg_digest(form=form)
def get_structure_chemical_state_index_from_system(
    item, structure_indices='all', skip_digestion=False
):
    """Getting nullable chemical-state indices aligned to stored structures."""

    structures = item.file['structures']
    n_structures = int(structures.attrs.get('n_structures_written', 0))
    if is_all(structure_indices):
        indices = range(n_structures)
    else:
        indices = structure_indices

    if 'chemical_state_index' in structures and structures['chemical_state_index'].size:
        dataset = structures['chemical_state_index']
        return [
            None if int(dataset[int(index)]) < 0 else int(dataset[int(index)])
            for index in indices
        ]

    from .get_topological_attributes import get_n_chemical_states_from_system

    n_states = get_n_chemical_states_from_system(item, skip_digestion=True)
    implicit = 0 if n_states == 1 else None
    return [implicit for _ in indices]

@arg_digest(form=form)
def get_kinetic_energy_from_system(item, structure_indices='all', skip_digestion=False):

    if item.file['structures']['kinetic_energy'].shape[0] == 0:
        return None

    output = _read_structure_rows(
        item.file['structures']['kinetic_energy'], structure_indices
    )

    output = puw.quantity(output, item.file.attrs['energy_unit'], standardized=True)

    return output

@arg_digest(form=form)
def get_potential_energy_from_system(item, structure_indices='all', skip_digestion=False):

    if item.file['structures']['potential_energy'].shape[0] == 0:
        return None

    output = _read_structure_rows(
        item.file['structures']['potential_energy'], structure_indices
    )

    output = puw.quantity(output, item.file.attrs['energy_unit'], standardized=True)

    return output

@arg_digest(form=form)
def get_temperature_from_system(item, structure_indices='all', skip_digestion=False):

    if (
        not item.file['structures'].attrs['temperature_from_kinetic_energy']
        and item.file['structures']['temperature'].shape[0] == 0
    ):
        return None

    constant_R = puw.constants.get_constant('R')

    if item.file['structures'].attrs['temperature_from_kinetic_energy']:

        kinetic_energy = get_kinetic_energy_from_system(item, structure_indices=structure_indices, skip_digestion=False)
        kinetic_energy = puw.convert(kinetic_energy, to_form='openmm.unit')
        output = 2 * kinetic_energy / (item.file['structures'].attrs['n_degrees_of_freedom'] * constant_R)
        output = puw.standardize(output)

    else:

        output = _read_structure_rows(
            item.file['structures']['temperature'], structure_indices
        )

        output = puw.quantity(output, item.file.attrs['temperature_unit'], standardized=True)

    return output


@arg_digest(form=form)
def get_total_energy_from_system(item, structure_indices='all', skip_digestion=False):

    potential_energy = get_potential_energy_from_system(
        item, structure_indices=structure_indices, skip_digestion=True
    )
    kinetic_energy = get_kinetic_energy_from_system(
        item, structure_indices=structure_indices, skip_digestion=True
    )
    if potential_energy is None or kinetic_energy is None:
        return None
    return potential_energy + kinetic_energy

@arg_digest(form=form)
def get_b_factor_from_system(item, structure_indices='all', skip_digestion=False):

    return get_b_factor_from_atom(item, structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_coordinates_from_system(item, structure_indices='all', skip_digestion=False):

    return get_coordinates_from_atom(item, indices='all', structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_velocities_from_system(item, structure_indices='all', skip_digestion=False):

    return get_velocities_from_atom(item, indices='all', structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_occupancy_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    if 'occupancy' not in item.file['structures']:
        return None

    if item.file['structures']['occupancy'].shape[0] == 0:
        return None

    if is_all(structure_indices):
        if is_all(indices):
            output = item.file['structures']['occupancy'][:, :].astype('float')
        else:
            output = item.file['structures']['occupancy'][:, indices].astype('float')
    else:
        output = []
        for ii in structure_indices:
            if is_all(indices):
                output.append(item.file['structures']['occupancy'][ii, :].astype('float'))
            else:
                output.append(item.file['structures']['occupancy'][ii, indices].astype('float'))
        output = np.array(output)

    return output

@arg_digest(form=form)
def get_occupancy_from_system(item, structure_indices='all', skip_digestion=False):

    return get_occupancy_from_atom(item, indices='all', structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_alternate_location_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    if 'alternate_location' not in item.file['structures']:
        return None

    if item.file['structures']['alternate_location'].shape[0] == 0:
        return None

    if is_all(structure_indices):
        if is_all(indices):
            output = item.file['structures']['alternate_location'][:, :].astype('str').tolist()
        else:
            output = item.file['structures']['alternate_location'][:, indices].astype('str').tolist()
    else:
        output = []
        for ii in structure_indices:
            if is_all(indices):
                output.append(item.file['structures']['alternate_location'][ii, :].astype('str').tolist())
            else:
                output.append(item.file['structures']['alternate_location'][ii, indices].astype('str').tolist())

    return output

@arg_digest(form=form)
def get_alternate_location_from_system(item, structure_indices='all', skip_digestion=False):

    return get_alternate_location_from_atom(item, indices='all', structure_indices=structure_indices, skip_digestion=True)

@arg_digest(form=form)
def get_bioassembly_from_system(item, skip_digestion=False):

    if 'bioassembly' not in item.file:
        return None

    import json
    return json.loads(item.file['bioassembly'][()])

@arg_digest(form=form)
def get_n_bioassemblies_from_system(item, skip_digestion=False):

    bioassembly = get_bioassembly_from_system(item, skip_digestion=True)
    if bioassembly is None:
        return 0
    return len(bioassembly)

@arg_digest(form=form)
def get_box_shape_from_system(item, structure_indices='all', skip_digestion=False):

    from molsysmt.pbc import get_shape_from_box
    box = get_box_from_system(item, structure_indices=structure_indices, skip_digestion=True)
    if box is None:
        return None
    return get_shape_from_box(box, skip_digestion=False)

@arg_digest(form=form)
def get_box_lengths_from_system(item, structure_indices='all', skip_digestion=False):

    from molsysmt.pbc import get_lengths_and_angles_from_box
    box = get_box_from_system(item, structure_indices=structure_indices, skip_digestion=True)
    if box is None:
        return None
    lengths, _ = get_lengths_and_angles_from_box(box, skip_digestion=True)
    return lengths

@arg_digest(form=form)
def get_box_angles_from_system(item, structure_indices='all', skip_digestion=False):

    from molsysmt.pbc import get_lengths_and_angles_from_box
    box = get_box_from_system(item, structure_indices=structure_indices, skip_digestion=True)
    if box is None:
        return None
    _, angles = get_lengths_and_angles_from_box(box, skip_digestion=True)
    return angles

@arg_digest(form=form)
def get_box_volume_from_system(item, structure_indices='all', skip_digestion=False):

    from molsysmt.pbc import get_volume_from_box
    box = get_box_from_system(item, structure_indices=structure_indices, skip_digestion=True)
    if box is None:
        return None
    return get_volume_from_box(box)
