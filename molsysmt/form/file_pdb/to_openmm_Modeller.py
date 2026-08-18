from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:pdb')
def to_openmm_Modeller(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:pdb to openmm.Modeller.

    Parameters
    ----------
    item : file:pdb
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.Modeller
        Converted molecular system representation.
    """

    from .to_openmm_PDBFile import to_openmm_PDBFile
    from molsysmt.form.openmm_PDBFile.to_openmm_Modeller import to_openmm_Modeller as openmm_PDBFile_to_openmm_Modeller

    tmp_item = to_openmm_PDBFile(item, skip_digestion=True)
    tmp_item = openmm_PDBFile_to_openmm_Modeller(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
                                                 skip_digestion=True)

    return tmp_item

