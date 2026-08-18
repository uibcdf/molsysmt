from molsysmt._private.argdigest import arg_digest
from molsysmt._private.files_and_directories import str_filename

@arg_digest(form='file:cif')
def to_file_cif(item, atom_indices='all', structure_indices='all', output_name=None, copy_if_all=True,
                skip_digestion=False):
    """
    Converting from file:cif to file.cif.

    Parameters
    ----------
    item : file:cif
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file.cif
        Converted molecular system representation.
    """

    from .extract import extract

    return extract(item, atom_indices=atom_indices, structure_indices=structure_indices, output_name=output_name,
                   copy_if_all=copy_if_all, skip_digestion=True)

