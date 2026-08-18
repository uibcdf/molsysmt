from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:inpcrd')
def copy(item, output_filename=None, skip_digestion=False):
    """
    Creating a copy of an item of form file:inpcrd.

    Parameters
    ----------
    item : file:inpcrd
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file:inpcrd
        Copied item.
    """

    from shutil import copy as copy_file
    copy_file(item, output_filename)
    tmp_item = output_filename

    return tmp_item

