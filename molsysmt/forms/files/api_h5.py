from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'h5': form_name,
    'hdf5': form_name
    }

info=["",""]
with_topology=True
with_trajectory=True

def to_mdtraj_Trajectory(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from mdtraj import load_hdf5 as mdtraj_load_hdf5
    tmp_item = mdtraj_load_hdf5(item)
    return tmp_item

def to_mdtraj_Topology(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    tmp_item = to_mdtraj_HDF5TrajectoryFile(item)
    tmp_item2 = tmp_item.topology
    tmp_item.close()
    del(tmp_item)
    return tmp_item2

def to_mdtraj_HDF5TrajectoryFile(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from mdtraj.formats import HDF5TrajectoryFile
    return HDF5TrajectoryFile(item)

def to_openmm_Topology(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    tmp_item = to_mdtraj_Topology(item)
    tmp_item = tmp_item.to_openmm()
    return tmp_item

def to_molsysmt_MolSys(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.files import from_h5 as _from_h5
    return _from_h5(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_molsysmt_Topology(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.files import from_h5 as _from_h5
    return _from_h5(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_molsysmt_DataFrame(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.dataframe.files import from_h5 as _from_h5
    return _from_h5(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_molsysmt_Trajectory(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory.files import from_h5 as _from_h5
    return _from_h5(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_pdb(item, trajectory_item=None, output_filepath=None, atom_indices='all',
           frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_MolSys import to_pdb as molsysmt_MolSys_to_pdb
    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return molsysmt_MolSys_to_pdb(tmp_item, output_filepath=output_filepath)

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError


#### Get

def get_frames_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt import get
    tmp_item = to_mdtraj_HDF5TrajectoryFile(item)
    xyz, time, step, box = get(tmp_item, target='atom', indices=indices,
                               frame_indices=frame_indices, frames=True)
    tmp_item.close()
    del(tmp_item, get)
    return xyz, time, step, box

# System

def get_frames_from_system (item, indices='all', frame_indices='all'):

    from molsysmt import get
    tmp_item = to_mdtraj_HDF5TrajectoryFile(item)
    xyz, time, step, box = get(tmp_item, target='system',
            frame_indices=frame_indices, frames=True)
    tmp_item.close()
    del(tmp_item, get)
    return xyz, time, step, box

def get_n_frames_from_system (item, indices='all', frame_indices='all'):

    from molsysmt import get
    tmp_item = to_mdtraj_HDF5TrajectoryFile(item)
    n_frames = get(tmp_item, target='system',  n_frames=True)
    tmp_item.close()
    del(tmp_item, get)
    return n_frames

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    from molsysmt import get
    tmp_item = to_mdtraj_HDF5TrajectoryFile(item)
    n_atoms = get(tmp_item, target='system',  n_atoms=True)
    tmp_item.close()
    del(tmp_item, get)
    return n_atoms

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

