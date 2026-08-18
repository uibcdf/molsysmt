from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:inpcrd')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:inpcrd to molsysmt.Structures.


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
    molsysmt.Structures
        Resulting object in molsysmt.Structures form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.form.file_inpcrd.to_openmm_AmberInpcrdFile import to_openmm_AmberInpcrdFile as file_inpcrd_to_openmm_AmberInpcrdFile
    from molsysmt.form.openmm_AmberInpcrdFile.to_molsysmt_Structures import to_molsysmt_Structures as openmm_AmberInpcrdFile_to_molsysmt_Structures

    # Step 1: Open the file into an OpenMM AmberInpcrdFile object
    tmp_item = file_inpcrd_to_openmm_AmberInpcrdFile(item, skip_digestion=True)
    
    # Step 2: Convert the OpenMM object to native Structures
    tmp_item = openmm_AmberInpcrdFile_to_molsysmt_Structures(tmp_item, atom_indices=atom_indices,
                                                             structure_indices=structure_indices, skip_digestion=True)

    return tmp_item
