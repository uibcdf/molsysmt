from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:dcd')
def copy(item):
    """
    Creating a copy of an item of form file:dcd.

    Parameters
    ----------
    item : file:dcd
        Source item in file:dcd form.

    Returns
    -------
    file:dcd
        Resulting object in file:dcd form.

    .. versionadded:: 1.0.0
    """

    from shutil import copy as copy_file
    copy_file(item, output_filename)
    tmp_item = output_filename

    return tmp_item

