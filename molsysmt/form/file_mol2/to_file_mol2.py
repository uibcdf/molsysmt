from molsysmt._private.argdigest import arg_digest
from molsysmt._private.files_and_directories import str_filename

@arg_digest(form='file:mol2')
def to_file_mol2(item, atom_indices='all', structure_indices='all', output_name=None, copy_if_all=True,
                skip_digestion=False):
    """
    Converting from file:mol2 to file.mol2.

    Parameters
    ----------
    item : file:mol2
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file.mol2
        Converted molecular system representation.
    """

    from .extract import extract

    return extract(item, atom_indices=atom_indices, structure_indices=structure_indices, output_name=output_name,
                   copy_if_all=copy_if_all, skip_digestion=True)

