from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:crd')
def merge(items, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Merging multiple items into a single item of form file:crd.

    Parameters
    ----------
    items : list of object
        List of items to merge.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file:crd
        Merged item.
    """

    raise NotImplementedMethodError()

