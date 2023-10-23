from molsysmt._private.digestion import digest

@digest(form='file:msmh5')
def to_molsysmt_Topology2(item, atom_indices='all'):

    from . import to_molsysmt_MSMH5FileHandler
    from ..molsysmt_MSMH5FileHandler import to_molsysmt_Topology2 as molsysmt_MSMH5FileHandler_to_molsysmt_Topology2

    handler = to_molsysmt_MSMH5FileHandler(item)
    tmp_item = molsysmt_MSMH5FileHandler_to_molsysmt_Topology2(handler, atom_indices=atom_indices)
    handler.close()

    return tmp_item
