from molsysmt._private.digestion import digest

@digest()
def open_file(filename, mode='read'):

    from mdtraj.formats import HDF5TrajectoryFile

    if mode=='read':
        return HDF5TrajectoryFile(filename, mode='r')
    elif mode=='write':
        return HDF5TrajectoryFile(filename, mode='w')

