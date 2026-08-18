from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:inpcrd')
def to_openmm_AmberInpcrdFile(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:inpcrd to openmm.AmberInpcrdFile.

    Parameters
    ----------
    item : file:inpcrd
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.AmberInpcrdFile
        Converted molecular system representation.
    """

    from openmm.app import AmberInpcrdFile

    tmp_item = AmberInpcrdFile(item)

    return tmp_item

