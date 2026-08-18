from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MolecularMechanicsDict')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : molsysmt.MolecularMechanicsDict
        Source item in molsysmt.MolecularMechanicsDict form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolecularMechanicsDict
        Resulting object in molsysmt.MolecularMechanicsDict form.

    .. versionadded:: 1.0.0
    """

    return item.copy()

