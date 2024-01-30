from molsysmt._private.digestion import digest

@digest(form='file:h5msm')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from . import to_molsysmt_H5MSMFileHandler
    from ..molsysmt_H5MSMFileHandler import to_molsysmt_MolSys as molsysmt_H5MSMFileHandler_to_molsysmt_MolSys

    handler = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    tmp_item = molsysmt_H5MSMFileHandler_to_molsysmt_MolSys(handler, atom_indices=atom_indices,
                                                           structure_indices=structure_indices,
                                                           skip_digestion=True)
    handler.close()

    return tmp_item

