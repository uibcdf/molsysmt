from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:mol2')
def copy(item, output_filename=None, skip_digestion=False):
    """
    Creating a copy of an item of form file:mol2.

    Parameters
    ----------
    item : file:mol2
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file:mol2
        Copied item.
    """

    if output_filename is None:
        output_filename = item

    raise NotImplementedMethodError()

