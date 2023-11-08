from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

@digest(form='molsysmt.MSMH5FileHandler')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all'):

    from molsysmt.native import Structures

    constant_R = puw.get_constant('R')

    structures_ds = item.file['structures']

    length_unit = puw.unit(item.file.attrs['length_unit'])
    time_unit = puw.unit(item.file.attrs['time_unit'])
    energy_unit = puw.unit(item.file.attrs['energy_unit'])
    temperature_unit = puw.unit(item.file.attrs['temperature_unit'])

    tmp_item = Structures()

    if is_all(structure_indices):

        n_structures = structures_ds.attrs['n_structures_written']
        tmp_item.n_structures = n_structures

        if is_all(atom_indices):
            n_atoms = structures_ds.attrs['n_atoms']
            tmp_item.n_atoms = n_atoms
        else:
            n_atoms = len(atom_indices)
            tmp_item.n_atoms = n_atoms

        if structures_ds['id'].shape[0]==0:
            tmp_item.structure_id = None
        else:
            if structures_ds.attrs['constant_id_step']:
                tmp_item.structure_id = structures_ds['id'][0].astype('int64')+\
                structures_ds.attrs['id_step']*np.arange(n_structures, dtype='int64')
            else:
                tmp_item.structure_id = structures_ds['id'][:].astype('int64')

        if structures_ds['time'].shape[0]==0:
            tmp_item.time = None
        else:
            if structures_ds.attrs['constant_time_step']:
                tmp_item.time = structures_ds['time'][0].astype('float64')+\
                structures_ds.attrs['time_step']*np.arange(n_structures, dtype='float64')
            else:
                tmp_item.time = structures_ds['time'][:].astype('float64')
            tmp_item.time = puw.quantity(tmp_item.time, time_unit, standardized=True)

        if structures_ds['coordinates'].shape[0]==0:
            tmp_item.coordinates = None
        else:
            if is_all(atom_indices):
                tmp_item.coordinates = structures_ds['coordinates'][:,:,:].astype('float64')
            else:
                tmp_item.coordinates = structures_ds['coordinates'][:,atom_indices,:].astype('float64')
            tmp_item.coordinates = puw.quantity(tmp_item.coordinates, length_unit, standardized=True)

        if structures_ds['velocities'].shape[0]==0:
            tmp_item.velocities = None
        else:
            if is_all(atom_indices):
                tmp_item.velocities = structures_ds['velocities'][:,:,:].astype('float64')
            else:
                tmp_item.velocities = structures_ds['velocities'][:,atom_indices,:].astype('float64')
            tmp_item.velocities = puw.quantity(tmp_item.velocities, length_unit/time_unit, standardized=True)

        if structures_ds['box'].shape[0]==0:
            tmp_item.box = None
        else:
            if structures_ds.attrs['constant_box']:
                aux = structures_ds['box'][0,:,:].astype('float64')
                tmp_item.box = np.repeat(aux[np.newaxis,:,:], n_structures, axis=0)
                del(aux)
            else:
                tmp_item.box = structures_ds['box'][:,:,:].astype('float64')
            tmp_item.box = puw.quantity(tmp_item.box, length_unit, standardized=True)

        if structures_ds['kinetic_energy'].shape[0]==0:
            tmp_item.kinetic_energy = None
        else:
            tmp_item.kinetic_energy = structures_ds['kinetic_energy'][:].astype('float64')
            tmp_item.kinetic_energy = puw.quantity(tmp_item.kinetic_energy, energy_unit, standardized=True)

        if structures_ds['potential_energy'].shape[0]==0:
            tmp_item.potential_energy = None
        else:
            tmp_item.potential_energy = structures_ds['potential_energy'][:].astype('float64')
            tmp_item.potential_energy = puw.quantity(tmp_item.potential_energy, energy_unit, standardized=True)


        if structures_ds.attrs['temperature_from_kinetic_energy']:

            if tmp_item.kinetic_energy is not None:
                tmp_item.temperature = 2 * tmp_item.kinetic_energy / (structures_ds.attrs['n_degrees_of_freedom'] * constant_R)
            else:
                tmp_item.temperature = None

        else:

            if structures_ds['temperature'].shape[0]==0:
                tmp_item.temperature = None
            else:
                tmp_item.temperature = structures_ds['temperature'].astype('float64')
                tmp_item.temperature = puw.quantity(tmp_item.temperature[:], temperature_unit, standardized=True)

    else:

        n_structures = len(structure_indices)
        tmp_item.n_structures = n_structures

        if is_all(atom_indices):
            n_atoms = structures_ds.attrs['n_atoms']
            tmp_item.n_atoms = n_atoms
        else:
            n_atoms = len(atom_indices)
            tmp_item.n_atoms = n_atoms

        if structures_ds['id'].shape[0]==0:
            tmp_item.structure_id = None
        else:
            if structures_ds.attrs['constant_id_step']:
                tmp_item.structure_id = structures_ds['id'][0].astype('int64')+\
                structures_ds.attrs['id_step']*structure_indices
            else:
                tmp_item.structure_id = structures_ds['id'][structure_indices].astype('int64')

        if structures_ds['time'].shape[0]==0:
            tmp_item.time = None
        else:
            if structures_ds.attrs['constant_time_step']:
                tmp_item.time = structures_ds['time'][0].astype('float64')+\
                structures_ds.attrs['time_step']*structure_indices
            else:
                tmp_item.time = structures_ds['time'][structure_indices].astype('float64')
            tmp_item.time = puw.quantity(tmp_item.time, time_unit, standardized=True)

        if structures_ds['coordinates'].shape[0]==0:
            tmp_item.coordinates = None
        else:
            if is_all(atom_indices):
                tmp_item.coordinates = structures_ds['coordinates'][structure_indices,:,:].astype('float64')
            else:
                aux = []
                for ii in structure_indices:
                    aux.append(structures_ds['coordinates'][ii,atom_indices,:].astype('float64'))
                tmp_item.coordinates = np.concatenate(aux)
                del(aux)
            tmp_item.coordinates = puw.quantity(tmp_item.coordinates, length_unit, standardized=True)

        if structures_ds['velocities'].shape[0]==0:
            tmp_item.velocities = None
        else:
            if is_all(atom_indices):
                tmp_item.velocities = structures_ds['velocities'][structure_indices,:,:].astype('float64')
            else:
                aux = []
                for ii in structure_indices:
                    aux.append(structures_ds['velocities'][ii,atom_indices,:].astype('float64'))
                tmp_item.velocities = np.concatenate(aux)
                del(aux)
            tmp_item.velocities = puw.quantity(tmp_item.velocities, length_unit/time_unit, standardized=True)

        if structures_ds['box'].shape[0]==0:
            tmp_item.box = None
        else:
            if structures_ds.attrs['constant_box']:
                aux = structures_ds['box'][0,:,:].astype('float64')
                tmp_item.box = np.repeat(aux[np.newaxis,:,:], n_structures, axis=0)
                del(aux)
            else:
                tmp_item.box = structures_ds['box'][structure_indices,:,:].astype('float64')
            tmp_item.box = puw.quantity(tmp_item.box, length_unit, standardized=True)

        if structures_ds['kinetic_energy'].shape[0]==0:
            tmp_item.kinetic_energy = None
        else:
            tmp_item.kinetic_energy = structures_ds['kinetic_energy'][structure_indices].astype('float64')
            tmp_item.kinetic_energy = puw.quantity(tmp_item.kinetic_energy, energy_unit, standardized=True)

        if structures_ds['potential_energy'].shape[0]==0:
            tmp_item.potential_energy = None
        else:
            tmp_item.potential_energy = structures_ds['potential_energy'][structure_indices].astype('float64')
            tmp_item.potential_energy = puw.quantity(tmp_item.potential_energy, energy_unit, standardized=True)


        if structures_ds.attrs['temperature_from_kinetic_energy']:

            if tmp_item.kinetic_energy is not None:
                tmp_item.temperature = 2 * tmp_item.kinetic_energy / (structures_ds.attrs['n_degrees_of_freedom'] * constant_R)
            else:
                tmp_item.temperature = None

        else:

            if structures_ds['temperature'].shape[0]==0:
                tmp_item.temperature = None
            else:
                tmp_item.temperature = structures_ds['temperature'][structure_indices].astype('float64')
                tmp_item.temperature = puw.quantity(tmp_item.temperature, temperature_unit, standardized=True)

    return tmp_item

