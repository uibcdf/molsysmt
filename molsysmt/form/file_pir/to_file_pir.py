from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='file:pir')
def to_file_pir(item, atom_indices='all', output_filename=None, copy_if_all=True, skip_digestion=False):
    """
    Converting from file:pir to file.pir.

    Parameters
    ----------
    item : file:pir
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file.pir
        Converted molecular system representation.
    """

    from .extract import extract

    return extract(item, atom_indices=atom_indices, output_filename=output_filename,
                   copy_if_all=copy_if_all, skip_digestion=True)
