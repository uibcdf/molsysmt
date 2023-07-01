from molsysmt._private.exceptions import NotImplementedIteratorError

class StructuresIterator():

    def __init__(self, molecular_system, atom_indices='all', start=0, interval=1, stop=None, chunk=1, structure_indices=None):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedIteratorError

class TopologyIterator():

    def __init__(self, molecular_system):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedIteratorError

#
#from molsysmt import pyunitwizard as puw
#from molsysmt._private.variables import is_all
#
#
#def iterate_mdtraj_trajectory(traj, start=0, stop=None,
#                              interval=1, selection="all", chunk_size=1):
#    """ Iterate a mdtraj Trajectory.
#
#        Parameters
#        ----------
#        traj : mdtraj.Trajectory
#            A trajectory
#
#        start: int
#            First frame index of the trajectory to start with.
#
#        stop: int, default=None
#            The iteration finishes if the current frame index
#            is larger than or equal to this integer.
#
#        interval : int, default=1
#            Number of structure indices to skip in each iteration
#
#        selection : arraylike of int or 'all', default='all'
#            The indices of the selected atoms.
#
#        chunk_size : int, default=1
#            Amount of frames in the output of each iteration.
#
#        Yields
#        ------
#        box : numpy.ndarray of shape (3, 3)
#                The box of the trajectory
#
#        coordinates : numpy.ndarray of shape (n_atoms, 3)
#            The coordinates of the trajectory.
#
#        time :  float
#            The time of the trajectory.
#    """
#    iter_end = traj.n_frames
#    if stop is not None:
#        iter_end = stop
#
#    if chunk_size > 1:
#        interval = chunk_size
#
#    for frame in range(start, iter_end, interval):
#        time = puw.quantity(traj.time[frame: frame + chunk_size],
#                            "picoseconds")
#
#        if is_all(selection):
#            if chunk_size == 1:
#                coords = puw.quantity(traj.xyz[frame], "nanometers")
#            else:
#                coords = puw.quantity(traj.xyz[frame: frame + chunk_size],
#                                      "nanometers")
#        else:
#            if chunk_size == 1:
#                coords = puw.quantity(traj.xyz[frame, selection, :], "nanometers")
#            else:
#                coords = puw.quantity(traj.xyz[frame: frame + chunk_size, selection, :],
#                                      "nanometers")
#
#        if chunk_size == 1:
#            box = puw.quantity(traj.unitcell_vectors[frame],
#                               "nanometers")
#        else:
#            box = puw.quantity(traj.unitcell_vectors[frame: frame + chunk_size],
#                               "nanometers")
#
#        yield time, coords, box
