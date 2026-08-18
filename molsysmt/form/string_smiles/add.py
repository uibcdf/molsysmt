from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:smiles', to_form='string:smiles')
def add(to_item, item, atom_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form string:smiles.

    Parameters
    ----------
    to_item : string:smiles
        Target item to modify or add elements to.
    item : string:smiles
        Source item in string:smiles form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:smiles
        Resulting object in string:smiles form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()
