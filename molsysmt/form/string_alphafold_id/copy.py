from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:alphafold_id')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form string:alphafold_id.

    Parameters
    ----------
    item : string:alphafold_id
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    string:alphafold_id
        Copied item.
    """

    raise NotImplementedMethodError()

