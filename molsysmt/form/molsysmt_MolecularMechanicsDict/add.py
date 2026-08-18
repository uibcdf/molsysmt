from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MolecularMechanicsDict', to_form='molsysmt.MolecularMechanicsDict')
def add(to_item, item, atom_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    to_item : molsysmt.MolecularMechanicsDict
        Target item to modify or add elements to.
    item : molsysmt.MolecularMechanicsDict
        Source item in molsysmt.MolecularMechanicsDict form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolecularMechanicsDict
        Resulting object in molsysmt.MolecularMechanicsDict form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

