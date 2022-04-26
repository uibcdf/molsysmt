
def is_mdtraj_XTCTrajectoryFile(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'mdtraj.HDF5TrajectoryFile')

    return output

