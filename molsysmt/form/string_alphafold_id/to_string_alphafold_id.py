from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:alphafold_id')
def to_string_alphafold_id(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Converting from string:alphafold_id to string.alphafold.id.

    Parameters
    ----------
    item : string:alphafold_id
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    string.alphafold.id
        Converted molecular system representation.
    """

    from .extract import extract

    return extract(item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=copy_if_all, skip_digestion=True)

