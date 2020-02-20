from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'h5': form_name,
    'hdf5': form_name
    }


def to_mdtraj_Trajectory(item, atom_indices='all', frame_indices='all'):

    from mdtraj import load_hdf5 as mdtraj_load_hdf5
    tmp_item = mdtraj_load_hdf5(item)
    del(_mdtraj_load)
    return tmp_item

def to_mdtraj_Topology(item, atom_indices='all', frame_indices='all'):

    from mdtraj.formats import HDF5TrajectoryFile
    hdf5=HDF5TrajectoryFile(item)
    tmp_item = hdf5.topology
    hdf5.close()
    del(hdf5, HDF5TrajectoryFile)
    return tmp_item

def to_molmodmt_MolMod(item, atom_indices='all', frame_indices='all'):

    from molmodmt.native.io.molmod.files import from_hdf5 as _from_hdf5
    return _from_hdf5(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_mdtraj_HDF5TrajectoryFile(item, atom_indices='all', frame_indices='all'):

    from mdtraj.formats import HDF5TrajectoryFile
    return HDF5TrajectoryFile(item)

def extract_subsystem(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def duplicate(item):

    raise NotImplementedError


#### Get

def get_frames_from_atom (item, indices='all', frame_indices='all'):

    from molmodmt import get
    tmp_item = to_mdtraj_HDF5TrajectoryFile(item)
    xyz, time, step, box = get(tmp_item, target='atom', indices=indices,
                               frame_indices=frame_indices, frames=True)
    tmp_item.close()
    del(tmp_item, get)
    return xyz, time, step, box

# System

def get_frames_from_system (item, indices='all', frame_indices='all'):

    from molmodmt import get
    tmp_item = to_mdtraj_HDF5TrajectoryFile(item)
    xyz, time, step, box = get(tmp_item, target='system',
            frame_indices=frame_indices, frames=True)
    tmp_item.close()
    del(tmp_item, get)
    return xyz, time, step, box

def get_n_frames_from_system (item, indices='all', frame_indices='all'):

    from molmodmt import get
    tmp_item = to_mdtraj_HDF5TrajectoryFile(item)
    n_frames = get(tmp_item, target='system',  n_frames=True)
    tmp_item.close()
    del(tmp_item, get)
    return n_frames

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    from molmodmt import get
    tmp_item = to_mdtraj_HDF5TrajectoryFile(item)
    n_atoms = get(tmp_item, target='system',  n_atoms=True)
    tmp_item.close()
    del(tmp_item, get)
    return n_atoms

def get_form_from_system(item, indices='all', frame_indices='all'):

    from molmodmt import get_form
    return get_form(item)

