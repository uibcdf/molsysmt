from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='molsysmt.MolecularMechanics')
def extract(item, copy_if_all=True, skip_digestion=False):
    """
    Extracting a subset of elements or structures from form molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    copy_if_all : object
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolecularMechanics
        Resulting object in molsysmt.MolecularMechanics form.

    .. versionadded:: 1.0.0
    """

    raise NotWithThisMolecularSystemError()

