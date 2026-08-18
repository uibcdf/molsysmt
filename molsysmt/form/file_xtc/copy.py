from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:xtc')
def copy(item, output_filename=None, skip_digestion=False):
    """
    Creating a copy of an item of form file:xtc.

    Parameters
    ----------
    item : file:xtc
        Source item in file:xtc form.
    output_filename : str or pathlib.Path
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:xtc
        Resulting object in file:xtc form.

    .. versionadded:: 1.0.0
    """

    if output_filename is None:
        output_filename = item

    from shutil import copy as copy_file
    copy_file(item, output_filename)
    tmp_item = output_filename

    return tmp_item
