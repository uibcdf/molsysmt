def to_nglview_NGLWidget(item, atom_indices='all', frame_indices='all', check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_MolSys import is_molsysmt_MolSys
        from molsysmt._private_tools.exceptions import ItemWithWrongForm
        if not is_molsysmt_MolSys(item):
            raise ItemWithWrongForm('molsysmt.MolSys')

    try:
        from nglview import show_molsysmt
    except:
        from molsysmt._private_tools.exceptions import LibraryNotFound
        raise LibraryNotFound('nglview')

    tmp_item = show_molsysmt(item, selection=atom_indices, frame_indices=frame_indices)

    return tmp_item

