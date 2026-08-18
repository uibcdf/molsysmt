from molsysmt._private.smonitor import NotImplementedMethodError, ArgumentError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:fasta')
def copy(item, output_filename=None, skip_digestion=False):
    """
    Creating a copy of an item of form file:fasta.

    Parameters
    ----------
    item : file:fasta
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file:fasta
        Copied item.
    """

    if output_filename is None:
        raise ArgumentError(argument='output_filename', caller='molsysmt.form.file_fasta.copy',
                            message='output_filename is required to copy a file:fasta item.')

    from shutil import copy as copy_file
    copy_file(item, output_filename)

    return output_filename
