from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='molsysmt.CIFFileHandler')
def copy(item, output_filename=None, skip_digestion=False):
    """
    Creating a copy of an item of form molsysmt.CIFFileHandler.

    Parameters
    ----------
    item : molsysmt.CIFFileHandler
        Source item in molsysmt.CIFFileHandler form.
    output_filename : str or pathlib.Path
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.CIFFileHandler
        Resulting object in molsysmt.CIFFileHandler form.

    .. versionadded:: 1.0.0
    """

    if output_filename is None:
        output_filename = item

    from shutil import copy as copy_file
    copy_file(item, output_filename)
    tmp_item = output_filename

    return tmp_item

