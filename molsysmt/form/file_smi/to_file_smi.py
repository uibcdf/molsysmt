from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='file:smi')
def to_file_smi(item, atom_indices='all', output_filename=None, copy_if_all=True, skip_digestion=False):
    """
    Converting from file:smi to file.smi.

    Parameters
    ----------
    item : file:smi
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file.smi
        Converted molecular system representation.
    """

    from .extract import extract

    return extract(item, atom_indices=atom_indices, output_filename=output_filename,
                   copy_if_all=copy_if_all, skip_digestion=True)
