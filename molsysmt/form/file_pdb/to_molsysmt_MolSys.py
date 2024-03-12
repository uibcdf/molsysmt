from molsysmt._private.digestion import digest

@digest(form='file:pdb')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', get_missing_bonds=False,
                       skip_digestion=False):

    from . import to_molsysmt_PDBFileHandler
    from ..molsysmt_PDBFileHandler import to_molsysmt_MolSys as molsysmt_PDBFileHandler_to_molsysmt_MolSys

    tmp_item = to_molsysmt_PDBFileHandler(item, skip_digestion=True)
    tmp_item = molsysmt_PDBFileHandler_to_molsysmt_MolSys(tmp_item, atom_indices=atom_indices,
                                                          structure_indices=structure_indices,
                                                          get_missing_bonds=get_missing_bonds,
                                                          skip_digestion=True)

    return tmp_item

