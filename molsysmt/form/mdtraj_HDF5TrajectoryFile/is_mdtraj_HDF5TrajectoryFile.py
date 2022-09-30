
def is_mdtraj_HDF5TrajectoryFile(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'mdtraj.formats.hdf5.HDF5TrajectoryFile')

    return output

