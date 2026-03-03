from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:h5msm')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from ..molsysmt_H5MSMFileHandler.to_molsysmt_Structures import to_molsysmt_Structures as molsysmt_H5MSMFileHandler_to_molsysmt_Structures

    handler = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    tmp_item = molsysmt_H5MSMFileHandler_to_molsysmt_Structures(handler, atom_indices=atom_indices,
            structure_indices=structure_indices, skip_digestion=True)
    handler.close()

    return tmp_item
