from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MolecularMechanicsDict')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : molsysmt.MolecularMechanicsDict
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.MolecularMechanicsDict
        Copied item.
    """

    return item.copy()

