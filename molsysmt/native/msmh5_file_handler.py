import h5py
import numpy as np
from molsysmt import pyunitwizard as puw

msmh5_version = "0.2"

class MSMH5FileHandler():

    def __init__(self, filename, io_mode='r', creator='MolSysMT', compression="gzip", compression_opts=4,
            int_precision='single', float_precision='single', length_unit=None, time_unit=None, energy_unit=None,
            temperature_unit=None, charge_unit=None, mass_unit=None, closed=False):

        self.file = None

        if io_mode=='w':

            self.file = _new_msmfile(filename, creator=creator, compression=compression,
                    compression_opts=compression_opts, int_precision=int_precision,
                    float_precision=float_precision, length_unit=length_unit, time_unit=time_unit,
                    energy_unit=energy_unit, temperature_unit=temperature_unit,
                    charge_unit=charge_unit, mass_unit=mass_unit)

        elif io_mode=='r':

            self.file = h5py.File(filename, "r")

        else:

            raise NotImplementedError

        if closed:
            self.file.close()

    def write_topology(self, topology, selection='all', syntax='MolSysMT'):

        from molsysmt.basic import get_form, select, convert
        from molsysmt._private.variables import is_all
        from molsysmt.form import _dict_modules

        if is_all(selection):
            atom_indices = 'all'
        else:
            atom_indices = select(topology, selection=selection, syntax=syntax)

        try:
            topology_form = get_form(topology)
            _dict_modules[topology_form].write_topology_in_msmh5(topology, file=self.file,
                    atom_indices=atom_indices)
        except:
            aux_topology = convert(topology, to_form='molsysmt.Topology', selection=atom_indices)
            _dict_modules['molsysmt.Topology'].write_topology_in_msmh5(aux_topology, file=self.file,
                    atom_indices=atom_indices)
            del(aux_topology)

    def close(self):

        self.file.close()

def _new_msmfile(filename, creator='MolSysMT', compression="gzip", compression_opts=4,
        int_precision='single', float_precision='single', length_unit=None,
        time_unit=None, energy_unit=None, temperature_unit=None, charge_unit=None,
        mass_unit=None):

    if int_precision=='single':
        int_type=np.int32
    elif int_precision=='double':
        int_type=np.int64

    if float_precision=='single':
        float_type=np.float32
    elif float_precision=='double':
        float_type=np.float64

    file = h5py.File(filename, "w")

    file.attrs['version'] = msmh5_version
    file.attrs['type'] = "msmh5"
    file.attrs['creator'] = creator
    file.attrs['int_precision'] = int_precision
    file.attrs['float_precision'] = float_precision

    if length_unit is None:
        file.attrs['length_unit']=puw.get_standard_units(dimensionality={'[L]':1}, form='string')
    else:
        file.attrs['length_unit']=puw.get_unit(length_unit, to_form='string')

    if time_unit is None:
        file.attrs['time_unit']=puw.get_standard_units(dimensionality={'[T]':1}, form='string')
    else:
        file.attrs['time_unit']=puw.get_unit(time_unit, to_form='string')

    if energy_unit is None:
        file.attrs['energy_unit']=puw.get_standard_units(dimensionality={'[L]':2, '[M]':1,
            '[T]':-2, '[mol]':-1}, form='string')
    else:
        file.attrs['energy_unit']=puw.get_unit(energy_unit, to_form='string')

    if temperature_unit is None:
        file.attrs['temperature_unit']=puw.get_standard_units(dimensionality={'[K]':1}, form='string')
    else:
        file.attrs['temperature_unit']=puw.get_unit(temperature_unit, to_form='string')

    if charge_unit is None:
        file.attrs['charge_unit']=puw.get_standard_units(dimensionality={'[A]':1, '[T]':1}, form='string')
    else:
        file.attrs['charge_unit']=puw.get_unit(charge_unit, to_form='string')

    if mass_unit is None:
        file.attrs['mass_unit']=puw.get_standard_units(dimensionality={'[M]':1}, form='string')
    else:
        file.attrs['mass_unit']=puw.get_unit(mass_unit, to_form='string')

    global_dataset_options = {
            'compression':compression,
            'compression_opts':compression_opts,
            }

    # Topology

    topology = file.create_group("topology")
    topology.attrs['n_atoms']=0
    topology.attrs['n_groups']=0
    topology.attrs['n_components']=0
    topology.attrs['n_molecules']=0
    topology.attrs['n_entities']=0
    topology.attrs['n_chains']=0
    topology.attrs['n_bonds']=0

    ## Atoms

    atoms = topology.create_group("atoms")

    atoms.create_dataset('id', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)
    atoms.create_dataset('name', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)
    atoms.create_dataset('type', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)
    atoms.create_dataset('group_index', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)
    atoms.create_dataset('chain_index', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)

    ## Groups

    groups = topology.create_group("groups")

    groups.create_dataset('id', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)
    groups.create_dataset('name', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)
    groups.create_dataset('type', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)
    groups.create_dataset('component_index', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)

    ## Components

    components = topology.create_group("components")

    components.create_dataset('id', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)
    components.create_dataset('name', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)
    components.create_dataset('type', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)
    components.create_dataset('molecule_index', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)

    ## Molecules

    molecules = topology.create_group("molecules")

    molecules.create_dataset('id', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)
    molecules.create_dataset('name', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)
    molecules.create_dataset('type', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)
    molecules.create_dataset('entity_index', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)

    ## Entities

    entities = topology.create_group("entities")

    entities.create_dataset('id', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)
    entities.create_dataset('name', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)
    entities.create_dataset('type', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)

    ## Chains

    chains = topology.create_group("chains")

    chains.create_dataset('id', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)
    chains.create_dataset('name', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)
    chains.create_dataset('type', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)


    ## Bonds

    bonds = topology.create_group("bonds")

    bonds.create_dataset('atom1_index', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)
    bonds.create_dataset('atom2_index', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)
    bonds.create_dataset('order', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)
    bonds.create_dataset('type', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)


    # Structures

    structures_sd = file.create_group("structures")
    structures_sd.attrs['n_atoms'] = 0
    structures_sd.attrs['n_structures'] = 0
    structures_sd.attrs['n_structures_written'] = 0
    structures_sd.attrs['constant_time_step'] = False
    structures_sd.attrs['time_step'] = 0.0
    structures_sd.attrs['constant_id_step'] = False
    structures_sd.attrs['id_step'] = 0
    structures_sd.attrs['constant_box'] = False
    structures_sd.attrs['pbc'] = 'none' # none, cell, mic, continuous
    structures_sd.attrs['n_degrees_of_freedom'] = 0
    structures_sd.attrs['temperature_from_kinetic_energy'] = False

    structures_sd.create_dataset('id', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)
    structures_sd.create_dataset('time', (0,), dtype=float_type, maxshape=(None,), **global_dataset_options)
    structures_sd.create_dataset('box', (0,3,3), dtype=float_type, maxshape=(None,3,3), **global_dataset_options)
    structures_sd.create_dataset('coordinates', (0,0,3), dtype=float_type, maxshape=(None,None,3), **global_dataset_options)
    structures_sd.create_dataset('velocities', (0,0,3), dtype=float_type, maxshape=(None,None,3), **global_dataset_options)
    structures_sd.create_dataset('kinetic_energy', (0,), dtype=float_type, maxshape=(None,), **global_dataset_options)
    structures_sd.create_dataset('potential_energy', (0,), dtype=float_type, maxshape=(None,), **global_dataset_options)
    structures_sd.create_dataset('temperature', (0,), dtype=float_type, maxshape=(None,), **global_dataset_options)

    return file

