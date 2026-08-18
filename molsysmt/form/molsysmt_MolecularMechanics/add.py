from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MolecularMechanics', to_form='molsysmt.MolecularMechanics')
def add(to_item, item, atom_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form molsysmt.MolecularMechanics.

    Parameters
    ----------
    to_item : molsysmt.MolecularMechanics
        Target item to modify or add elements to.
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolecularMechanics
        Resulting object in molsysmt.MolecularMechanics form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

