from molsysmt._private.smonitor import NotImplementedMethodError, ArgumentError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:fasta')
def copy(item, output_filename=None, skip_digestion=False):
    """
    Creating a copy of an item of form file:fasta.


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
    file:fasta
        Resulting object in file:fasta form.


    .. versionadded:: 1.0.0
    """

    if output_filename is None:
        raise ArgumentError(argument='output_filename', caller='molsysmt.form.file_fasta.copy',
                            message='output_filename is required to copy a file:fasta item.')

    from shutil import copy as copy_file
    copy_file(item, output_filename)

    return output_filename
