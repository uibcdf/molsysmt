from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:h5msm')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from ..molsysmt_H5MSMFileHandler.to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from ..molsysmt_H5MSMFileHandler.to_molsysmt_MolSys import to_molsysmt_MolSys as molsysmt_H5MSMFileHandler_to_molsysmt_MolSys

    handler = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    tmp_item = molsysmt_H5MSMFileHandler_to_molsysmt_MolSys(handler, atom_indices=atom_indices,
                                                           structure_indices=structure_indices,
                                                           skip_digestion=True)
    handler.close()

    return tmp_item

