from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:uniprot_id', to_form='string:uniprot_id')
def add(to_item, item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Adding elements from another item into an item of form string:uniprot_id.

    Parameters
    ----------
    to_item : string:uniprot_id
        Target item to modify or add elements to.
    item : string:uniprot_id
        Source item in string:uniprot_id form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:uniprot_id
        Resulting object in string:uniprot_id form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()
