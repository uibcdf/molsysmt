def to_nglview_NGLWidget(item, atom_indices='all', structure_indices='all', check=True):

    if check:
        from molsysmt.tools.molsysmt_MolSys import is_molsysmt_MolSys
        from molsysmt._private_tools.exceptions import WrongFormError
        if not is_molsysmt_MolSys(item):
            raise WrongFormError('molsysmt.MolSys')

    try:
        from nglview import show_molsysmt
    except:
        from molsysmt._private_tools.exceptions import LibraryNotFound
        raise LibraryNotFound('nglview')

    tmp_item = show_molsysmt(item, selection=atom_indices, structure_indices=structure_indices)

    return tmp_item

