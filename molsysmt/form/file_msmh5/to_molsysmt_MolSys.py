from molsysmt._private.digestion import digest

@digest(form='file:msmh5')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all'):

    from . import to_molsysmt_MSMH5FileHandler
    from ..molsysmt_MSMH5FileHandler import to_molsysmt_MolSys as molsysmt_MSMH5FileHandler_to_molsysmt_MolSys

    handler = to_molsysmt_MSMH5FileHandler(item)
    tmp_item = molsysmt_MSMH5FileHandler_to_molsysmt_MolSys(handler, atom_indices=atom_indices,
                                                           structure_indices=structure_indices)
    handler.close()

    return tmp_item

