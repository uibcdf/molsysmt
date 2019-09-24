from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'h5': form_name,
    'hdf5': form_name
    }

def to_mdtraj(item, selection=None, frame_indices=None, syntaxis='MDTraj'):
    return to_mdtraj_Trajectory(item, selection=selection, frame_indices=frame_indices,
                                syntaxis=syntaxis)

def to_mdtraj_Trajectory(item, selection=None, frame_indices=None, syntaxis='MDTraj'):

    from mdtraj import load_hdf5 as _mdtraj_load
    tmp_item = _mdtraj_load(item)
    del(_mdtraj_load)
    return tmp_item

def to_mdtraj_Topology(item, selection=None, frame_indices=None, syntaxis='MDTraj'):

    from mdtraj.formats import HDF5TrajectoryFile
    hdf5=HDF5TrajectoryFile(item)
    tmp_item = hdf5.topology
    hdf5.close()
    del(hdf5, HDF5TrajectoryFile)
    return tmp_item

def to_molmodmt_MolMod(item, selection=None, frame_indices=None, syntaxis='MDTraj'):

    from molmodmt.native.io_molmod import from_hdf5 as _from_hdf5
    return _from_hdf5(item, selection=selection, frame_indices=frame_indices, syntaxis=syntaxis)

def to_mdtraj_HDF5TrajectoryFile(item, selection=None, frame_indices=None, syntaxis='MDTraj'):

    from mdtraj.formats import HDF5TrajectoryFile
    return HDF5TrajectoryFile(item)

#### Get

def get_frames_from_atom (item, indices=None, frame_indices=None):

    from molmodmt import get
    tmp_item = to_mdtraj_HDF5TrajectoryFile(item)
    xyz, time, step, box = get(tmp_item, element='atom', indices=indices,
                               frame_indices=frame_indices, frames=True)
    tmp_item.close()
    del(tmp_item, get)
    return xyz, time, step, box

# System

def get_frames_from_system (item, indices=None, frame_indices=None):

    from molmodmt import get
    tmp_item = to_mdtraj_HDF5TrajectoryFile(item)
    xyz, time, step, box = get(tmp_item, element='system',
            frame_indices=frame_indices, frames=True)
    tmp_item.close()
    del(tmp_item, get)
    return xyz, time, step, box

def get_n_frames_from_system (item, indices=None, frame_indices=None):

    from molmodmt import get
    tmp_item = to_mdtraj_HDF5TrajectoryFile(item)
    n_frames = get(tmp_item, element='system',  n_frames=True)
    tmp_item.close()
    del(tmp_item, get)
    return n_frames

def get_n_atoms_from_system (item, indices=None, frame_indices=None):

    from molmodmt import get
    tmp_item = to_mdtraj_HDF5TrajectoryFile(item)
    n_atoms = get(tmp_item, element='system',  n_atoms=True)
    tmp_item.close()
    del(tmp_item, get)
    return n_atoms

