from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from shutil import copy as copy_file

@arg_digest(form='file:crd')
def copy(item, output_filename=None, progress_bar=False, skip_digestion=False):
    """
    Creating a copy of an item of form file:crd.

    Parameters
    ----------
    item : file:crd
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file:crd
        Copied item.
    """

    if output_filename is None:
        output_filename = item

    copy_file(item, output_filename)
    tmp_item = output_filename

    return tmp_item

