from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:uniprot_id')
def merge(items, atom_indices='all', skip_digestion=False):
    """
    Merging multiple items into a single item of form string:uniprot_id.


    Parameters
    ----------
    items : object
        Argument items.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:uniprot_id
        Resulting object in string:uniprot_id form.


    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()
