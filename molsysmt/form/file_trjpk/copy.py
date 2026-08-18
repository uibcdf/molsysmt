from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='file:trjpk')
def copy(item, output_filename=None, skip_digestion=False):
    """
    Creating a copy of an item of form file:trjpk.

    Parameters
    ----------
    item : file:trjpk
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file:trjpk
        Copied item.
    """

    if output_filename is None:
        output_filename = item

    from shutil import copy as copy_file
    copy_file(item, output_filename)
    tmp_item = output_filename

    return tmp_item

