from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MolecularMechanicsDict')
def merge(items, atom_indices='all', skip_digestion=False):
    """
    Merging multiple items into a single item of form molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    items : list of object
        List of items to merge.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.MolecularMechanicsDict
        Merged item.
    """

    raise NotImplementedMethodError()

