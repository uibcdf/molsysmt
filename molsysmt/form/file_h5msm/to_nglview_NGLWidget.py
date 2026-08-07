from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:h5msm')
def to_nglview_NGLWidget(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.form.molsysmt_H5MSMFileHandler.to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler.to_nglview_NGLWidget import to_nglview_NGLWidget as molsysmt_H5MSMFileHandler_to_nglview_NGLWidget

    handler = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    tmp_item = molsysmt_H5MSMFileHandler_to_nglview_NGLWidget(handler, atom_indices=atom_indices,
                                                              structure_indices=structure_indices, skip_digestion=True)
    handler.close()

    return tmp_item

