from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:h5msm')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from ..molsysmt_H5MSMFileHandler.to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from ..molsysmt_H5MSMFileHandler.to_molsysmt_Topology import to_molsysmt_Topology as molsysmt_H5MSMFileHandler_to_molsysmt_Topology

    handler = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    tmp_item = molsysmt_H5MSMFileHandler_to_molsysmt_Topology(handler, atom_indices=atom_indices, skip_digestion=True)
    handler.close()

    return tmp_item
