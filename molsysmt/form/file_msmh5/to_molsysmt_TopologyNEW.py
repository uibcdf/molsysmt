from molsysmt._private.digestion import digest

@digest(form='file:h5msm')
def to_molsysmt_TopologyNEW(item, atom_indices='all'):

    from . import to_molsysmt_H5MSMFileHandler
    from ..molsysmt_H5MSMFileHandler import to_molsysmt_TopologyNEW as molsysmt_H5MSMFileHandler_to_molsysmt_TopologyNEW

    handler = to_molsysmt_H5MSMFileHandler(item)
    tmp_item = molsysmt_H5MSMFileHandler_to_molsysmt_TopologyNEW(handler, atom_indices=atom_indices)
    handler.close()

    return tmp_item
