from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(forms='molsysmt.StructuresDict')
def merge(items, atom_indices='all', structure_indices='all'):
    """
    Merging multiple items into a single item of form molsysmt.StructuresDict.

    Parameters
    ----------
    items : list of object
        List of items to merge.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.StructuresDict
        Merged item.
    """

    raise NotImplementedMethodError()

