from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from shutil import copy as copy_file

@arg_digest(form='file:crd')
def copy(item, output_filename=None, progress_bar=False, skip_digestion=False):
    """
    Creating a copy of an item of form file:crd.


    Parameters
    ----------
    item : molecular system
        Argument item.
    output_filename : str or pathlib.Path, default=None
        Output file path for serialization.
    progress_bar : object, default=False
        Argument progress_bar.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:crd
        Resulting object in file:crd form.


    .. versionadded:: 1.0.0
    """

    if output_filename is None:
        output_filename = item

    copy_file(item, output_filename)
    tmp_item = output_filename

    return tmp_item

