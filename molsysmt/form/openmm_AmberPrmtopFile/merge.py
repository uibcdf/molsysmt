from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.AmberPrmtopFile')
def merge(items, atom_indices='all', skip_digestion=False):
    """
    Merging multiple items into a single item of form openmm.AmberPrmtopFile.

    Parameters
    ----------
    items : list of object
        List of items to merge.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.AmberPrmtopFile
        Merged item.
    """

    raise NotImplementedMethodError()

