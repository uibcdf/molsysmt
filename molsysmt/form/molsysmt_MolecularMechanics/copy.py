from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MolecularMechanics')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.MolecularMechanics
        Copied item.
    """

    return item.copy()

