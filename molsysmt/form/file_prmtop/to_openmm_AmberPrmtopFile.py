from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:prmtop')
def to_openmm_AmberPrmtopFile(item, atom_indices='all', skip_digestion=False):
    """
    Converting from file:prmtop to openmm.AmberPrmtopFile.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.AmberPrmtopFile
        Resulting object in openmm.AmberPrmtopFile form.


    .. versionadded:: 1.0.0
    """

    from openmm.app import AmberPrmtopFile

    tmp_item = AmberPrmtopFile(item)

    return tmp_item

