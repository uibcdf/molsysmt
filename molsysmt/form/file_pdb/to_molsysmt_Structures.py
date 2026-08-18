from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:pdb')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:pdb to molsysmt.Structures.

    Parameters
    ----------
    item : file:pdb
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.Structures
        Converted molecular system representation.
    """

    from molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_PDBFileHandler import to_molsysmt_PDBFileHandler
    from molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_Structures import to_molsysmt_Structures as molsysmt_PDBFileHandler_to_molsysmt_Structures

    handler = to_molsysmt_PDBFileHandler(item, skip_digestion=True)
    tmp_item = molsysmt_PDBFileHandler_to_molsysmt_Structures(handler, atom_indices=atom_indices, 
                                                             structure_indices=structure_indices, skip_digestion=True)
    handler.close()

    return tmp_item
