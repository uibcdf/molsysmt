import h5py
import numpy as np

msmh5_version = "1.0"

class MSMH5FileHandler():

    def __init__(self, filename, io_mode='r', creator='MolSysMT', compression="gzip", compression_opts=4,
            int_precision='single', float_precision='single', closed=False):

        self.file = None

        if io_mode=='w':

            self.file = _new_msmfile(filename, creator=creator, compression=compression,
                    compression_opts=compression_opts, int_precision=int_precision,
                    float_precision=float_precision)

        elif io_mode=='r':

            self.file = h5py.File(filename, "r")

        else:

            raise NotImplementedError

        if closed:
            self.file.close()

    def close(self):

        self.file.close()

def _new_msmfile(filename, creator='MolSysMT', compression="gzip", compression_opts=4,
        int_precision='single', float_precision='single'):

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

    global_dataset_options = {
            'compression':compression,
            'compression_opts':compression_opts,
            }

    # Topology

    topology = file.create_group("topology")

    ## Atoms

    atoms = topology.create_group("atoms")
    atoms.attrs['n_atoms'] = 0

    atoms.create_dataset('id', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)
    atoms.create_dataset('name', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)
    atoms.create_dataset('type', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)
    atoms.create_dataset('group_index', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)
    atoms.create_dataset('chain_index', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)

    ## Groups

    groups = topology.create_group("groups")
    groups.attrs['n_groups'] = 0

    groups.create_dataset('id', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)
    groups.create_dataset('name', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)
    groups.create_dataset('type', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)
    groups.create_dataset('component_index', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)

    ## Components

    components = topology.create_group("components")
    components.attrs['n_components'] = 0

    components.create_dataset('id', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)
    components.create_dataset('name', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)
    components.create_dataset('type', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)
    components.create_dataset('molecule_index', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)

    ## Molecules

    molecules = topology.create_group("molecules")
    molecules.attrs['n_molecules'] = 0

    molecules.create_dataset('id', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)
    molecules.create_dataset('name', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)
    molecules.create_dataset('type', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)
    molecules.create_dataset('entity_index', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)

    ## Entities

    entities = topology.create_group("entities")
    entities.attrs['n_entities'] = 0

    entities.create_dataset('id', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)
    entities.create_dataset('name', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)
    entities.create_dataset('type', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)

    ## Chains

    chains = topology.create_group("chains")
    chains.attrs['n_chains'] = 0

    chains.create_dataset('id', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)
    chains.create_dataset('name', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)
    chains.create_dataset('type', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)


    ## Bonds

    bonds = topology.create_group("bonds")
    bonds.attrs['n_bonds'] = 0

    bonds.create_dataset('atom1_index', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)
    bonds.create_dataset('atom2_index', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)
    bonds.create_dataset('order', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)
    bonds.create_dataset('type', (0,), dtype=h5py.string_dtype(), maxshape=(None,), **global_dataset_options)


    # Structures

    structures = file.create_group("structures")
    structures.attrs['n_atoms'] = 0
    structures.attrs['n_structures'] = 0
    structures.attrs['constant_time_step']=False
    structures.attrs['time_step']=0.0
    structures.attrs['constant_id_step']=False
    structures.attrs['id_step']=0
    structures.attrs['constant_volume']=False
    structures.attrs['constant_temperature']=False
    structures.attrs['length_unit']='nm'
    structures.attrs['time_unit']='ps'
    structures.attrs['energy_unit']='kJ/mol'

    bonds.create_dataset('id', (0,), dtype=int_type, maxshape=(None,), **global_dataset_options)
    bonds.create_dataset('box', (0,6), dtype=float_type, maxshape=(None,6), **global_dataset_options)
    bonds.create_dataset('coordinates', (0,0,3), dtype=float_type, maxshape=(None,None,3), **global_dataset_options)
    bonds.create_dataset('velocities', (0,0,3), dtype=float_type, maxshape=(None,None,3), **global_dataset_options)
    bonds.create_dataset('kinetic_energy', (0,), dtype=float_type, maxshape=(None,), **global_dataset_options)
    bonds.create_dataset('potential_energy', (0,), dtype=float_type, maxshape=(None,), **global_dataset_options)
    bonds.create_dataset('temperature', (0,), dtype=float_type, maxshape=(None,), **global_dataset_options)

    return file

