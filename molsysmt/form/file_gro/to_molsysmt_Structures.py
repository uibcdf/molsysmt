from molsysmt._private.digestion import digest

@digest(form='file:gro')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all',
                       skip_digestion=False):

    from .to_molsysmt_GROFileHandler import to_molsysmt_GROFileHandler
    from ..molsysmt_GROFileHandler import to_molsysmt_Structures as molsysmt_GROFileHandler_to_molsysmt_Structures

    tmp_item = to_molsysmt_GROFileHandler(item, skip_digestion=True)
    tmp_item = molsysmt_GROFileHandler_to_molsysmt_Structures(tmp_item, atom_indices=atom_indices,
                                                          structure_indices=structure_indices,
                                                          skip_digestion=True)

    return tmp_item

