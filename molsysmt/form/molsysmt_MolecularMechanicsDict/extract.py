from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='molsysmt.MolecularMechanicsDict')
def extract(item, copy_if_all=True, skip_digestion=False):
    """
    Extracting a subset of atoms or structures from form molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : molsysmt.MolecularMechanicsDict
        Source item.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atom selection to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices to extract.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.MolecularMechanicsDict
        Extracted subset in the same form.
    """

    if copy_if_all:
        return item.copy()
    else:
        return item

