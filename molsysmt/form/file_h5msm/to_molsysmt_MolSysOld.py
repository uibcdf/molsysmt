from molsysmt._private.digestion import digest

@digest(form='file:h5msm')
def to_molsysmt_MolSysOld(item, atom_indices='all', structure_indices='all'):

    from . import to_molsysmt_H5MSMFileHandler
    from ..molsysmt_H5MSMFileHandler import to_molsysmt_MolSysOld as molsysmt_H5MSMFileHandler_to_molsysmt_MolSysOld

    handler = to_molsysmt_H5MSMFileHandler(item)
    tmp_item = molsysmt_H5MSMFileHandler_to_molsysmt_MolSysOld(handler, atom_indices=atom_indices,
                                                           structure_indices=structure_indices)
    handler.close()

    return tmp_item

