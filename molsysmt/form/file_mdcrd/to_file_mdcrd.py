from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:mdcrd')
def to_file_mdcrd(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):
    """
    Converting from file:mdcrd to file.mdcrd.

    Parameters
    ----------
    item : file:mdcrd
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file.mdcrd
        Converted molecular system representation.
    """

    from .extract import extract

    return extract(item, atom_indices=atom_indices, structure_indices=structure_indices,
                   output_filename=output_filename, skip_digestion=True)
