from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:inpcrd')
def to_openmm_AmberInpcrdFile(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:inpcrd to openmm.AmberInpcrdFile.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.AmberInpcrdFile
        Resulting object in openmm.AmberInpcrdFile form.


    .. versionadded:: 1.0.0
    """

    from openmm.app import AmberInpcrdFile

    tmp_item = AmberInpcrdFile(item)

    return tmp_item

