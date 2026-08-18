from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:uniprot_id')
def append_structures(to_item, item, structure_indices='all', skip_digestion=False):
    """
    Appending coordinate structures to an item of form string:uniprot_id.

    Parameters
    ----------
    to_item : string:uniprot_id
        Target item to modify or add elements to.
    item : string:uniprot_id
        Source item in string:uniprot_id form.
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
