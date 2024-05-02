from molsysmt._private.digestion import digest

@digest(form='file:gro')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', get_missing_bonds=True,
                       skip_digestion=False):

    from .to_molsysmt_GROFileHandler import to_molsysmt_GROFileHandler
    from ..molsysmt_GROFileHandler import to_molsysmt_MolSys as molsysmt_GROFileHandler_to_molsysmt_MolSys

    tmp_item = to_molsysmt_GROFileHandler(item)
    tmp_item = molsysmt_GROFileHandler_to_molsysmt_MolSys(tmp_item, atom_indices=atom_indices,
                                                          structure_indices=structure_indices,
                                                          get_missing_bonds=get_missing_bonds, skip_digestion=True)

    return tmp_item

