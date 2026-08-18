from molsysmt._private.argdigest import arg_digest
from molsysmt._private.files_and_directories import str_filename

@arg_digest(form='file:xyznpy')
def to_file_xyznpy(item, atom_indices='all', structure_indices='all', output_name=None, copy_if_all=True,
                skip_digestion=False):
    """
    Converting from file:xyznpy to file.xyznpy.

    Parameters
    ----------
    item : file:xyznpy
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file.xyznpy
        Converted molecular system representation.
    """

    from .extract import extract

    return extract(item, atom_indices=atom_indices, structure_indices=structure_indices, output_name=output_name,
                   copy_if_all=copy_if_all, skip_digestion=True)

