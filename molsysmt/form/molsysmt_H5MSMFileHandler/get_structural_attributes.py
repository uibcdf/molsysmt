#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.execfile import execfile
from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form='molsysmt.H5MSMFileHandler'


## From atom


@digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    if is_all(structure_indices):
        if is_all(indices):
            output = item.file['structures']['coordinates'][:,:,:].astype('float')
        else:
            output = item.file['structures']['coordinates'][:,indices,:].astype('float')
    else:
        output = []
        for ii in structure_indices:
            output.append(item.file['structures']['coordinates'][ii,indices,:].astype('float'))
        output = np.array(output)

    output = puw.quantity(output, item.file.attrs['length_unit'], standardized=True)

    return output

@digest(form=form)
def get_velocities_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    if is_all(structure_indices):
        if is_all(indices):
            output = item.file['structures']['velocities'][:,:,:].astype('float')
        else:
            output = item.file['structures']['velocities'][:,indices,:].astype('float')
    else:
        output = []
        for ii in structure_indices:
            output.append(item.file['structures']['velocities'][ii,indices,:].astype('float'))
        output = np.array(output)

    output = puw.quantity(output, item.file.attrs['length_unit']+'/'+item.file.attrs['time_unit'], standardized=True)

    return output


## From system


@digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    output = item.file['structures'].attrs['n_structures_written']

    return output

@digest(form=form)
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

@digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):

    if item.file['structures'].attrs['constant_time_step']:
        init_time = item.file['structures']['time'][0]
        time_step = item.file['structures'].attrs['time_step']
        if is_all(structure_indices):
            n_structures = item.file['structures'].attrs['n_structures_written']
            output = init_time + time_step*np_arange(n_structures)
        else:
            output = init_time + time_step*structure_indices
    else:
        if is_all(structure_indices):
            output = item.file['structures']['time'][:]
        else:
            output = item.file['structures']['time'][structure_indices]

    output = puw.quantity(output, item.file.attrs['time_unit'], standardized=True)

    return output

@digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    if item.file['structures'].attrs['constant_id_step']:
        init_id = item.file['structures']['id'][0]
        id_step = item.file['structures'].attrs['id_step']
        if is_all(structure_indices):
            n_structures = item.file['structures'].attrs['n_structures_written']
            output = init_id + id_step*np_arange(n_structures)
        else:
            output = init_id + id_step*structure_indices
    else:
        if is_all(structure_indices):
            output = item.file['structures']['id'][:]
        else:
            output = item.file['structures']['id'][structure_indices]

    return output

@digest(form=form)
def get_kinetic_energy_from_system(item, structure_indices='all', skip_digestion=False):

    if is_all(structure_indices):
        output = item.file['structures']['kinetic_energy'][:]
    else:
        output = item.file['structures']['kinetic_energy'][structure_indices]

    output = puw.quantity(output, item.file.attrs['energy_unit'], standardized=True)

    return output

@digest(form=form)
def get_potential_energy_from_system(item, structure_indices='all', skip_digestion=False):

    if is_all(structure_indices):
        output = item.file['structures']['potential_energy'][:]
    else:
        output = item.file['structures']['potential_energy'][structure_indices]

    output = puw.quantity(output, item.file.attrs['energy_unit'], standardized=True)

    return output

@digest(form=form)
def get_temperature_from_system(item, structure_indices='all', skip_digestion=False):

    constant_R = puw.get_constant('R')

    if item.file['structures'].attrs['temperature_from_kinetic_energy']:

        kinetic_energy = get_kinetic_energy_from_system(item, structure_indices=structure_indices, skip_digestion=False)
        kinetic_energy = puw.convert(kinetic_energy, to_form='openmm.unit')
        output = 2 * kinetic_energy / (item.file['structures'].attrs['n_degrees_of_freedom'] * constant_R)
        output = puw.standardize(output)

    else:

        if is_all(structure_indices):
            output = item.file['structures']['temperature'][:]
        else:
            output = item.file['structures']['temperature'][structure_indices]

        output = puw.quantity(output, item.file.attrs['temperature_unit'], standardized=True)

    return output



