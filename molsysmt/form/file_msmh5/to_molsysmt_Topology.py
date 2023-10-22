from molsysmt._private.digestion import digest

@digest(form='file:msmh5')
def to_molsysmt_Topology(item, atom_indices='all'):

    from . import to_molsysmt_MSMH5FileHandler
    from ..molsysmt_MSMH5FileHandler import to_molsysmt_Topology as molsysmt_MSMH5FileHandler_to_molsysmt_Topology

    handler = to_molsysmt_MSMH5FileHandler(item)
    tmp_item = molsysmt_MSMH5FileHandler_to_molsysmt_Topology(handler, atom_indices=atom_indices)
    handler.close()

    return tmp_item
