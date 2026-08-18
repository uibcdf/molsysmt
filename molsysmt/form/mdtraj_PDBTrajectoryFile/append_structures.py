from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.PDBTrajectoryFile')
def append_structures(item, structure_id=None, time=None, coordinates=None, box=None, skip_digestion=False):
    """
    Appending coordinate structures to an item of form mdtraj.PDBTrajectoryFile.

    Parameters
    ----------
    item : mdtraj.PDBTrajectoryFile
        Source item in mdtraj.PDBTrajectoryFile form.
    structure_id : object
        Structure identifiers.
    time : numpy.ndarray or quantity
        Simulation time coordinates in picoseconds.
    coordinates : numpy.ndarray or quantity
        Cartesian coordinate array in nanometers.
    box : numpy.ndarray or quantity
        Simulation box vectors in nanometers.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.PDBTrajectoryFile
        Resulting object in mdtraj.PDBTrajectoryFile form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()
