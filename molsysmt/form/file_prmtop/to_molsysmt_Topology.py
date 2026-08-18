from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:prmtop')
def to_molsysmt_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:prmtop to molsysmt.Topology.

    Parameters
    ----------
    item : file:prmtop
        Source item in file:prmtop form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Topology
        Resulting object in molsysmt.Topology form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.file_prmtop.to_openmm_AmberPrmtopFile import to_openmm_AmberPrmtopFile as file_prmtop_to_openmm_AmberPrmtopFile
    from molsysmt.form.openmm_AmberPrmtopFile.to_molsysmt_Topology import to_molsysmt_Topology as openmm_AmberPrmtopFile_to_molsysmt_Topology

    # Step 1: Open the file into an OpenMM AmberPrmtopFile object
    tmp_item = file_prmtop_to_openmm_AmberPrmtopFile(item, skip_digestion=True)
    
    # Step 2: Convert the OpenMM object to native Topology
    tmp_item = openmm_AmberPrmtopFile_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices,
                                                           skip_digestion=True)

    return tmp_item
