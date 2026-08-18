from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:xyz')
def to_file_xyz(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):
    """
    Converting from file:xyz to file.xyz.

    Parameters
    ----------
    item : file:xyz
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file.xyz
        Converted molecular system representation.
    """

    from .extract import extract

    return extract(item, atom_indices=atom_indices, structure_indices=structure_indices,
                   output_filename=output_filename, skip_digestion=True)
