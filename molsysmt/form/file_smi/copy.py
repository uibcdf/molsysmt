from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError

@arg_digest(form='file:smi')
def copy(item, output_filename=None, skip_digestion=False):
    """
    Creating a copy of an item of form file:smi.


    Parameters
    ----------
    item : molecular system
        Argument item.
    output_filename : str or pathlib.Path, default=None
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:smi
        Resulting object in file:smi form.


    .. versionadded:: 1.0.0
    """

    if output_filename is None:
        raise ArgumentError(argument='output_filename', caller='molsysmt.form.file_smi.copy',
                            message='output_filename is required to copy a file:smi item.')

    from shutil import copy as copy_file
    copy_file(item, output_filename)

    return output_filename
