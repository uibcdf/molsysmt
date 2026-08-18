from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MolSys')
def to_XYZ(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from molsysmt.MolSys to XYZ.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    XYZ
        Converted molecular system representation.
    """

    from . import get_coordinates_from_atom

    tmp_item = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)

    return tmp_item

