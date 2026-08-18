from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:gro')
def to_openmm_Modeller(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:gro to openmm.Modeller.


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
    openmm.Modeller
        Resulting object in openmm.Modeller form.


    .. versionadded:: 1.0.0
    """

    from .to_openmm_GromacsGroFile import to_openmm_GromacsGroFile
    from molsysmt.form.openmm_GromacsGroFile.to_openmm_Modeller import to_openmm_Modeller as openmm_GromacsGroFile_to_openmm_Modeller

    tmp_item = to_openmm_GromacsGroFile(item, skip_digestion=True)
    tmp_item = openmm_GromacsGroFile_to_openmm_Modeller(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, skip_digestion=True)

    return tmp_item

