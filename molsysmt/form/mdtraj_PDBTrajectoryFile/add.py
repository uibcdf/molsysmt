from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.PDBTrajectoryFile', to_form='mdtraj.PDBTrajectoryFile')
def add(to_item, item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form mdtraj.PDBTrajectoryFile.

    Parameters
    ----------
    to_item : mdtraj.PDBTrajectoryFile
        Target item to modify or add elements to.
    from_item : object
        Source item providing elements.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mdtraj.PDBTrajectoryFile
        Target item with added elements.
    """

    raise NotImplementedMethodError()
