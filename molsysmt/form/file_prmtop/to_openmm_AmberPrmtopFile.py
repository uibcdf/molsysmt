from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:prmtop')
def to_openmm_AmberPrmtopFile(item, atom_indices='all', skip_digestion=False):
    """
    Converting from file:prmtop to openmm.AmberPrmtopFile.

    Parameters
    ----------
    item : file:prmtop
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.AmberPrmtopFile
        Converted molecular system representation.
    """

    from openmm.app import AmberPrmtopFile

    tmp_item = AmberPrmtopFile(item)

    return tmp_item

