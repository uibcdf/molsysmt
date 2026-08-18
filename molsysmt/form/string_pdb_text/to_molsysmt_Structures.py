from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:pdb_text')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from string:pdb_text to molsysmt.Structures.

    Parameters
    ----------
    item : string:pdb_text
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

    tmp_item = to_molsysmt_PDBFileHandler(item, skip_digestion=True)
    tmp_item = molsysmt_PDBFileHandler_to_molsysmt_Structures(tmp_item, atom_indices=atom_indices,
                                                            structure_indices=structure_indices,
                                                            skip_digestion=True)

    return tmp_item

