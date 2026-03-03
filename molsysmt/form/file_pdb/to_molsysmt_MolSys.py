from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:pdb')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', get_missing_bonds=True,
                       skip_digestion=False):

    from .to_molsysmt_PDBFileHandler import to_molsysmt_PDBFileHandler
    from ..molsysmt_PDBFileHandler.to_molsysmt_MolSys import to_molsysmt_MolSys as molsysmt_PDBFileHandler_to_molsysmt_MolSys

    tmp_item = to_molsysmt_PDBFileHandler(item, skip_digestion=True)
    tmp_item = molsysmt_PDBFileHandler_to_molsysmt_MolSys(tmp_item, atom_indices=atom_indices,
                                                          structure_indices=structure_indices,
                                                          get_missing_bonds=get_missing_bonds,
                                                          skip_digestion=True)

    return tmp_item

