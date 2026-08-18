from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.PDBTrajectoryFile')
def append_structures(item, structure_id=None, time=None, coordinates=None, box=None, skip_digestion=False):
    """
    Appending coordinate structures to an item of form mdtraj.PDBTrajectoryFile.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_id : object, default=None
        Argument structure_id.
    time : object, default=None
        Argument time.
    coordinates : object, default=None
        Argument coordinates.
    box : object, default=None
        Argument box.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.PDBTrajectoryFile
        Resulting object in mdtraj.PDBTrajectoryFile form.


    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()
