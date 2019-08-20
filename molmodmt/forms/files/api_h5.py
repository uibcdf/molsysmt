from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'h5': form_name,
    'hdf5': form_name
    }

def to_mdtraj(item, selection='all', frame_indices='all', syntaxis='MDTraj'):
    return to_mdtraj_Trajectory(item, selection=selection, frame_indices=frame_indices,
                                syntaxis=syntaxis)

def to_mdtraj_Trajectory(item, selection='all', frame_indices='all', syntaxis='MDTraj'):

    from mdtraj import load_hdf5 as _mdtraj_load
    tmp_item = _mdtraj_load(item)
    del(_mdtraj_load)
    return tmp_item

def to_mdtraj_Topology(item, selection='all', syntaxis='MDTraj'):

    from mdtraj.formats import HDF5TrajectoryFile
    hdf5=HDF5TrajectoryFile(item)
    tmp_item = hdf5.topology
    hdf5.close()
    del(hdf5, HDF5TrajectoryFile)
    return tmp_item

def to_molmodmt_MolMod(item, selection='all', frame_indices='all', syntaxis='MDTraj'):

    from molmodmt.native.io_molmod import from_hdf5 as _from_hdf5
    return _from_hdf5(item, selection=selection, frame_indices=frame_indices, syntaxis=syntaxis)

def to_mdtraj_HDF5TrajectoryFile(item, selection='all', syntaxis='MDTraj'):

    from mdtraj.formarts import HDF5TrajectoryFile
    return HDF5TrajectoryFile(item)

