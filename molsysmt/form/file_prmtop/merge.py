from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:prmtop')
def merge(items, atom_indices='all', skip_digestion=False):
    """
    Merging multiple items into a single item of form file:prmtop.

    Parameters
    ----------
    items : list of object
        List of items to merge.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file:prmtop
        Merged item.
    """

    raise NotImplementedMethodError()

