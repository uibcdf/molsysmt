from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:bcif.gz')
def copy(item, output_filename=None, skip_digestion=False):
    """
    Creating a copy of an item of form file:bcif.gz.

    Parameters
    ----------
    item : file:bcif.gz
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file:bcif.gz
        Copied item.
    """

    if output_filename is None:
        output_filename = item

    raise NotImplementedMethodError()

