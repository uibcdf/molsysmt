from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:pdb_id')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form string:pdb_id.

    Parameters
    ----------
    item : string:pdb_id
        Source item in string:pdb_id form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:pdb_id
        Resulting object in string:pdb_id form.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError()

